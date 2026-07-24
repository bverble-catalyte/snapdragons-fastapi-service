from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints
from sqlalchemy import Identity, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ProductCreate(BaseModel):
    """Represents a product sold by the garden center.

    Attributes:
        name: The product name
        unit: The product's unit of sale (e.g. "each", "bag", "lb")
        cost_per_unit: Amount the garden center pays suppliers, in dollars per unit
        price_per_unit: Amount the garden center charges customers, in dollars per unit
        quantity_in_stock: Current amount of product in inventory, in stock units
    """

    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    unit: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    cost_per_unit: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    price_per_unit: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    quantity_in_stock: Annotated[Decimal, Field(ge=0)]


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
