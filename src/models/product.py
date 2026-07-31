from decimal import Decimal
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    StringConstraints,
    field_validator,
)
from sqlalchemy import Boolean, ForeignKey, Identity, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.category import Category, CategoryRead

PRODUCT_NAME_TITLE = "Product Name"
PRODUCT_NAME_DESC = "The product name"

PRODUCT_UNIT_TITLE = "Unit of Sale"
PRODUCT_UNIT_DESC = 'The product\'s unit of sale (e.g. "each", "bag", "lb")'

PRODUCT_COST_TITLE = "Cost Per Unit"
PRODUCT_COST_PER_UNIT_DESC = (
    "Amount the garden center pays suppliers, in dollars per unit"
)

PRODUCT_PRICE_TITLE = "Price Per Unit"
PRODUCT_PRICE_PER_UNIT_DESC = (
    "Amount the garden center charges customers, in dollars per unit"
)

PRODUCT_QUANTITY_TITLE = "Quantity In Stock"
PRODUCT_QUANTITY_IN_STOCK_DESC = (
    "Current amount of product in inventory, in stock units"
)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")
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
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class ProductBase(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = (
        Field(title=PRODUCT_NAME_TITLE, description=PRODUCT_NAME_DESC)
    )
    unit: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = (
        Field(title=PRODUCT_UNIT_TITLE, description=PRODUCT_UNIT_DESC)
    )
    cost_per_unit: Annotated[Decimal, Field(gt=0, decimal_places=2)] = Field(
        title=PRODUCT_COST_TITLE, description=PRODUCT_COST_PER_UNIT_DESC
    )
    price_per_unit: Annotated[Decimal, Field(gt=0, decimal_places=2)] = Field(
        title=PRODUCT_PRICE_TITLE, description=PRODUCT_PRICE_PER_UNIT_DESC
    )
    quantity_in_stock: Annotated[Decimal, Field(ge=0)] = Field(
        title=PRODUCT_QUANTITY_TITLE, description=PRODUCT_QUANTITY_IN_STOCK_DESC
    )


class ProductCreate(ProductBase):
    """
    Input schema for creating a new product.

    Does not include `id`, since this will be assigned on creation.
    """

    category_id: PositiveInt = Field(title="The product's category ID")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Basil Plant - 4in Pot",
                "unit": "each",
                "cost_per_unit": "1.75",
                "price_per_unit": "4.99",
                "quantity_in_stock": "40",
                "category_id": 1,
            }
        },
    )


class ProductReadWithoutCategory(ProductBase):
    """Represents a product without its parent category.

    Used where the product is already nested under its category, so
    repeating the category would just duplicate data the caller already has.
    """

    id: PositiveInt = Field(
        title="Product ID", description="The unique product identifier"
    )

    model_config = ConfigDict(from_attributes=True)


class ProductRead(ProductReadWithoutCategory):
    """Represents a product sold by the garden center."""

    category: CategoryRead = Field(
        title="The product category",
        description="The category this product belongs to",
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
                "category": {"id": 1, "name": "Pots and Planters"},
            }
        },
    )
