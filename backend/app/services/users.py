from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


from app.models.users import User
from app.repositories.users import UserRepository
from app.core.security import hash_password

from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.schemas.common import Message

class UserService:
    def __init__(self, session: AsyncSession):
        self.session=session
        self.repo=UserRepository(session)

    @staticmethod
    def build_user(*,payload: UserCreate) -> User:
        user=User()
        user.username = payload.username
        user.email = payload.email
        user.password_hash = hash_password(payload.password)
        return user

    @staticmethod
    def build_update_user(*,payload: UserUpdate) -> dict:
        data = payload.model_dump(exclude_unset=True)

        if "password" in data:
            data["password_hash"] = hash_password(data.pop("password"))

        return data


    async def save_user(self, payload: UserCreate) -> UserRead:
        user=self.build_user(payload=payload)
        try:
            user=await self.repo.create_user(user)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return UserRead.model_validate(user,from_attributes=True)

    async def get_user(self,*,user_id:UUID) -> UserRead:
        user=await self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserRead.model_validate(user,from_attributes=True)

    async def get_all_users(self) -> list[UserRead]:
        users=await self.repo.get_all_users()
        return [UserRead.model_validate(user,from_attributes=True) for user in users]

    async def update_user(self,*,user_id: UUID,payload:UserUpdate) -> UserRead:
        await self.get_user(user_id=user_id)
        data=self.build_update_user(payload=payload)
        try:
            updated=await self.repo.update_user(user_id=user_id, **data)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return UserRead.model_validate(updated,from_attributes=True)

    async def delete_user(self,*,user_id: UUID) -> Message:
        await self.get_user(user_id=user_id)
        try:
            deleted = await self.repo.delete_user(user_id=user_id)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return Message(message="User deleted successfully")
