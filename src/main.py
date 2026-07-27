from contextlib import asynccontextmanager
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine, temp_storage
from models import Product, ProductCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on app startup (Only creates tables if they don't exist yet)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        # Perform a simple query to verify connection
        count = db.query(Product).count()
        return {"status": "connected", "product_count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}",
        )


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/products", response_model=List[ProductCreate])
def view_products():
    return temp_storage


@app.get("/products/search")
def search_products(
    name: Annotated[str, Query(description="The product name is required.")],
    unit: Annotated[str | None, Query(description="Optional product unit.")] = None,
):
    """Handles GET requests for /products/search by searching for matching products in-memory.

    Args:
        name (str): The product name.
        unit (str): The product's unit of sale; optional.

    Returns:
        A list of products with a matching name and unit.
    """

    # Helper: Normalizes the formatting of strings for search.
    def normalize(s: str) -> str:
        return "".join(s.lower().split())

    return [
        product
        for product in temp_storage
        if normalize(name) in normalize(product["name"])
        and (unit is None or product["unit"] == unit)
    ]


@app.post(
    "/products", status_code=status.HTTP_201_CREATED, response_model=ProductCreate
)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
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
