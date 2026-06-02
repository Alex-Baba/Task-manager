from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.security import create_access_token, verify_password
from app.repositories.admins import AdminRepository
from app.repositories.users import UserRepository
from app.schemas.auth import CurrentUserRead, Token
from app.schemas.users import UserRead


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.admin_repo = AdminRepository(session)

    async def login(self, *, username_or_email: str, password: str) -> Token:
        user = await self.user_repo.get_user_by_username_or_email(username_or_email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return Token(access_token=create_access_token(user.id))

    async def read_current_user(self, user) -> CurrentUserRead:
        admin = await self.admin_repo.get_admin_by_user_id(user.id)
        user_data = UserRead.model_validate(user, from_attributes=True)
        return CurrentUserRead(
            **user_data.model_dump(),
            is_admin=admin is not None,
        )
