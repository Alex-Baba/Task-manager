import uuid
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    Enum as SAEnum,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.enums import CategoryEnum, PriorityEnum
from .base import Base, BaseModel


class TaskPredictions(Base, BaseModel):
    __tablename__ = "task_predictions"
    __table_args__ = (
        CheckConstraint(
            "category_confidence >= 0 AND category_confidence <= 1",
            name="ck_task_predictions_category_confidence_range",
        ),
        CheckConstraint(
            "priority_confidence >= 0 AND priority_confidence <= 1",
            name="ck_task_predictions_priority_confidence_range",
        ),
        CheckConstraint(
            "smart_score >= 0 AND smart_score <= 1",
            name="ck_task_predictions_smart_score_range",
        ),
        Index(
            "uq_active_prediction_per_task",
            "task_id",
            unique=True,
            postgresql_where=text("is_active = true"),
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    is_active = Column(Boolean, default=True, nullable=False)
    applied_category = Column(Boolean, default=False, nullable=False)
    applied_priority = Column(Boolean, default=False, nullable=False)
    applied_at = Column(DateTime(timezone=True), nullable=True)

    predicted_priority = Column(SAEnum(PriorityEnum), nullable=False)
    predicted_category = Column(SAEnum(CategoryEnum), nullable=False)

    category_confidence = Column(Float, default=0.0, nullable=False)
    priority_confidence = Column(Float, default=0.0, nullable=False)

    smart_score = Column(Float, nullable=False)
    reasoning = Column(JSONB, nullable=True)

    model_version = Column(String(50), nullable=True)

    task = relationship(
        "Task",
        back_populates="predictions",
        lazy="selectin",
    )
