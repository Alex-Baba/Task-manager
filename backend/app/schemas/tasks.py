from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

from .common import TimeStamp

class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[str] = None  # ISO format date string
    category_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[str] = None  # ISO format date string YYYY-MM-DDTHH:MM:SSZ
    category_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None

class TaskRead(TaskBase, TimeStamp):
    id: UUID
    user_id: UUID