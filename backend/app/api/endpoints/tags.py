from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.common import Message
from app.schemas.tags import TagCreate, TagRead, TagUpdate
from app.services.tags import TagService

router = APIRouter(prefix="/users/{user_id}/tags", tags=["Tags"])


@router.post("", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(
    user_id: UUID,
    payload: TagCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TagRead:
    service = TagService(session)
    return await service.save_tag(user_id=user_id, payload=payload)


@router.get("", response_model=list[TagRead], status_code=status.HTTP_200_OK)
async def get_tags(
    user_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    name: str | None = None,
) -> list[TagRead]:
    service = TagService(session)

    if name:
        return await service.get_user_tags_by_name(user_id=user_id, name=name)

    return await service.get_all_user_tags(user_id=user_id)


@router.get("/{tag_id}", response_model=TagRead, status_code=status.HTTP_200_OK)
async def get_tag_by_id(
    user_id: UUID,
    tag_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TagRead:
    service = TagService(session)
    return await service.get_tag_by_user_id(user_id=user_id, tag_id=tag_id)


@router.patch("/{tag_id}", response_model=TagRead, status_code=status.HTTP_200_OK)
async def update_tag(
    user_id: UUID,
    tag_id: UUID,
    payload: TagUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TagRead:
    service = TagService(session)
    return await service.update_tag(user_id=user_id, tag_id=tag_id, payload=payload)


@router.delete("/{tag_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_tag(
    user_id: UUID,
    tag_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Message:
    service = TagService(session)
    return await service.delete_tag(user_id=user_id, tag_id=tag_id)
