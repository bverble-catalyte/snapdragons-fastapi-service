from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, StringConstraints
from sqlalchemy import Identity, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

NAME_TITLE = "Product Name"
NAME_DESC = "The product name"

UNIT_TITLE = "Unit of Sale"
UNIT_DESC = 'The product\'s unit of sale (e.g. "each", "bag", "lb")'

COST_TITLE = "Cost Per Unit"
COST_PER_UNIT_DESC = "Amount the garden center pays suppliers, in dollars per unit"

PRICE_TITLE = "Price Per Unit"
PRICE_PER_UNIT_DESC = "Amount the garden center charges customers, in dollars per unit"

QUANTITY_TITLE = "Quantity In Stock"
QUANTITY_IN_STOCK_DESC = "Current amount of product in inventory, in stock units"


class ProductCreate(BaseModel):
    """
    Input schema for creating a new product.

    Does not include `id`, since this will be assigned on creation.
    """

    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = (
        Field(title=NAME_TITLE, description=NAME_DESC)
    )
    unit: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = (
        Field(title=UNIT_TITLE, description=UNIT_DESC)
    )
    cost_per_unit: Annotated[Decimal, Field(gt=0, decimal_places=2)] = Field(
        title=COST_TITLE, description=COST_PER_UNIT_DESC
    )
    price_per_unit: Annotated[Decimal, Field(gt=0, decimal_places=2)] = Field(
        title=PRICE_TITLE, description=PRICE_PER_UNIT_DESC
    )
    quantity_in_stock: Annotated[Decimal, Field(ge=0)] = Field(
        title=QUANTITY_TITLE, description=QUANTITY_IN_STOCK_DESC
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Basil Plant - 4in Pot",
                "unit": "each",
                "cost_per_unit": "1.75",
                "price_per_unit": "4.99",
                "quantity_in_stock": "40",
            }
        }
    )


class ProductRead(BaseModel):
    """Represents a product sold by the garden center."""

    id: PositiveInt = Field(
        title="Product ID", description="The unique product identifier"
    )
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = (
        Field(title=NAME_TITLE, description=NAME_DESC)
    )
    unit: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = (
        Field(title=UNIT_TITLE, description=UNIT_DESC)
    )
    cost_per_unit: Annotated[Decimal, Field(gt=0, decimal_places=2)] = Field(
        title=COST_TITLE, description=COST_PER_UNIT_DESC
    )
    price_per_unit: Annotated[Decimal, Field(gt=0, decimal_places=2)] = Field(
        title=UNIT_TITLE, description=PRICE_PER_UNIT_DESC
    )
    quantity_in_stock: Annotated[Decimal, Field(ge=0)] = Field(
        title=QUANTITY_TITLE, description=QUANTITY_IN_STOCK_DESC
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Basil Plant - 4in Pot",
                "unit": "each",
                "cost_per_unit": "1.75",
                "price_per_unit": "4.99",
                "quantity_in_stock": "40",
            }
        },
    )


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    unit: Mapped[str] = mapped_column(nullable=False)
    cost_per_unit: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2), nullable=False
    )
    price_per_unit: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2), nullable=False
    )
    quantity_in_stock: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2), nullable=False
    )
