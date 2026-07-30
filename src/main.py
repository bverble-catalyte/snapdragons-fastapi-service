from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Annotated, List
from zoneinfo import ZoneInfo

import jwt
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine, get_db
from models import (
    Category,
    CategoryCreate,
    CategoryRead,
    CategoryReadWithProducts,
    DatabaseStatus,
    Product,
    ProductCreate,
    ProductRead,
    TokenRead,
    User,
    UserCredentials,
)

# generate a secret key in PowerShell:
#   [Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
SECRET_KEY = "Ei/RWnrANct1ctayTdpm1YHoakgMqb7DJK5s8CmSAoU="
ALGORITHM = "HS256"
HASHER = PasswordHash.recommended()


get_bearer_token = OAuth2PasswordBearer(tokenUrl="/tokens")


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal
    with SessionLocal() as session:
        user = User(
            **{
                "username": "manager",
                # password == "admin"
                "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$cZwzIBCPEaSFju3XYSXT2Q$Tt3jLTrMTyb+hafu05PHSv2eZbv3YYh5kzmkrlDktR8",
            }
        )
        session.add(user)
        session.commit()
    yield


app = FastAPI(lifespan=lifespan)
DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(db: DbSession, token: str = Depends(get_bearer_token)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid bearer token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub") or "")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (ValueError, jwt.PyJWTError):
        raise credentials_exception

    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user


@app.post(
    "/tokens",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenRead,
    response_description="The access token, valid for five minutes",
    responses={401: {"description": "The request is unauthenticated"}},
)
def create_token(db: DbSession, credentials: UserCredentials):
    user = (
        db.query(User)
        .where(
            User.username == credentials.username,
        )
        .first()
    )

    if user is None or not HASHER.verify(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expire_at = datetime.now(ZoneInfo("America/Chicago")) + timedelta(minutes=5)
    data = {
        "sub": str(user.id),
        "exp": expire_at,
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


def normalize(s: str) -> str:
    """Normalizes the formatting of strings for search.

    Args:
        s (str): The string to be reformatted.

    Returns:
        A normalized string for search.
    """
    return "".join(s.lower().split())


def get_product_by_id(id: int, db: DbSession) -> Product:
    """Looks up a product by a given ID or raises a 404: Not Found"""
    product = (
        db.query(Product).filter(Product.id == id, Product.is_deleted == False).first()
    )
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )
    return product


def get_category_by_id(id: int, db: DbSession) -> Category:
    """Looks up a category by a given ID or raises a 404: Not Found"""
    category = (
        db.query(Category)
        .filter(Category.id == id, Category.is_deleted == False)
        .first()
    )
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {id} not found",
        )
    return category


@app.get(
    "/db-check",
    response_model=DatabaseStatus,
    response_description="The connection status",
)
def db_check(db: DbSession):
    """Check the status of the database connection."""
    try:
        # Perform a simple query to verify connection
        count = db.query(Product).count()
        return {"status": "connected", "product_count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database health check failed",
        )


# =========================================
#           PRODUCTS
# =========================================
@app.get(
    "/products",
    response_model=List[ProductRead],
    response_description="The list of products",
)
def view_products(
    db: DbSession,
    name: Annotated[
        str | None, Query(description="Name search query, partial match")
    ] = None,
    unit: Annotated[
        str | None, Query(description="Unit search query, exact match")
    ] = None,
):
    """View all products in the database, optionally filtered by name and/or unit of sale."""
    products_query = db.query(Product).filter(Product.is_deleted == False)
    if unit is not None:
        products_query = products_query.filter(Product.unit == unit)

    if name is not None:
        normalized_name = normalize(name)
        return [p for p in products_query.all() if normalized_name in normalize(p.name)]
    else:
        return products_query.all()


@app.get(
    "/products/{id}",
    response_model=ProductRead,
    response_description="The product",
    responses={404: {"description": "A product with that ID does not exist."}},
)
def get_product(product: Product = Depends(get_product_by_id)) -> Product:
    """View a product with a given ID."""
    return product


@app.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductRead,
    response_description="The newly created product",
    responses={
        401: {"description": "The client is not authenticated"},
        404: {"description": "The category was not found"},
    },
)
def create_product(
    db: DbSession, product: ProductCreate, user: User = Depends(get_current_user)
):
    """Create a new product."""
    category = db.get(Category, product.category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="The category was not found")
    new_product = Product(**product.model_dump())
    category.products.append(new_product)
    db.add(new_product)
    db.commit()
    return new_product


@app.put(
    "/products/{id}",
    response_model=ProductRead,
    response_description="The updated product",
    responses={
        401: {"description": "The client is not authenticated"},
        404: {"description": "A product with that ID does not exist."},
    },
)
def update_product(
    db: DbSession,
    product_create: ProductCreate,
    product: Product = Depends(get_product_by_id),
    user: User = Depends(get_current_user),
) -> Product:
    """Update a product with a given ID."""
    for field, value in product_create.model_dump().items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@app.delete(
    "/products/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "The client is not authenticated"},
        404: {"description": "A product with that ID does not exist."},
    },
)
def delete_product(
    db: DbSession,
    product: Product = Depends(get_product_by_id),
    user: User = Depends(get_current_user),
) -> None:
    """Soft deletes product based on given ID."""
    product.is_deleted = True
    db.commit()


# =========================================
#           CATEGORIES
# =========================================


@app.get(
    "/categories",
    response_model=List[CategoryRead],
    response_description="The list of categories",
)
def view_categories(
    db: DbSession,
    name: Annotated[
        str | None, Query(description="Name search query, partial match")
    ] = None,
):
    """View all categories in the database"""
    categories_query = db.query(Category).filter(Category.is_deleted == False)
    if name is not None:
        normalized_name = normalize(name)
        return [
            p for p in categories_query.all() if normalized_name in normalize(p.name)
        ]
    else:
        return categories_query.all()


@app.get(
    "/categories/{id}",
    response_model=CategoryRead,
    response_description="The category",
    responses={404: {"description": "A category with that ID does not exist."}},
)
def get_category(category: Category = Depends(get_category_by_id)) -> Category:
    """View a category with a given ID."""
    return category


@app.get(
    "/categories/{id}/products",
    response_model=CategoryReadWithProducts,
    response_description="The category",
    responses={404: {"description": "A category with that ID does not exist."}},
)
def get_category_with_products(
    category: Category = Depends(get_category_by_id),
) -> Category:
    """View a category with a given ID and all its associated products."""
    return category


@app.post(
    "/categories",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryRead,
    response_description="The newly created category",
    responses={401: {"description": "The client is not authenticated"}},
)
def create_category(
    db: DbSession, category: CategoryCreate, user: User = Depends(get_current_user)
):
    """Create a new category."""
    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    return new_category


@app.put(
    "/categories/{id}",
    response_model=CategoryRead,
    response_description="The updated category",
    responses={
        401: {"description": "The client is not authenticated"},
        404: {"description": "A category with that ID does not exist."},
    },
)
def update_category(
    db: DbSession,
    category_create: CategoryCreate,
    category: Category = Depends(get_category_by_id),
    user: User = Depends(get_current_user),
) -> Category:
    """Update a category with a given ID."""
    for field, value in category_create.model_dump().items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


@app.delete(
    "/categories/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "The client is not authenticated"},
        404: {"description": "A category with that ID does not exist."},
        409: {
            "description": "The category must not have any products associated with it."
        },
    },
)
def delete_category(
    db: DbSession,
    category: Category = Depends(get_category_by_id),
    user: User = Depends(get_current_user),
) -> None:
    """Soft deletes emptry categories based on given ID."""
    product_count = len(category.products)
    if product_count != 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The category must not have any products associated with it. Currently, this category is associated with {product_count} product{'s' if product_count != 1 else ''}.",
        )
    category.is_deleted = True
    db.commit()
