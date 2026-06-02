from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_session
from app.models.users import User
from app.schemas.common import Message
from app.schemas.tags import TagCreate, TagRead, TagUpdate
from app.services.tags import TagService

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(
    payload: TagCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TagRead:
    service = TagService(session)
    return await service.save_tag(user_id=current_user.id, payload=payload)


@router.get("", response_model=list[TagRead], status_code=status.HTTP_200_OK)
async def get_tags(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    name: str | None = None,
) -> list[TagRead]:
    service = TagService(session)

    if name:
        return await service.get_user_tags_by_name(user_id=current_user.id, name=name)

    return await service.get_all_user_tags(user_id=current_user.id)


@router.get("/{tag_id}", response_model=TagRead, status_code=status.HTTP_200_OK)
async def get_tag_by_id(
    tag_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TagRead:
    service = TagService(session)
    return await service.get_tag_by_user_id(user_id=current_user.id, tag_id=tag_id)


@router.patch("/{tag_id}", response_model=TagRead, status_code=status.HTTP_200_OK)
async def update_tag(
    tag_id: UUID,
    payload: TagUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TagRead:
    service = TagService(session)
    return await service.update_tag(
        user_id=current_user.id,
        tag_id=tag_id,
        payload=payload,
    )


@router.delete("/{tag_id}", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_tag(
    tag_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Message:
    service = TagService(session)
    return await service.delete_tag(user_id=current_user.id, tag_id=tag_id)
