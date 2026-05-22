import uuid
from enum import Enum
from sqlalchemy import Column, ForeignKey, String, Float, Enum as SAEnum, Boolean
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import relationship
from .base import Base, BaseModel

class CategoryEnum(str,Enum):
    WORK = 'WORK'
    PERSONAL = 'PERSONAL'
    SHOPPING = 'SHOPPING'
    HEALTH = 'HEALTH'
    FINANCE = 'FINANCE'
    EDUCATION = 'EDUCATION'
    ENTERTAINMENT = 'ENTERTAINMENT'
    OTHER = 'OTHER'

class PriorityEnum(str, Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

class TaskPredictions(Base, BaseModel):
    __tablename__ = 'task_predictions'

    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id=Column(UUID(as_uuid=True), ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False,index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    predicted_priority=Column(SAEnum(PriorityEnum), nullable=False)
    predicted_category=Column(SAEnum(CategoryEnum), nullable=False)

    category_confidence=Column(Float,default=0.0, nullable=False)
    priority_confidence=Column(Float,default=0.0, nullable=False)

    smart_score=Column(Float, nullable=False)
    reasoning=Column(JSONB, nullable=True)

    model_version=Column(String(50), nullable=True)


    task=relationship('Task', back_populates='predictions', lazy='selectin')