from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

from app.schemas.tasks import TaskRead, TaskCreate, TaskUpdate
from app.services.tasks import TaskService
from app.schemas.common import Message

router = APIRouter(tags=['Tasks'])

@router.post('/create_task',response_model=TaskRead,status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate,session:Annotated[AsyncSession,Depends(get_session)]) -> TaskRead:
    service = TaskService(session)
    return await service.save_task(payload=payload)

@router.get('/get_task/{task_id}',response_model=TaskRead,status_code=status.HTTP_200_OK)
async def get_task(task_id:UUID,session:Annotated[AsyncSession,Depends(get_session)]) -> TaskRead:
    service = TaskService(session)
    return await service.get_task(task_id=task_id)

@router.get('/get_all_tasks_by_user_id/{user_id}',response_model=list[TaskRead],status_code=status.HTTP_200_OK)
async def get_all_tasks_by_user_id(user_id:UUID,session:Annotated[AsyncSession,Depends(get_session)]) -> list[TaskRead]:
    service = TaskService(session)
    return await service.get_all_tasks_by_user_id(user_id=user_id)

@router.patch('/update_task/{task_id}',response_model=TaskRead,status_code=status.HTTP_200_OK)
async def update_task(task_id:UUID,payload:TaskUpdate,session:Annotated[AsyncSession,Depends(get_session)]) -> TaskRead:
    service = TaskService(session)
    return await service.update_task(task_id=task_id,payload=payload)

@router.post('/tasks/{task_id}/tag/{tag_id}',response_model=TaskRead | None,status_code=status.HTTP_200_OK)
async def add_tag_to_task(task_id:UUID,tag_id:UUID,session:Annotated[AsyncSession,Depends(get_session)]) -> TaskRead | None:
    service = TaskService(session)
    return await service.add_tag_to_task(task_id=task_id,tag_id=tag_id)

@router.delete('/tasks/{task_id}/tag/{tag_id}',response_model=TaskRead | None,status_code=status.HTTP_200_OK)
async def remove_tag_from_task(task_id:UUID,tag_id:UUID,session:Annotated[AsyncSession,Depends(get_session)]) -> TaskRead | None:
    service = TaskService(session)
    return await service.remove_tag_from_task(task_id=task_id,tag_id=tag_id)

@router.delete('/delete_task/{task_id}',response_model=Message,status_code=status.HTTP_200_OK)
async def delete_task(task_id:UUID,session:Annotated[AsyncSession,Depends(get_session)]) -> Message:
    service = TaskService(session)
    return await service.delete_task(task_id=task_id)