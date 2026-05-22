from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from typing import Any

from app.models.task_predictions import CategoryEnum,PriorityEnum

from .common import TimeStamp

class PredictionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    predicted_priority: PriorityEnum
    predicted_category: CategoryEnum

    category_confidence: float=Field(ge=0,le=1)
    priority_confidence: float=Field(ge=0,le=1)

    smart_score:float=Field(ge=0,le=1)
    reasoning: dict[str, Any] | None = None
    model_version: str | None = None

class PredictionCreate(PredictionBase):
    task_id: UUID

class PredictionUpdate(BaseModel):

    predicted_priority: PriorityEnum | None = None
    predicted_category: CategoryEnum | None = None

    category_confidence: float | None = Field(default=None, ge=0, le=1)
    priority_confidence: float | None = Field(default=None, ge=0, le=1)

    smart_score: float | None = Field(default=None, ge=0, le=1)
    reasoning: dict[str, Any] | None = None
    model_version: str | None = None
    is_active: bool | None = None

class PredictionResult(PredictionBase):
    pass

class TaskPredictionRead(PredictionBase,TimeStamp):
    id: UUID
    task_id: UUID
    is_active: bool