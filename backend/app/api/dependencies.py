from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import forbidden, unauthorized
from app.core.security import decode_access_token
from app.db.session import get_session
from app.models.users import User
from app.repositories.admins import AdminRepository
from app.repositories.users import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    user_id = decode_access_token(token)

    if not user_id:
        raise unauthorized("Invalid authentication token")

    user = await UserRepository(session).get_user_by_id(user_id)

    if not user:
        raise unauthorized("User no longer exists")

    return user


async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    admin = await AdminRepository(session).get_admin_by_user_id(current_user.id)

    if not admin:
        raise forbidden("Admin access required")

    return current_user
