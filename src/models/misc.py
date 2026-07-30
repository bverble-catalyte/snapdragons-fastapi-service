from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


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
