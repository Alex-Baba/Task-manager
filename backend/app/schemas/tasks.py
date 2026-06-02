from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime

from .common import TimeStamp

from app.core.enums import Priority, Status

class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    description: Optional[str] = None
    due_date: Optional[datetime] = None
    category_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None


class TaskCreate(TaskBase):
    title: str
    status: Status = Status.PENDING
    manual_priority: Priority = Priority.LOW

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_strings(cls, value):
        return value.strip() if isinstance(value, str) else value


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    completed_at: Optional[datetime] = None
    status: Optional[Status] = None
    manual_priority: Optional[Priority] = None

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_strings(cls, value):
        return value.strip() if isinstance(value, str) else value


class TagRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class TaskRead(TimeStamp):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: Optional[str] = None
    status: Status
    manual_priority: Priority
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    user_id: UUID
    category_id: Optional[UUID] = None
    tags: List[TagRead] = []
