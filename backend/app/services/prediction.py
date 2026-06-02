from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.ml.predictor import predict_task
from app.models.task_predictions import TaskPredictions
from app.repositories.prediction import PredictionRepository
from app.repositories.tasks import TaskRepository
from app.schemas.common import Message
from app.schemas.task_predictions import (
    PredictionCreate,
    PredictionUpdate,
    TaskPredictionRead,
)


class PredictionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PredictionRepository(session)
        self.task_repo = TaskRepository(session)

    async def _get_task_or_404(self, *, user_id: UUID, task_id: UUID):
        task = await self.task_repo.get_task_by_id(task_id)

        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return task

    async def _get_prediction_for_task_or_404(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
        prediction_id: UUID,
    ) -> TaskPredictions:
        await self._get_task_or_404(user_id=user_id, task_id=task_id)
        prediction = await self.repo.get_task_prediction_for_task_by_id(
            user_id=user_id,
            task_id=task_id,
            prediction_id=prediction_id,
        )

        if not prediction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prediction not found",
            )

        return prediction

    @staticmethod
    def build_prediction(*, payload: PredictionCreate) -> TaskPredictions:
        prediction = TaskPredictions()
        prediction.task_id = payload.task_id
        prediction.predicted_priority = payload.predicted_priority
        prediction.predicted_category = payload.predicted_category
        prediction.category_confidence = payload.category_confidence
        prediction.priority_confidence = payload.priority_confidence
        prediction.smart_score = payload.smart_score
        prediction.reasoning = payload.reasoning
        prediction.model_version = payload.model_version
        prediction.is_active = True

        return prediction

    async def generate_prediction_for_task(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
    ) -> TaskPredictionRead:
        task = await self._get_task_or_404(user_id=user_id, task_id=task_id)
        result = predict_task(task)
        payload = PredictionCreate(task_id=task_id, **result.model_dump())
        prediction = self.build_prediction(payload=payload)

        try:
            await self.repo.deactivate_all_task_predictions(
                user_id=user_id,
                task_id=task_id,
            )
            prediction = await self.repo.create_task_prediction(prediction)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return TaskPredictionRead.model_validate(prediction, from_attributes=True)

    async def get_active_prediction_for_task(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
    ) -> TaskPredictionRead:
        await self._get_task_or_404(user_id=user_id, task_id=task_id)

        prediction = await self.repo.get_active_prediction_for_task(
            user_id=user_id,
            task_id=task_id,
        )

        if not prediction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active prediction not found",
            )

        return TaskPredictionRead.model_validate(prediction, from_attributes=True)

    async def get_predictions_for_task(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
    ) -> list[TaskPredictionRead]:
        await self._get_task_or_404(user_id=user_id, task_id=task_id)
        predictions = await self.repo.get_predictions_for_task(
            user_id=user_id,
            task_id=task_id,
        )

        return [
            TaskPredictionRead.model_validate(prediction, from_attributes=True)
            for prediction in predictions
        ]

    async def update_prediction(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
        prediction_id: UUID,
        payload: PredictionUpdate,
    ) -> TaskPredictionRead:
        await self._get_prediction_for_task_or_404(
            user_id=user_id,
            task_id=task_id,
            prediction_id=prediction_id,
        )
        data = payload.model_dump(exclude_unset=True)

        try:
            if data.get("is_active") is True:
                await self.repo.deactivate_all_task_predictions(
                    user_id=user_id,
                    task_id=task_id,
                )

            prediction = await self.repo.update_task_prediction(
                user_id=user_id,
                task_id=task_id,
                prediction_id=prediction_id,
                **data,
            )
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return TaskPredictionRead.model_validate(prediction, from_attributes=True)

    async def activate_prediction(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
        prediction_id: UUID,
    ) -> TaskPredictionRead:
        await self._get_prediction_for_task_or_404(
            user_id=user_id,
            task_id=task_id,
            prediction_id=prediction_id,
        )

        try:
            await self.repo.deactivate_all_task_predictions(
                user_id=user_id,
                task_id=task_id,
            )
            prediction = await self.repo.activate_task_prediction(
                user_id=user_id,
                task_id=task_id,
                prediction_id=prediction_id,
            )
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return TaskPredictionRead.model_validate(prediction, from_attributes=True)

    async def delete_prediction(
        self,
        *,
        user_id: UUID,
        task_id: UUID,
        prediction_id: UUID,
    ) -> Message:
        await self._get_prediction_for_task_or_404(
            user_id=user_id,
            task_id=task_id,
            prediction_id=prediction_id,
        )

        try:
            await self.repo.delete_task_prediction(
                user_id=user_id,
                task_id=task_id,
                prediction_id=prediction_id,
            )
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return Message(message="Prediction deleted successfully")
