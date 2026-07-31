from decimal import Decimal

import pytest
from sqlalchemy import select

from models.product import Product, ProductCreate, ProductRead


def test_create_product_should_create_product(
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


def test_create_product_with_bad_input_should_return_422(
    authenticated_client, invalid_product_kwargs
):
    response = authenticated_client.post("/products", json=invalid_product_kwargs)
    assert response.status_code == 422


def test_view_products_should_return_all_products(
    unauthenticated_client, db_session, seed_product
):
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


def test_view_product_should_return_product(
    unauthenticated_client, db_session, seed_product
):
    product = db_session.scalars(select(Product)).first()
    response = unauthenticated_client.get(f"/products/{product.id}")
    product_json = ProductRead.model_validate(product).model_dump(mode="json")
    assert response.status_code == 200
    assert response.json() == product_json


def test_view_product_on_nonexistant_product_should_return_404(
    unauthenticated_client, db_session
):
    response = unauthenticated_client.get(f"/products/1")
    assert response.status_code == 404


def test_update_product_should_update_product(
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


def test_update_product_on_nonexistant_product_should_return_404(
    authenticated_client, db_session, valid_product_kwargs, unused_product_id
):
    request_body = ProductCreate(**(valid_product_kwargs))
    response = authenticated_client.put(
        f"/products/{unused_product_id}", json=request_body.model_dump(mode="json")
    )
    assert response.status_code == 404


def test_update_product_with_nonexistant_category_should_return_404(
    authenticated_client,
    db_session,
    seed_product,
    first_existing_product,
    unused_category_id,
):
    request_body = ProductCreate.model_validate(first_existing_product)
    request_body.category_id = unused_category_id
    response = authenticated_client.put(
        f"/products/{first_existing_product.id}",
        json=request_body.model_dump(mode="json"),
    )

    assert response.status_code == 404
    product = db_session.get(Product, first_existing_product.id)
    assert product.category_id == first_existing_product.category_id


def test_update_product_with_bad_input_should_return_422(
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


def test_update_product_should_not_update_deleted_products(
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


def test_delete_product_should_remove_product_from_all_endpoint_responses(
    authenticated_client, db_session, seed_product, first_existing_product
):
    pid = first_existing_product.id

    view_one_before = authenticated_client.get(f"/products/{pid}")
    search_query = view_one_before.json()["name"][:3]
    view_all_before = authenticated_client.get("/products")
    search_before = authenticated_client.get("/products", params={"name": search_query})

    response = authenticated_client.delete(f"/products/{pid}")
    assert response.status_code == 204

    view_one_after = authenticated_client.get(f"/products/{pid}")
    view_all_after = authenticated_client.get("/products")
    search_after = authenticated_client.get("/products", params={"name": search_query})

    assert view_one_after.status_code == 404
    assert len(view_all_before.json()) - 1 == len(view_all_after.json())
    assert len(search_before.json()) - 1 == len(search_after.json())


def test_delete_product_on_nonexistant_product_should_return_404(
    authenticated_client, db_session, seed_product, unused_product_id
):
    response = authenticated_client.delete(f"/products/{unused_product_id}")
    assert response.status_code == 404


def test_delete_product_should_keep_product_in_database(
    authenticated_client, db_session, seed_product, first_existing_product
):
    get_response = authenticated_client.get(f"/products/{first_existing_product.id}")
    delete_response = authenticated_client.delete(
        f"/products/{first_existing_product.id}"
    )
    assert delete_response.status_code == 204
    product = db_session.get(Product, first_existing_product.id)
    assert product.name == get_response.json()["name"]
