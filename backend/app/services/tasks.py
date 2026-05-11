from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task
from app.repositories.tasks import TaskRepository
from app.schemas.tasks import TaskCreate,TaskRead, TaskUpdate
from app.schemas.common import Message

class TaskService:
    def __init__(self,session: AsyncSession):
        self.session = session
        self.repo = TaskRepository(session)

    @staticmethod
    def build_task(*,payload: TaskCreate) -> Task:
        task = Task()
        task.title = payload.title
        task.description = payload.description
        task.user_id = payload.user_id
        task.due_date = payload.due_date

        return task

    @staticmethod
    def build_update_task(*,payload: TaskUpdate) -> dict:
        data=payload.model_dump(exclude_unset=True)
        return data

    async def save_task(self,*,payload: TaskCreate) -> TaskRead:
        task = self.build_task(payload=payload)
        try:
            task=await self.repo.create_task(task)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return TaskRead.model_validate(task,from_attributes=True)

    async def get_task(self,*,task_id: UUID) -> TaskRead:
        task=await self.repo.get_task_by_id(task_id)
        if not task:
            raise Exception
        return TaskRead.model_validate(task,from_attributes=True)

    async def get_all_tasks_by_user_id(self,*,user_id: UUID) -> list[TaskRead]:
        tasks=await self.repo.get_tasks_by_user_id(user_id)
        return [TaskRead.model_validate(task,from_attributes=True) for task in tasks]

    async def update_task(self,*,task_id: UUID,payload: TaskUpdate) -> TaskRead:
        data=self.build_update_task(payload=payload)
        try:
            updated=await self.repo.update_task(task_id=task_id, **data)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return TaskRead.model_validate(updated,from_attributes=True)

    async def delete_task(self,*,task_id: UUID) -> Message:
        try:
            await self.repo.delete_task(task_id=task_id)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return Message(message="Task deleted successfully")

    async def add_tag_to_task(self,*,task_id: UUID,tag_id: UUID) -> Task | None:
        try:
            await self.repo.add_tag_to_task(task_id=task_id, tag_id=tag_id)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return await self.repo.get_task_by_id(task_id)

    async def remove_tag_from_task(self,*,task_id: UUID,tag_id: UUID) -> Task | None:
        try:
            await self.repo.remove_tag_from_task(task_id=task_id, tag_id=tag_id)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return await self.repo.get_task_by_id(task_id)