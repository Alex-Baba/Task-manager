import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, BaseModel

class TaskTag(Base, BaseModel):
    __tablename__ = 'task_tags'

    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True)
