from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

from app.schemas.categories import CategoryRead, CategoryCreate
from app.services.categories import CategoryService

router = APIRouter(tags=["Categories"])
@router.post("/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(payload:CategoryCreate,session:Annotated[AsyncSession,Depends(get_session)])->CategoryRead:
    category = CategoryService(session)
    return await category.save_category(payload=payload)

@router.get("/categories",response_model=list[CategoryRead],status_code=status.HTTP_200_OK)
async def get_categories(session:Annotated[AsyncSession,Depends(get_session)])->list[CategoryRead]:
    service = CategoryService(session)
    categories = await service.get_categories()
    return categories