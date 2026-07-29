import os
import subprocess
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from config import settings
from models import Base, Product


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


@pytest.fixture()
def seed_product(db_session, valid_product_kwargs):
    product = Product(**valid_product_kwargs)
    db_session.add(product)
    db_session.commit()
