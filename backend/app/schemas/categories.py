from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None

class CategoryRead(CategoryBase):
    id: UUID