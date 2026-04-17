import uuid
from enum import Enum
from sqlalchemy import Column, String, Enum as SAEnum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, BaseModel


class Category(str,Enum):
    WORK = 'WORK'
    PERSONAL = 'PERSONAL'
    SHOPPING = 'SHOPPING'
    HEALTH = 'HEALTH'
    FINANCE = 'FINANCE'
    EDUCATION = 'EDUCATION'
    ENTERTAINMENT = 'ENTERTAINMENT'
    OTHER = 'OTHER'


class Categories(Base, BaseModel):
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(SAEnum(Category), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    # tasks relationship
    tasks = relationship('Task', back_populates='category', lazy='selectin')