import pytest
from fastapi.testclient import TestClient

import database
from main import app
from models.product import Product

client = TestClient(app)


@pytest.fixture
def basil_plant_kwargs():
    return {
        "name": "Basil Plant - 4in Pot",
        "unit": "each",
        "cost_per_unit": "1.75",
        "price_per_unit": "4.99",
        "quantity_in_stock": "40",
    }


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_hello_name():
    response = client.get("/hello/Jimmie")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Jimmie!"}


def test_create_product(basil_plant_kwargs):
    response = client.post("/products", json=basil_plant_kwargs)
    assert response.status_code == 201
    data = response.json()
    assert (
        "name"
        and "unit"
        and "cost_per_unit"
        and "price_per_unit"
        and "quantity_in_stock" in data
    )
    assert isinstance(data["name"], str)


def test_view_products(monkeypatch, basil_plant_kwargs):
    products = [Product(**basil_plant_kwargs)]
    monkeypatch.setattr(database, "temp_storage", products)

    response = client.get("/products")
    assert response.status_code == 200

    expected = [p.model_dump(mode="json") for p in products]
    assert response.json() == expected
