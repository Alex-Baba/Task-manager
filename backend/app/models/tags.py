import uuid
from sqlalchemy import CheckConstraint, Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, BaseModel


class Tag(Base, BaseModel):
    __tablename__ = "tags"

    # ensure that each user cannot have duplicate tag names but can have the same tag name as other users
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_tag_name"),
        CheckConstraint("length(trim(name)) > 0", name="ck_tags_name_not_empty"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # tasks relationship
    tasks = relationship(
        "Task", secondary="task_tags", back_populates="tags", lazy="selectin"
    )
    user = relationship("User", back_populates="tags", lazy="selectin")
