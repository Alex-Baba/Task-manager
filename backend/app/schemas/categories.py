from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.core.enums import Category

from .common import TimeStamp


class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Category


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[Category] = None


class CategoryRead(CategoryBase, TimeStamp):
    id: UUID
