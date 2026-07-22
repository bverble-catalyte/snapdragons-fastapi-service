from fastapi import FastAPI, status
from models.product import Product

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}!"}

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    """Sends a POST request for /products endpoint.

    Args:
        product: A valid product.
    
    Returns:
        Status Code - 201 Created with sent data.
    """
    return product