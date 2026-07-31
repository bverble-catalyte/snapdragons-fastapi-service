from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session


def test_db_check_should_return_success(unauthenticated_client, seed_product):
    response = unauthenticated_client.get("/db-check")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "connected"
    assert body["product_count"] == 1


def test_db_check_should_not_leak_internals(unauthenticated_client, monkeypatch):
    def bad_query(*args, **kwargs):
        raise OperationalError(
            "Connection to server 10.0.0.2 failed", None, Exception()
        )

    monkeypatch.setattr(Session, "query", bad_query)
    response = unauthenticated_client.get("/db-check")

    assert response.status_code == 500
    assert "10.0.0.2" not in response.json()["detail"]
