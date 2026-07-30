from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from models.product import Product, ProductCreate, ProductRead


def test_create_product(
    authenticated_client, seed_category, valid_category_kwargs, valid_product_kwargs
):
    product = ProductCreate.model_validate(valid_product_kwargs)
    response = authenticated_client.post(
        "/products", json=product.model_dump(mode="json")
    )
    assert response.status_code == 201
    product = ProductRead(**response.json())

    expected = valid_product_kwargs | {
        "id": product.id,
        "category": {
            "id": valid_product_kwargs["category_id"],
            "name": valid_category_kwargs["name"],
        },
    }
    del expected["category_id"]
    expected = ProductRead(**expected)

    assert product.model_dump(mode="json") == expected.model_dump(mode="json")


def test_create_product_with_invalid_payload_returns_422(
    authenticated_client, invalid_product_kwargs
):
    response = authenticated_client.post("/products", json=invalid_product_kwargs)
    assert response.status_code == 422


def test_view_products_all(unauthenticated_client, db_session, seed_product):
    products = db_session.query(Product).all()

    response = unauthenticated_client.get("/products")
    assert response.status_code == 200

    expected = [
        ProductRead.model_validate(p, from_attributes=True).model_dump(mode="json")
        for p in products
    ]
    assert response.json() == expected


@pytest.mark.parametrize(
    "name, unit, result",
    [
        (None, None, 1),
        ("pot", None, 1),
        ("basil", None, 0),
        ("pot", "each", 1),
        ("pot", "bag", 0),
    ],
)
def test_view_products_search(
    name, unit, result, unauthenticated_client, db_session, seed_product
):
    params = {}
    if name:
        params["name"] = name
    if unit:
        params["unit"] = unit

    response = unauthenticated_client.get("/products", params=params)
    assert len(response.json()) == result
    assert response.status_code == 200


def test_get_product_should_return_product(
    unauthenticated_client, db_session, seed_product
):
    product = db_session.scalars(select(Product)).first()
    response = unauthenticated_client.get(f"/products/{product.id}")
    product_json = ProductRead.model_validate(product).model_dump(mode="json")
    assert response.status_code == 200
    assert response.json() == product_json


def test_get_product_should_return_404_if_not_exists(
    unauthenticated_client, db_session
):
    response = unauthenticated_client.get(f"/products/1")
    assert response.status_code == 404


def test_db_check_returns_success(unauthenticated_client, seed_product):
    response = unauthenticated_client.get("/db-check")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "connected"
    assert body["product_count"] == 1


def test_db_check_does_not_leak_internals(unauthenticated_client, monkeypatch):
    def bad_query(*args, **kwargs):
        raise OperationalError(
            "Connection to server 10.0.0.2 failed", None, Exception()
        )

    monkeypatch.setattr(Session, "query", bad_query)
    response = unauthenticated_client.get("/db-check")

    assert response.status_code == 500
    assert "10.0.0.2" not in response.json()["detail"]


def test_delete_should_remove_product_from_all_endpoint_responses(
    authenticated_client, db_session, seed_product, first_existing_product
):
    eid = first_existing_product.id

    view_one_before = authenticated_client.get(f"/products/{eid}")
    search_query = view_one_before.json()["name"][:3]
    view_all_before = authenticated_client.get("/products")
    search_before = authenticated_client.get("/products", params={"name": search_query})

    response = authenticated_client.delete(f"/products/{eid}")
    assert response.status_code == 204

    view_one_after = authenticated_client.get(f"/products/{eid}")
    view_all_after = authenticated_client.get("/products")
    search_after = authenticated_client.get("/products", params={"name": search_query})

    assert view_one_after.status_code == 404
    assert len(view_all_before.json()) - 1 == len(view_all_after.json())
    assert len(search_before.json()) - 1 == len(search_after.json())


def test_delete_should_return_404_if_not_exists(
    authenticated_client, db_session, seed_product, unused_product_id
):
    response = authenticated_client.delete(f"/products/{unused_product_id}")
    assert response.status_code == 404


def test_delete_should_keep_product_in_database(
    authenticated_client, db_session, seed_product, first_existing_product
):
    get_response = authenticated_client.get(f"/products/{first_existing_product.id}")
    delete_response = authenticated_client.delete(
        f"/products/{first_existing_product.id}"
    )
    assert delete_response.status_code == 204
    product = db_session.get(Product, first_existing_product.id)
    assert product.name == get_response.json()["name"]


def test_update_should_update_product(
    authenticated_client, db_session, seed_product, first_existing_product
):
    request_body = ProductCreate.model_validate(first_existing_product)
    request_body.name = "12in Blue Ceramic Pot"
    put_response = authenticated_client.put(
        f"/products/{first_existing_product.id}",
        json=request_body.model_dump(mode="json"),
    )
    get_response = authenticated_client.get(f"/products/{first_existing_product.id}")

    assert put_response.status_code == 200
    assert get_response.json()["name"] == request_body.name


def test_update_should_return_404_if_not_exists(
    authenticated_client, db_session, valid_product_kwargs, unused_product_id
):
    request_body = ProductCreate(**(valid_product_kwargs))
    response = authenticated_client.put(
        f"/products/{unused_product_id}", json=request_body.model_dump(mode="json")
    )
    assert response.status_code == 404


def test_update_should_return_422_if_bad_input(
    authenticated_client,
    db_session,
    seed_product,
    first_existing_product,
):
    request_body = ProductCreate.model_validate(first_existing_product)
    request_body.cost_per_unit = Decimal("-5.0")
    response = authenticated_client.put(
        f"/products/{first_existing_product.id}",
        json=request_body.model_dump(mode="json"),
    )

    assert response.status_code == 422


def test_update_should_not_update_deleted_products(
    authenticated_client, db_session, seed_product, first_existing_product
):
    request_body = ProductCreate.model_validate(first_existing_product)
    request_body.name = "12in Blue Ceramic Pot"
    response = authenticated_client.delete(f"/products/{first_existing_product.id}")
    assert response.status_code == 204

    response = authenticated_client.put(
        f"/products/{first_existing_product.id}",
        json=request_body.model_dump(mode="json"),
    )
    assert response.status_code == 404
    product = db_session.get(Product, first_existing_product.id)
    assert product == first_existing_product
