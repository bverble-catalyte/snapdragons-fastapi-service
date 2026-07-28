from contextlib import asynccontextmanager
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import insert
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import DatabaseStatus, Product, ProductCreate, ProductRead


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
DbSession = Annotated[Session, Depends(get_db)]


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


@app.get(
    "/products",
    response_model=List[ProductRead],
    response_description="The list of products",
)
def view_products(db: DbSession):
    """View all products in the database."""
    products = db.query(Product).filter(Product.is_deleted == False)
    return products


@app.get(
    "/products/search",
    response_model=List[ProductRead],
    response_description="The list of products with matching name and unit",
)
def search_products(
    db: DbSession,
    name: Annotated[str, Query(description="The product name is required.")],
    unit: Annotated[str | None, Query(description="Optional product unit.")] = None,
):
    """Search the database for products with matching name and unit."""
    query = db.query(Product).filter(Product.is_deleted == False)
    if unit is not None:
        query = query.filter(Product.unit == unit)

    normalized_name = normalize(name)
    return [p for p in query.all() if normalized_name in normalize(p.name)]


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
)
def create_product(db: DbSession, product: ProductCreate):
    """Create a new product."""
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    return new_product


@app.put(
    "/products/{id}",
    response_model=ProductRead,
    response_description="The updated product",
    responses={404: {"description": "A product with that ID does not exist."}},
)
def update_product(
    db: DbSession,
    product_create: ProductCreate,
    product: Product = Depends(get_product_by_id),
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
    responses={404: {"description": "A product with that ID does not exist."}},
)
def delete_product(
    db: DbSession, product: Product = Depends(get_product_by_id)
) -> None:
    """Soft deletes product based on given ID."""
    product.is_deleted = True
    db.commit()
