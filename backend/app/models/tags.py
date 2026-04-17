import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, BaseModel

class Tag(Base, BaseModel):
    __tablename__ = 'tags'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)

    # tasks relationship
    tasks = relationship('Task', secondary='task_tags', back_populates='tags', lazy='selectin')