from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from datetime import date

from .common import TimeStamp

class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[date] = None  # ISO format date string
    category_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None
    user_id: UUID

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_strings(cls, value):
        return value.strip() if isinstance(value, str) else value


class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[date] = None  # ISO format date string YYYY-MM-DDTHH:MM:SSZ
    category_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None
    status:Optional[str] = None

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_strings(cls, value):
        return value.strip() if isinstance(value, str) else value

class TagRead(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)

class TaskRead(TaskBase, TimeStamp):
    id: UUID
    user_id: UUID
    tags: List[TagRead]=[]