from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

from app.schemas.tags import TagRead, TagCreate
from app.services.tags import TagService

router = APIRouter(tags=['Tags'])

@router.post('/tags',response_model=TagRead,status_code=status.HTTP_201_CREATED)
async def create_tag(payload: TagCreate, session: Annotated[AsyncSession,Depends(get_session)])->TagRead:
    service=TagService(session)
    return await service.save_tag(payload=payload)

@router.get('/all_tags',response_model=list[TagRead],status_code=status.HTTP_200_OK)
async def get_all_tags(session: Annotated[AsyncSession,Depends(get_session)])->list[TagRead]:
    service=TagService(session)
    return await service.get_all_tags()