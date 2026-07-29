import os
import subprocess
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import sessionmaker

from config import settings
from main import app, get_current_user, get_db
from models import Base, Product, User, UserCredentials


def create_test_database(db_name: str) -> None:
    env = os.environ.copy()
    env["PGPASSWORD"] = "root"
    subprocess.run(
        ["createdb", "-U", "root", "-h", "localhost", "-p", "5432", db_name],
        env=env,
        check=True,
    )


def destroy_test_database(db_name: str) -> None:
    env = os.environ.copy()
    env["PGPASSWORD"] = "root"
    subprocess.run(
        ["dropdb", "-U", "root", "-h", "localhost", "-p", "5432", db_name],
        env=env,
        check=True,
    )


@pytest.fixture(scope="session")
def db_engine(request):
    db_name = settings._test_db_name
    db_url = settings.test_database_url(db_name)
    create_test_database(db_name)
    request.addfinalizer(lambda: destroy_test_database(db_name))

    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def valid_product_kwargs():
    return {
        "name": "12in Terra Cotta Clay Pot",
        "unit": "each",
        "cost_per_unit": Decimal("5.00"),
        "price_per_unit": Decimal("8.75"),
        "quantity_in_stock": Decimal("55"),
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


@pytest.fixture()
def seed_product(db_session, valid_product_kwargs):
    product = Product(**valid_product_kwargs)
    db_session.add(product)
    db_session.commit()


@pytest.fixture
def first_existing_product(db_session, seed_product):
    return db_session.scalars(select(Product)).first()


@pytest.fixture()
def unused_product_id(db_session, seed_product):
    max_id = db_session.scalar(select(func.max(Product.id))) or 0
    return max_id + 1


@pytest.fixture
def manager_valid_credentials():
    return UserCredentials(
        **{
            "username": "manager",
            "password": "admin",
        }
    )


@pytest.fixture
def manager_invalid_credentials():
    return UserCredentials(
        **{
            "username": "manager",
            "password": "incorrect",
        }
    )


@pytest.fixture
def manager_user():
    return User(
        username="manager",
        # generate an example password hash in Python:
        #   from pwdlib import PasswordHash
        #   PasswordHash.recommended().hash("password")
        # password == "admin"
        password_hash="$argon2id$v=19$m=65536,t=3,p=4$cZwzIBCPEaSFju3XYSXT2Q$Tt3jLTrMTyb+hafu05PHSv2eZbv3YYh5kzmkrlDktR8",
    )


@pytest.fixture()
def seed_users(db_session, manager_user):
    user = manager_user
    db_session.add(user)
    db_session.commit()


@pytest.fixture()
def unauthenticated_client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture
def authenticated_client(unauthenticated_client, manager_user, seed_users):
    app.dependency_overrides[get_current_user] = lambda: manager_user
    yield unauthenticated_client
    del app.dependency_overrides[get_current_user]
