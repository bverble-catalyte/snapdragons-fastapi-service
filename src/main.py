from contextlib import asynccontextmanager
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine, temp_storage
from models import Product, ProductCreate, ProductRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
temp_storage = []


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def normalize(s: str) -> str:
    """Normalizes the formatting of strings for search.

    Args:
        s (str): The string to be reformatted.

    Returns:
        A normalized string for search.
    """
    return "".join(s.lower().split())


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
def view_products(db: Session = Depends(get_db)):
    """Views all products within the database.

    Args:
        db (Session): The database session.

    Returns:
        A list of products in the database.
    """
    products = db.query(Product).all()
    return products


@app.get("/products/{id}", response_model=ProductRead)
def get_product(id: int, session=Depends(get_db)) -> Product:
    product = session.get(Product, id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found",
        )
    return product


@app.get("/products/search")
def search_products(
    name: Annotated[str, Query(description="The product name is required.")],
    unit: Annotated[str | None, Query(description="Optional product unit.")] = None,
    db: Session = Depends(get_db),
):
    """Searches the database for products with matching name and unit.

    Args:
        name (str): The product name.
        unit (str): The product's unit of sale; optional.
        db (Session): The database session.

    Returns:
        A list of products with a matching name and unit.
    """

    return [
        db.query(Product).filter(
            normalize(name) in normalize(Product.name)
            and (unit is None or Product.unit == unit)
        )
    ]
    # return [
    #     product
    #     for product in temp_storage
    #     if normalize(name) in normalize(product["name"])
    #     and (unit is None or product["unit"] == unit)
    # ]


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
