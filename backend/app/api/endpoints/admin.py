from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_admin
from app.db.session import get_session
from app.schemas.admins import AdminRead
from app.schemas.categories import CategoryCreate, CategoryRead
from app.schemas.common import Message
from app.schemas.users import UserRead
from app.services.admins import AdminService
from app.services.categories import CategoryService
from app.services.users import UserService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("/users", response_model=list[UserRead], status_code=status.HTTP_200_OK)
async def get_all_users(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[UserRead]:
    service = UserService(session)
    return await service.get_all_users()


@router.get("/users/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRead:
    service = UserService(session)
    return await service.get_user(user_id=user_id)


@router.delete(
    "/users/{user_id}",
    response_model=Message,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Message:
    service = UserService(session)
    return await service.delete_user(user_id=user_id)


@router.post(
    "/users/{user_id}/admin",
    response_model=AdminRead,
    status_code=status.HTTP_201_CREATED,
)
async def grant_admin(
    user_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AdminRead:
    service = AdminService(session)
    return await service.grant_admin(user_id=user_id)


@router.delete(
    "/users/{user_id}/admin",
    response_model=Message,
    status_code=status.HTTP_200_OK,
)
async def revoke_admin(
    user_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Message:
    service = AdminService(session)
    return await service.revoke_admin(user_id=user_id)


@router.post(
    "/categories",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    payload: CategoryCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CategoryRead:
    service = CategoryService(session)
    return await service.save_category(payload=payload)
