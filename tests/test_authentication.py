from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

import database
from main import app, get_db
from models import Product, ProductCreate, ProductRead, TokenRead, UserCredentials


def test_create_token_should_issue_token_on_valid_credentials(
    unauthenticated_client, seed_users, manager_valid_credentials
):
    response = unauthenticated_client.post(
        "/tokens", json=manager_valid_credentials.model_dump(mode="json")
    )
    assert response.status_code == 201

    token = TokenRead(**response.json())
    assert token.token_type == "bearer"
    assert len(token.access_token) > 0


def test_create_token_should_throw_401_on_invalid_credentials(
    unauthenticated_client, seed_users, manager_invalid_credentials
):
    response = unauthenticated_client.post(
        "/tokens", json=manager_invalid_credentials.model_dump(mode="json")
    )
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json()["detail"] == "Invalid username or password"


def test_create_product_requires_authentication(
    unauthenticated_client, valid_product_kwargs
):
    product = ProductCreate(**valid_product_kwargs)
    response = unauthenticated_client.post(
        "/products", json=product.model_dump(mode="json")
    )
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json()["detail"] == "Not authenticated"


def test_update_product_requires_authentication(
    unauthenticated_client, seed_product, valid_product_kwargs, first_existing_product
):
    request_body = ProductCreate.model_validate(first_existing_product)
    request_body.name = "12in Blue Ceramic Pot"
    response = unauthenticated_client.put(
        f"/products/{first_existing_product.id}",
        json=request_body.model_dump(mode="json"),
    )

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json()["detail"] == "Not authenticated"


def test_delete_product_requires_authentication(
    unauthenticated_client, seed_product, first_existing_product
):
    response = unauthenticated_client.delete(f"/products/{first_existing_product.id}")
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json()["detail"] == "Not authenticated"
