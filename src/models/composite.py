from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, StringConstraints

from models.product import ProductRead

CATEGORY_NAME_TITLE = "Category Name"
CATEGORY_NAME_DESC = "The name of the category"


class CategoryReadWithProducts(BaseModel):
    id: PositiveInt = Field(
        title="Category ID", description="The unique category identifier"
    )
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] = (
        Field(title=CATEGORY_NAME_TITLE, description=CATEGORY_NAME_DESC)
    )
    products: Annotated[list[ProductRead], Field(min_length=0)]

    model_config = ConfigDict(from_attributes=True)
