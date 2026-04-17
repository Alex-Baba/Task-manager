from uuid import UUID
from pydantic import BaseModel, ConfigDict

class TaskTagBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task_id: UUID
    tag_id: UUID

class TaskTagCreate(TaskTagBase):
    pass

class TaskTagRead(TaskTagBase):
    id: UUID