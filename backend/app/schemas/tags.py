from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

from .common import TimeStamp

class TagBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

class TagCreate(TagBase):
    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, value):
        return value.strip() if isinstance(value, str) else value

class TagUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, value):
        return value.strip() if isinstance(value, str) else value

class TagRead(TagBase, TimeStamp):
    id: UUID