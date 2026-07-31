from sqlalchemy import select

from models.category import Category, CategoryCreate, CategoryRead


def test_create_category_should_create_category(
    authenticated_client, valid_category_kwargs
):
    response = authenticated_client.post("/categories", json=valid_category_kwargs)
    assert response.status_code == 201
    category = CategoryRead(**response.json())
    for field, value in valid_category_kwargs.items():
        assert value == getattr(category, field)


def test_create_category_with_bad_input_should_return_422(
    authenticated_client, invalid_category_kwargs
):
    response = authenticated_client.post("/categories", json=invalid_category_kwargs)
    assert response.status_code == 422


def test_view_categories_should_return_all_categories(
    unauthenticated_client, db_session, seed_category
):
    categories = db_session.query(Category).all()
    response = unauthenticated_client.get("/categories")
    assert len(categories) == len(response.json())


def test_view_category_should_return_category(
    db_session, seed_category, unauthenticated_client
):
    category = db_session.scalars(select(Category)).first()
    response = unauthenticated_client.get(f"/categories/{category.id}")
    category_json = CategoryRead.model_validate(category).model_dump(mode="json")
    assert response.status_code == 200
    assert response.json() == category_json


def test_view_category_on_nonexistant_category_should_return_404(
    unauthenticated_client,
):
    response = unauthenticated_client.get(f"/products/1")
    assert response.status_code == 404


def test_update_category_should_update_category(
    authenticated_client, first_existing_category
):
    request_body = CategoryCreate(name="Pots, Planters, and More")
    put_response = authenticated_client.put(
        f"/categories/{first_existing_category.id}",
        json=request_body.model_dump(mode="json"),
    )
    get_response = authenticated_client.get(f"/categories/{first_existing_category.id}")

    assert put_response.status_code == 200
    assert get_response.json()["name"] == request_body.name


def test_update_category_on_nonexistant_category_should_return_404(
    authenticated_client, db_session, valid_category_kwargs, unused_category_id
):
    request_body = CategoryCreate(**valid_category_kwargs)
    response = authenticated_client.put(
        f"/categories/{unused_category_id}", json=request_body.model_dump(mode="json")
    )
    assert response.status_code == 404


def test_update_category_with_bad_input_should_return_422(
    authenticated_client,
    db_session,
    first_existing_category,
):
    request_body = CategoryCreate.model_construct(name="")
    response = authenticated_client.put(
        f"/categories/{first_existing_category.id}",
        json=request_body.model_dump(mode="json"),
    )

    assert response.status_code == 422


def test_update_category_should_not_update_deleted_categories(
    authenticated_client, db_session, first_existing_category
):
    response = authenticated_client.delete(f"/categories/{first_existing_category.id}")
    assert response.status_code == 204

    request_body = CategoryCreate.model_validate(
        CategoryRead.model_validate(first_existing_category), from_attributes=True
    )
    request_body.name = "Pots, Planters, and More"
    response = authenticated_client.put(
        f"/categories/{first_existing_category.id}",
        json=request_body.model_dump(mode="json"),
    )
    assert response.status_code == 404
    category = db_session.get(Category, first_existing_category.id)
    assert category == first_existing_category


def test_delete_category_should_remove_category_from_all_endpoint_responses(
    authenticated_client, first_existing_category
):
    cid = first_existing_category.id

    view_one_before = authenticated_client.get(f"/categories/{cid}")
    view_all_before = authenticated_client.get("/categories")

    response = authenticated_client.delete(f"/categories/{cid}")
    assert response.status_code == 204

    view_one_after = authenticated_client.get(f"/categories/{cid}")
    view_all_after = authenticated_client.get("/categories")

    assert view_one_after.status_code == 404
    assert len(view_all_before.json()) - 1 == len(view_all_after.json())


def test_delete_category_on_nonexistant_category_should_return_404(
    authenticated_client, unused_category_id
):
    response = authenticated_client.delete(f"/categories/{unused_category_id}")
    assert response.status_code == 404


def test_delete_category_with_associated_products_should_return_409(
    authenticated_client, unused_category_id, first_existing_category
):
    response = authenticated_client.delete(f"/categories/{first_existing_category.id}")
    assert response.status_code == 409


def test_delete_category_should_keep_category_in_database(
    authenticated_client, db_session, first_existing_category
):
    get_response = authenticated_client.get(f"/categories/{first_existing_category.id}")
    delete_response = authenticated_client.delete(
        f"/categories/{first_existing_category.id}"
    )
    assert delete_response.status_code == 204
    category = db_session.get(Category, first_existing_category.id)
    assert category.name == get_response.json()["name"]
