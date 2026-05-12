from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette import status

from app.models import Task,Tag
from app.repositories.tasks import TaskRepository
from app.repositories.tags import TagsRepository
from app.schemas.tasks import TaskCreate,TaskRead, TaskUpdate
from app.schemas.common import Message

class TaskService:
    def __init__(self,session: AsyncSession):
        self.session = session
        self.repo = TaskRepository(session)
        self.tags_repo = TagsRepository(session)

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

    async def _get_task_or_404(self,task_id: UUID) -> Task:
        task=await self.repo.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task

    async def _get_tag_or_404(self,tag_id: UUID) -> Tag:
        tag=await self.tags_repo.get_tag_by_id(tag_id)
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
        return tag

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

    async def add_tag_to_task(self,*,task_id: UUID,tag_id: UUID) -> TaskRead:
        await self._get_task_or_404(task_id)
        await self._get_tag_or_404(tag_id)

        try:
            await self.repo.add_tag_to_task(task_id=task_id, tag_id=tag_id)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        task = await self.repo.get_task_by_id(task_id)

        return TaskRead.model_validate(task, from_attributes=True)

    async def remove_tag_from_task(self,*,task_id: UUID,tag_id: UUID) -> TaskRead:
        await self._get_task_or_404(task_id)
        await self._get_tag_or_404(tag_id)

        try:
            await self.repo.remove_tag_from_task(task_id=task_id, tag_id=tag_id)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        task = await self.repo.get_task_by_id(task_id)

        return TaskRead.model_validate(task, from_attributes=True)