from typing import TYPE_CHECKING, Annotated, List

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, StringConstraints
from sqlalchemy import Boolean, Identity, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.product import Product

CATEGORY_NAME_TITLE = "Category Name"
CATEGORY_NAME_DESC = "The name of the category"


class CategoryCreate(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    products: Mapped[List["Product"]] = relationship(back_populates="category")
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
