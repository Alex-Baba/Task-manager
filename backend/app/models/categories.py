import uuid
from sqlalchemy import Column, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.enums import CategoryEnum
from .base import Base, BaseModel


class Categories(Base, BaseModel):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(SAEnum(CategoryEnum, name="category"), unique=True, nullable=False)

    # tasks relationship
    tasks = relationship("Task", back_populates="category", lazy="selectin")
