from decimal import Decimal

import pytest
from pydantic import ValidationError

from models import ProductCreate


def test_product_name_must_be_nonempty(valid_product_kwargs):
    valid_product_kwargs["name"] = ""
    with pytest.raises(ValidationError):
        ProductCreate(**valid_product_kwargs)


def test_product_unit_must_be_nonempty(valid_product_kwargs):
    valid_product_kwargs["unit"] = ""
    with pytest.raises(ValidationError):
        ProductCreate(**valid_product_kwargs)


def test_product_cost_per_unit_must_be_gt_zero(valid_product_kwargs):
    valid_product_kwargs["cost_per_unit"] = Decimal("0.0")
    with pytest.raises(ValidationError):
        ProductCreate(**valid_product_kwargs)


def test_product_price_per_unit_must_be_gt_zero(valid_product_kwargs):
    valid_product_kwargs["price_per_unit"] = Decimal("0.0")
    with pytest.raises(ValidationError):
        ProductCreate(**valid_product_kwargs)


def test_product_quantity_in_stock_must_be_gte_zero(valid_product_kwargs):
    valid_product_kwargs["quantity_in_stock"] = Decimal("-1")
    with pytest.raises(ValidationError):
        ProductCreate(**valid_product_kwargs)


def test_product_quantity_in_stock_may_equal_zero(valid_product_kwargs):
    valid_product_kwargs["quantity_in_stock"] = Decimal("0")
    ProductCreate(**valid_product_kwargs)
