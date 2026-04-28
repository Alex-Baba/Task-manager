from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

from app.schemas.tasks import TaskRead, TaskCreate
from app.services.tasks import TaskService

router = APIRouter(tags=['Tasks'])

@router.post('/tasks',response_model=TaskRead,status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate,session:Annotated[AsyncSession,Depends(get_session)]) -> TaskRead:
    service = TaskService(session)
    return await service.save_task(payload=payload)

@router.get('/tasks',response_model=TaskRead,status_code=status.HTTP_200_OK)
async def get_task(task_id:UUID,session:Annotated[AsyncSession,Depends(get_session)]) -> TaskRead:
    service = TaskService(session)
    return await service.get_task(task_id=task_id)