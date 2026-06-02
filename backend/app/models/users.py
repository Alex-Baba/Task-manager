import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, BaseModel


class User(Base, BaseModel):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    tasks = relationship(
        "Task", back_populates="user", lazy="selectin", cascade="all, delete-orphan"
    )
    tags = relationship(
        "Tag", back_populates="user", lazy="selectin", cascade="all, delete-orphan"
    )
    admin_profile = relationship(
        "Admin",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        uselist=False,
    )
