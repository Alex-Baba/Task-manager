from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.users import User
from app.repositories.users import UserRepository

from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.schemas.common import Message

class UserService:
    def __init__(self, session: AsyncSession):
        self.session=session
        self.repo=UserRepository(session)

    @staticmethod
    def build_user(*,payload: UserCreate) -> User:
        user=User()
        user.username = payload.username.strip()
        user.email = payload.email.strip()
        user.password_hash = payload.password.strip()
        return user

    @staticmethod
    def build_update_user(*,payload: UserUpdate) -> dict:
        data=payload.model_dump(exclude_unset=True)
        if "username" in data:
            data["username"] = str(data["username"]).strip()
        if "email" in data:
            data["email"] = str(data["email"]).strip()
        if "password_hash" in data:
            data["password_hash"] = str(data["password_hash"]).strip()
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
            raise
        return UserRead.model_validate(user,from_attributes=True)

    async def get_all_users(self) -> list[UserRead]:
        users=await self.repo.get_all_users()
        return [UserRead.model_validate(user,from_attributes=True) for user in users]

    async def update_user(self,*,user_id: UUID,payload:UserUpdate) -> UserRead:
        data=self.build_update_user(payload=payload)
        try:
            updated=await self.repo.update_user(user_id=user_id, **data)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return UserRead.model_validate(updated,from_attributes=True)

    async def delete_user(self,*,user_id: UUID) -> Message:
        try:
            await self.repo.delete_user(user_id=user_id)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return Message(message="User deleted successfully")