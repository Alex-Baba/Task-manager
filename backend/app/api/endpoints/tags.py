from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

from app.schemas.tags import TagRead, TagCreate, TagUpdate
from app.services.tags import TagService
from app.schemas.common import Message

router = APIRouter(tags=['Tags'])

@router.post('/create_tags',response_model=TagRead,status_code=status.HTTP_201_CREATED)
async def create_tag(payload: TagCreate, session: Annotated[AsyncSession,Depends(get_session)])->TagRead:
    service=TagService(session)
    return await service.save_tag(payload=payload)

@router.get('/all_tags',response_model=list[TagRead],status_code=status.HTTP_200_OK)
async def get_all_tags(session: Annotated[AsyncSession,Depends(get_session)])->list[TagRead]:
    service=TagService(session)
    return await service.get_all_tags()

@router.get('/tag_id/{tag_id}',response_model=TagRead,status_code=status.HTTP_200_OK)
async def get_tag_by_id(tag_id:UUID,session: Annotated[AsyncSession,Depends(get_session)])->TagRead:
    service=TagService(session)
    return await service.get_tag_by_id(tag_id=tag_id)

@router.get('/tag_name/{tag_name}',response_model=list[TagRead],status_code=status.HTTP_200_OK)
async def get_tag_by_name(tag_name:str,session: Annotated[AsyncSession,Depends(get_session)])->list[TagRead]:
    service=TagService(session)
    return await service.get_tags_by_name(name=tag_name)

@router.patch('/update_tag/{tag_id}',response_model=TagRead,status_code=status.HTTP_200_OK)
async def update_tag(tag_id:UUID,payload:TagUpdate,session: Annotated[AsyncSession,Depends(get_session)])->TagRead:
    service=TagService(session)
    return await service.update_tag(tag_id=tag_id,payload=payload)

@router.delete('/delete_tag/{tag_id}',response_model=Message,status_code=status.HTTP_200_OK)
async def delete_tag(tag_id:UUID,session: Annotated[AsyncSession,Depends(get_session)])->Message:
    service=TagService(session)
    return await service.delete_tag(tag_id=tag_id)
