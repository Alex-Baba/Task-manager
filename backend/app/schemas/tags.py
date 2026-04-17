from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional

class TagBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None

class TagRead(TagBase):
    id: UUID