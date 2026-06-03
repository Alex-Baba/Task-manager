from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, List
from datetime import datetime

from .common import TimeStamp

from app.core.enums import PriorityEnum, Status


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    description: Optional[str] = None
    due_date: Optional[datetime] = None
    category_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None


class TaskCreate(TaskBase):
    title: str = Field(min_length=1)
    status: Status = Status.PENDING
    manual_priority: PriorityEnum = PriorityEnum.LOW

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_strings(cls, value):
        return value.strip() if isinstance(value, str) else value


class TaskUpdate(TaskBase):
    title: Optional[str] = Field(default=None, min_length=1)
    completed_at: Optional[datetime] = None
    status: Optional[Status] = None
    manual_priority: Optional[PriorityEnum] = None

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
    manual_priority: PriorityEnum
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    user_id: UUID
    category_id: Optional[UUID] = None
    tags: List[TagRead] = []
