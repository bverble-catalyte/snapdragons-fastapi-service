from decimal import Decimal

import pytest
from pydantic import ValidationError

from models.product import Product


@pytest.fixture()
def valid_product_kwargs():
    return {
        "name": "12in Terra Cotta Clay Pot",
        "unit": "each",
        "cost_per_unit": Decimal("5.00"),
        "price_per_unit": Decimal("8.75"),
        "quantity_in_stock": Decimal("55"),
    }


def test_product_name_must_be_nonempty(valid_product_kwargs):
    valid_product_kwargs["name"] = ""
    with pytest.raises(ValidationError):
        Product(**valid_product_kwargs)


def test_product_unit_must_be_nonempty(valid_product_kwargs):
    valid_product_kwargs["unit"] = ""
    with pytest.raises(ValidationError):
        Product(**valid_product_kwargs)


def test_product_cost_per_unit_must_be_gt_zero(valid_product_kwargs):
    valid_product_kwargs["cost_per_unit"] = Decimal("0.0")
    with pytest.raises(ValidationError):
        Product(**valid_product_kwargs)


def test_product_price_per_unit_must_be_gt_zero(valid_product_kwargs):
    valid_product_kwargs["price_per_unit"] = Decimal("0.0")
    with pytest.raises(ValidationError):
        Product(**valid_product_kwargs)


def test_product_quantity_in_stock_must_be_gte_zero(valid_product_kwargs):
    valid_product_kwargs["quantity_in_stock"] = Decimal("-1")
    with pytest.raises(ValidationError):
        Product(**valid_product_kwargs)


def test_product_quantity_in_stock_may_equal_zero(valid_product_kwargs):
    valid_product_kwargs["quantity_in_stock"] = Decimal("0")
    Product(**valid_product_kwargs)
