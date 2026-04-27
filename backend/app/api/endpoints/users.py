from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

from app.schemas.users import UserCreate, UserRead
from app.services.users import UserService

router=APIRouter(tags=["Users"])
@router.post("/users", response_model=UserRead,status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, session:Annotated[AsyncSession,Depends(get_session)])->UserRead:
    service=UserService(session)
    return await service.create_user(payload=payload)

@router.get("/all_users", response_model=list[UserRead],status_code=status.HTTP_200_OK)
async def get_all_users(session:Annotated[AsyncSession,Depends(get_session)]) -> list[UserRead]:
    service=UserService(session)
    users=await service.get_all_users()
    return users


