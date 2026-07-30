from typing import Literal

from pydantic import BaseModel, Field


class TokenRead(BaseModel):
    access_token: str = Field(
        title="Access Token", description="The JWT for API access"
    )
    token_type: Literal["bearer"] = Field(
        title="Token Type", description='The token type (always "bearer")'
    )
