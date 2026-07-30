from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from sqlalchemy import Identity, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    model_config = ConfigDict(from_attributes=True)


class UserCredentials(BaseModel):
    username: Annotated[str, StringConstraints(min_length=1)] = Field(
        title="Username", description="The username used for login"
    )
    password: Annotated[str, StringConstraints(min_length=1)] = Field(
        title="Password", description="The password used for login"
    )
