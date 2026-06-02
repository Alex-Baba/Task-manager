import uuid
from sqlalchemy import (
    CheckConstraint,
    Column,
    String,
    DateTime,
    ForeignKey,
    Enum as SAEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.enums import Priority, Status
from .base import Base, BaseModel


class Task(Base, BaseModel):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("length(trim(title)) > 0", name="ck_tasks_title_not_empty"),
        CheckConstraint(
            """
            (
                status::text = 'COMPLETED'
                AND completed_at IS NOT NULL
            )
            OR
            (
                status::text <> 'COMPLETED'
                AND completed_at IS NULL
            )
            """,
            name="ck_tasks_completed_at_matches_status",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    status = Column(SAEnum(Status), default=Status.PENDING, nullable=False)
    manual_priority = Column(SAEnum(Priority), default=Priority.LOW, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship(
        "User",
        back_populates="tasks",
        lazy="selectin",
    )

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    category = relationship("Categories", back_populates="tasks", lazy="selectin")

    tags = relationship(
        "Tag", secondary="task_tags", back_populates="tasks", lazy="selectin"
    )

    predictions = relationship(
        "TaskPredictions",
        back_populates="task",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
