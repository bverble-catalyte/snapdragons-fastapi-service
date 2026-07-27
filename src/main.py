from contextlib import asynccontextmanager
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import insert
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Product, ProductCreate, ProductRead


@asynccontextmanager
async def lifespan(app: FastAPI):
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


@app.get("/db-check")
def db_check(db: DbSession):
    try:
        # Perform a simple query to verify connection
        count = db.query(Product).count()
        return {"status": "connected", "product_count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}",
        )


@app.get("/products", response_model=List[ProductRead])
def view_products(db: DbSession):
    """Views all products within the database.

    Args:
        db (Session): The database session.

    Returns:
        A list of products in the database.
    """
    products = db.query(Product).all()
    return products


@app.get("/products/search", response_model=List[ProductRead])
def search_products(
    db: DbSession,
    name: Annotated[str, Query(description="The product name is required.")],
    unit: Annotated[str | None, Query(description="Optional product unit.")] = None,
):
    """Searches the database for products with matching name and unit.

    Args:
        name (str): The product name.
        unit (str): The product's unit of sale; optional.
        db (Session): The database session.

    Returns:
        A list of products with a matching name and unit.
    """
    query = db.query(Product)
    if unit is not None:
        query = query.filter(Product.unit == unit)

    normalized_name = normalize(name)
    return [p for p in query.all() if normalized_name in normalize(p.name)]


@app.get("/products/{id}", response_model=ProductRead)
def get_product(db: DbSession, id: int) -> Product:
    product = db.get(Product, id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )
    return product


@app.post(
    "/products", status_code=status.HTTP_201_CREATED, response_model=ProductCreate
)
def create_product(db: DbSession, product: ProductCreate):
    """Handles POST requests for /products endpoint and appends product for in-memory storage.

    Args:
        product (Product): A valid product.

    Returns:
        Status Code - 201 Created with sent data.
    """
    stmt = insert(Product).values(
        name=product.name,
        unit=product.unit,
        cost_per_unit=product.cost_per_unit,
        price_per_unit=product.price_per_unit,
        quantity_in_stock=product.quantity_in_stock,
    )

    db.execute(stmt)
    db.commit()

    return product
