from uuid import UUID
from typing import Optional

from sqlalchemy import select, update, or_ , delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task
from app.models.tags import Tag

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        stmt = select(Task).where(Task.id == task_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_tasks_by_user_id(self, user_id: UUID) -> list[Task]:
        tasks_stmt=select(Task).where(Task.user_id == user_id)
        result=(await self.session.execute(tasks_stmt)).scalars().all()
        return list(result)

    async def create_task(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.flush() # Flush to get the ID of the new task
        await self.session.refresh(task) # Refresh to get the updated task with ID
        return task

    async def update_task(self, task_id:UUID, only_if_changed:bool=False,**values) -> Optional[Task]:
        # Remove keys with None values to avoid overwriting existing data with None
        values={key: value for key, value in values.items() if value is not None}
        if not values:
            return await self.get_task_by_id(task_id)

        # Build the where clause to check for changes if only_if_changed is True
        where=[Task.id == task_id]
        if only_if_changed:
            # Check if any of the provided values are different from the current values in the database
            # maybe add some allowed fields to ignore for this check in the future
            distinct_tasks = [getattr(Task, k).is_distinct_from(v) for k,v in values.items()]
            # If all provided values are the same as the current values, the update will not be applied
            where.append(or_(*distinct_tasks))

        # Perform the update and return the updated task
        stmt = update(Task).where(*where).values(**values).returning(Task)
        result = await self.session.execute(stmt)
        await self.session.flush() # Flush to apply the update
        return result.scalars().first()

    async def delete_task(self, task_id: UUID) -> bool:
        stmt = delete(Task).where(Task.id == task_id)

        result = await self.session.execute(stmt)

        return result.rowcount > 0

    async def add_tag_to_task(self, task_id: UUID, tag_id: UUID) -> Task | None:
        task = await self.get_task_by_id(task_id)
        if not task:
            return None

        tag = await self.session.get(Tag, tag_id)
        #add option to create if not existing
        if not tag:
            return None

        if tag in task.tags:
            return task

        task.tags.append(tag)
        await self.session.flush()

        return task

    async def remove_tag_from_task(self, task_id: UUID, tag_id: UUID) -> Task | None:
        task = await self.get_task_by_id(task_id)
        if not task:
            return None

        tag = await self.session.get(Tag, tag_id)
        if not tag:
            return task

        if tag in task.tags:
            task.tags.remove(tag)
            await self.session.flush()

        return task