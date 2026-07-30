from decimal import Decimal
from typing import Annotated, List, Literal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, StringConstraints
from sqlalchemy import Boolean, ForeignKey, Identity, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

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

CATEGORY_NAME_TITLE = "Category Name"
CATEGORY_NAME_DESC = "The name of the category"


class CategoryCreate(BaseModel):
    id: PositiveInt = Field(
        title="Category ID", description="The unique category identifier"
    )
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = (
        Field(title=CATEGORY_NAME_TITLE, description=CATEGORY_NAME_DESC)
    )


class CategoryRead(BaseModel):
    id: PositiveInt = Field(
        title="Category ID", description="The unique category identifier"
    )
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = (
        Field(title=CATEGORY_NAME_TITLE, description=CATEGORY_NAME_DESC)
    )


class CategoryReadWithProducts(BaseModel):
    id: PositiveInt = Field(
        title="Category ID", description="The unique category identifier"
    )
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = (
        Field(title=CATEGORY_NAME_TITLE, description=CATEGORY_NAME_DESC)
    )
    products: Annotated[list[ProductRead], Field(min_length=0)]


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    products: Mapped[List["Product"]] = relationship(back_populates="category")


class ProductCreate(BaseModel):
    """
    Input schema for creating a new product.

    Does not include `id`, since this will be assigned on creation.
    """

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


class ProductRead(BaseModel):
    """Represents a product sold by the garden center."""

    id: PositiveInt = Field(
        title="Product ID", description="The unique product identifier"
    )
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
        title=PRODUCT_UNIT_TITLE, description=PRODUCT_PRICE_PER_UNIT_DESC
    )
    quantity_in_stock: Annotated[Decimal, Field(ge=0)] = Field(
        title=PRODUCT_QUANTITY_TITLE, description=PRODUCT_QUANTITY_IN_STOCK_DESC
    )
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


class DatabaseStatus(BaseModel):
    status: str = Field(title="Status", description="Database connection status")
    product_count: int = Field(
        title="Product Count", description="The number of rows in the product table"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "connected",
                "product_count": 1,
            }
        }
    )


class UserCredentials(BaseModel):
    username: Annotated[str, StringConstraints(min_length=1)] = Field(
        title="Username", description="The username used for login"
    )
    password: Annotated[str, StringConstraints(min_length=1)] = Field(
        title="Password", description="The password used for login"
    )


class TokenRead(BaseModel):
    access_token: str = Field(
        title="Access Token", description="The JWT for API access"
    )
    token_type: Literal["bearer"] = Field(
        title="Token Type", description='The token type (always "bearer")'
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    model_config = ConfigDict(from_attributes=True)
