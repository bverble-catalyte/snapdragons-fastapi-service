from typing import Annotated, List

from fastapi import FastAPI, Query, status

from database import temp_storage
from models.product import Product

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/products", response_model=List[Product])
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


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    """Handles POST requests for /products endpoint and appends product for in-memory storage.

    Args:
        product (Product): A valid product.

    Returns:
        Status Code - 201 Created with sent data.
    """
    temp_storage.append(product.model_dump())
    return product
