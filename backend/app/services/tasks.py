from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task
from app.repositories.tasks import TaskRepository
from app.schemas.tasks import TaskCreate,TaskRead

class TaskService:
    def __init__(self,session: AsyncSession):
        self.session = session
        self.repo = TaskRepository(session)

    @staticmethod
    def build_task(*,payload: TaskCreate) -> Task:
        task = Task()
        task.title = payload.title.strip()
        task.description = payload.description.strip() if payload.description else None
        task.user_id = payload.user_id
        task.due_date = payload.due_date

        return task

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