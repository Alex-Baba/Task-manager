from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_session
from app.models.users import User
from app.schemas.common import Message
from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.services.users import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRead:
    service = UserService(session)
    return await service.save_user(payload=payload)


@router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserRead:
    return UserRead.model_validate(current_user, from_attributes=True)


@router.patch("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
async def update_me(
    payload: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRead:
    service = UserService(session)
    return await service.update_user(user_id=current_user.id, payload=payload)


@router.delete("/me", response_model=Message, status_code=status.HTTP_200_OK)
async def delete_me(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Message:
    service = UserService(session)
    return await service.delete_user(user_id=current_user.id)
