from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.categories import CategoryRead
from app.services.categories import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryRead], status_code=status.HTTP_200_OK)
async def get_categories(
    session: Annotated[AsyncSession, Depends(get_session)],
    name: str | None = None,
) -> list[CategoryRead]:
    service = CategoryService(session)

    if name:
        return await service.get_category_by_name(name)

    return await service.get_categories()


@router.get(
    "/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
)
async def get_category_by_id(
    category_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CategoryRead:
    service = CategoryService(session)
    return await service.get_category_by_id(category_id=category_id)
