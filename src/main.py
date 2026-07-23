from fastapi import FastAPI, status
from models.product import Product
from database import temp_storage

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}!"}

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    """Handles POST requests for /products endpoint and appends product for in-memory storage.

    Args:
        product: A valid product.
    
    Returns:
        Status Code - 201 Created with sent data.
    """
    temp_storage.append(product.model_dump())
    return product