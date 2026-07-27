import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

import database
from main import app, get_db
from models import Product, ProductCreate, ProductRead


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def basil_plant_kwargs():
    return {
        "name": "Basil Plant - 4in Pot",
        "unit": "each",
        "cost_per_unit": "1.75",
        "price_per_unit": "4.99",
        "quantity_in_stock": "40",
    }


@pytest.fixture
def invalid_product_kwargs():
    return {
        "name": "Happy Plant Fertilizer",
        "unit": "bag",
        "cost_per_unit": "15.50",
        "price_per_unit": "20.99",
        "quantity_in_stock": "-5",
    }


def test_create_product(client, basil_plant_kwargs):
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


def test_create_product_with_invalid_payload_returns_422(
    client, invalid_product_kwargs
):
    response = client.post("/products", json=invalid_product_kwargs)
    assert response.status_code == 422


def test_view_products(client, basil_plant_kwargs, seed_product, db_session):
    products = db_session.query(Product).all()

    response = client.get("/products")
    assert response.status_code == 200

    expected = [
        ProductRead.model_validate(p, from_attributes=True).model_dump(mode="json")
        for p in products
    ]
    assert response.json() == expected


def test_get_product_should_return_product(client, db_session, seed_product):
    product = db_session.scalars(select(Product)).first()
    response = client.get(f"/products/{product.id}")
    product_json = ProductRead.model_validate(product).model_dump(mode="json")
    assert response.status_code == 200
    assert response.json() == product_json
