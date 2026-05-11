import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.services.users import UserService

router=APIRouter(tags=["Users"])
@router.post("/users", response_model=UserRead,status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, session:Annotated[AsyncSession,Depends(get_session)])->UserRead:
    service=UserService(session)
    return await service.save_user(payload=payload)

@router.get("/all_users", response_model=list[UserRead],status_code=status.HTTP_200_OK)
async def get_all_users(session:Annotated[AsyncSession,Depends(get_session)]) -> list[UserRead]:
    service=UserService(session)
    users=await service.get_all_users()
    return users

@router.get("/users/{user_id}", response_model=UserRead,status_code=status.HTTP_200_OK)
async def get_user(user_id:uuid.UUID,session:Annotated[AsyncSession,Depends(get_session)]) -> UserRead:
    service=UserService(session)
    return await service.get_user(user_id=user_id)

@router.post("/user_update/{user_id}", response_model=UserRead,status_code=status.HTTP_200_OK)
async def update_user(user_id:uuid.UUID,payload: UserUpdate,session:Annotated[AsyncSession,Depends(get_session)])->UserRead:
    service=UserService(session)
    return await service.update_user(user_id=user_id, payload=payload)

@router.post("/user_delete/{user_id}", response_model=UserRead,status_code=status.HTTP_200_OK)
async def delete_user(user_id:uuid.UUID,session:Annotated[AsyncSession,Depends(get_session)]) -> None:
    service=UserService(session)
    return await service.delete_user(user_id=user_id)
