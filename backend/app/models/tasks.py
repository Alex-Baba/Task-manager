import uuid
from enum import Enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, BaseModel

class Status(str,Enum):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

class Priority(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

class Task(Base, BaseModel):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    status = Column(SAEnum(Status), default=Status.PENDING, nullable=False)
    manual_priority= Column(SAEnum(Priority), default=Priority.LOW, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='tasks', lazy='selectin',)
    
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=True)
    category = relationship('Categories', back_populates='tasks', lazy='selectin')

    tags = relationship('Tag', secondary='task_tags', back_populates='tasks', lazy='selectin')

    predictions= relationship('Prediction', back_populates='tasks',cascade="all, delete-orphan", lazy='selectin')