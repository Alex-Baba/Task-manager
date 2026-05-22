from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task
from app.models.task_predictions import TaskPredictions


class PredictionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task_prediction(
        self,
        task_prediction: TaskPredictions,
    ) -> TaskPredictions:
        self.session.add(task_prediction)
        await self.session.flush()
        return task_prediction

    async def get_task_prediction_by_id(
        self,
        user_id: UUID,
        prediction_id: UUID,
    ) -> TaskPredictions | None:
        stmt = (
            select(TaskPredictions)
            .join(Task, Task.id == TaskPredictions.task_id)
            .where(
                TaskPredictions.id == prediction_id,
                Task.user_id == user_id,
            )
        )

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_active_prediction_for_task(
        self,
        user_id: UUID,
        task_id: UUID,
    ) -> TaskPredictions | None:
        stmt = (
            select(TaskPredictions)
            .join(Task, Task.id == TaskPredictions.task_id)
            .where(
                TaskPredictions.task_id == task_id,
                Task.user_id == user_id,
                TaskPredictions.is_active.is_(True),
            )
        )

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_predictions_for_task(
        self,
        user_id: UUID,
        task_id: UUID,
    ) -> list[TaskPredictions]:
        stmt = (
            select(TaskPredictions)
            .join(Task, Task.id == TaskPredictions.task_id)
            .where(
                TaskPredictions.task_id == task_id,
                Task.user_id == user_id,
            )
            .order_by(TaskPredictions.created_at.desc())
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_task_prediction(
            self,
            user_id: UUID,
            prediction_id: UUID,
            **values,
    ) -> TaskPredictions | None:
        values = {
            key: value
            for key, value in values.items()
            if value is not None
        }

        if not values:
            return await self.get_task_prediction_by_id(user_id, prediction_id)

        stmt = (
            update(TaskPredictions)
            .where(
                TaskPredictions.id == prediction_id,
                TaskPredictions.task_id.in_(
                    select(Task.id).where(Task.user_id == user_id)
                ),
            )
            .values(**values)
            .returning(TaskPredictions)
        )

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def activate_task_prediction(
        self,
        user_id: UUID,
        prediction_id: UUID,
    ) -> TaskPredictions | None:
        stmt = (
            update(TaskPredictions)
            .where(
                TaskPredictions.id == prediction_id,
                TaskPredictions.task_id.in_(
                    select(Task.id).where(Task.user_id == user_id)
                ),
            )
            .values(is_active=True)
            .returning(TaskPredictions)
        )

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def deactivate_task_prediction(
        self,
        user_id: UUID,
        prediction_id: UUID,
    ) -> TaskPredictions | None:
        stmt = (
            update(TaskPredictions)
            .where(
                TaskPredictions.id == prediction_id,
                TaskPredictions.task_id.in_(
                    select(Task.id).where(Task.user_id == user_id)
                ),
            )
            .values(is_active=False)
            .returning(TaskPredictions)
        )

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def deactivate_all_task_predictions(
        self,
        user_id: UUID,
        task_id: UUID,
    ) -> list[TaskPredictions]:
        stmt = (
            update(TaskPredictions)
            .where(
                TaskPredictions.task_id == task_id,
                TaskPredictions.task_id.in_(
                    select(Task.id).where(Task.user_id == user_id)
                ),
                TaskPredictions.is_active.is_(True),
            )
            .values(is_active=False)
            .returning(TaskPredictions)
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete_task_prediction(
        self,
        user_id: UUID,
        prediction_id: UUID,
    ) -> bool:
        stmt = (
            delete(TaskPredictions)
            .where(
                TaskPredictions.id == prediction_id,
                TaskPredictions.task_id.in_(
                    select(Task.id).where(Task.user_id == user_id)
                ),
            )
        )

        result = await self.session.execute(stmt)
        return result.rowcount > 0