from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

from .common import TimeStamp

class TagBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: str = Field(min_length=1)

class TagCreate(TagBase):
    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value):
        if not value:
            raise ValueError("Tag name cannot be empty")
        return value

class TagUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(default=None, min_length=1)

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, value):
        return value.strip() if isinstance(value, str) else value

class TagRead(TagBase, TimeStamp):
    id: UUID
    user_id:UUID
