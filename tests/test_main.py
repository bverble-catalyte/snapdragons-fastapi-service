from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_hello_name():
    response = client.get("/hello/Jimmie")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Jimmie!"}

def test_create_product():
    product_test = {"name": "Basil Plant - 4in Pot", "unit": "each", "cost_per_unit": 1.75, "price_per_unit": 4.99, "quantity_in_stock": 40}
    response = client.post("/products", json = product_test)
    assert response.status_code == 201
    data = response.json()
    assert "name" and "unit" and "cost_per_unit" and "price_per_unit" and "quantity_in_stock" in data
    assert isinstance(data["name"], str)