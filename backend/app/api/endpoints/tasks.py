from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_session
from app.models.users import User
from app.schemas.common import Message
from app.schemas.tasks import TaskCreate, TaskRead, TaskUpdate
from app.services.tasks import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskRead:
    service = TaskService(session)
    return await service.save_task(payload=payload, user_id=current_user.id)


@router.get("", response_model=list[TaskRead], status_code=status.HTTP_200_OK)
async def get_tasks(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[TaskRead]:
    service = TaskService(session)
    return await service.get_all_tasks_by_user_id(user_id=current_user.id)


@router.get("/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def get_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskRead:
    service = TaskService(session)
    return await service.get_task(task_id=task_id, user_id=current_user.id)


@router.patch("/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskRead:
    service = TaskService(session)
    return await service.update_task(
        task_id=task_id,
        user_id=current_user.id,
        payload=payload,
    )


@router.post(
    "/{task_id}/tags/{tag_id}",
    response_model=TaskRead,
    status_code=status.HTTP_200_OK,
)
async def add_tag_to_task(
    task_id: UUID,
    tag_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskRead:
    service = TaskService(session)
    return await service.add_tag_to_task(
        task_id=task_id,
        tag_id=tag_id,
        user_id=current_user.id,
    )


@router.delete(
    "/{task_id}/tags/{tag_id}",
    response_model=TaskRead,
    status_code=status.HTTP_200_OK,
)
async def remove_tag_from_task(
    task_id: UUID,
    tag_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskRead:
    service = TaskService(session)
    return await service.remove_tag_from_task(
        task_id=task_id,
        tag_id=tag_id,
        user_id=current_user.id,
    )


@router.delete("/{task_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Message:
    service = TaskService(session)
    return await service.delete_task(task_id=task_id, user_id=current_user.id)
