from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional

from .common import TimeStamp

class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None

class CategoryRead(CategoryBase, TimeStamp):
    id: UUID