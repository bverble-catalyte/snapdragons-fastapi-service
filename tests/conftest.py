import os
import subprocess
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from models import Base, Product

TEST_DB_NAME = "gardentest"
DATABASE_URL = f"postgresql://root:root@localhost/{TEST_DB_NAME}"


def create_test_database():
    env = os.environ.copy()
    env["PGPASSWORD"] = "root"
    subprocess.run(["createdb", "-U", "root", TEST_DB_NAME], env=env)


def destroy_test_database():
    env = os.environ.copy()
    env["PGPASSWORD"] = "root"
    subprocess.run(["dropdb", "-U", "root", TEST_DB_NAME], env=env)


@pytest.fixture(scope="session")
def db_engine(request):
    create_test_database()
    request.addfinalizer(destroy_test_database)

    engine = create_engine(DATABASE_URL)
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
def seed_product(db_session):
    product = Product(
        **{
            "name": "12in Terra Cotta Clay Pot",
            "unit": "each",
            "cost_per_unit": Decimal("5.00"),
            "price_per_unit": Decimal("8.75"),
            "quantity_in_stock": Decimal("55"),
        }
    )
    db_session.add(product)
    db_session.commit()
