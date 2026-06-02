from uuid import UUID
from typing import Optional

from sqlalchemy import delete, select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User

class UserRepository:
    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_username_or_email(self, username_or_email: str) -> Optional[User]:
        stmt = select(User).where(
            or_(
                User.username == username_or_email,
                User.email == username_or_email,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_users(self) -> list[User]:
        stmt = select(User).order_by(User.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush() # Flush to get the ID of the new user
        await self.session.refresh(user) # Refresh to get the updated user with ID
        return user

    async def update_user(self,*, user_id: UUID, only_if_changed: bool=False,**values) -> Optional[User]:
        # Remove keys with None values to avoid overwriting existing data with None
        values={key: value for key, value in values.items() if value is not None}
        if not values:
            return await self.get_user_by_id(user_id)

        # Build the where clause to check for changes if only_if_changed is True
        where=[User.id == user_id]
        if only_if_changed:
            # Check if any of the provided values are different from the current values in the database
            # maybe add some allowed fields to ignore for this check in the future
            distinct_users = [getattr(User, k).isdistinct_from(v) for k,v in values.items()]
            # If all provided values are the same as the current values, the update will not be applied
            where.append(or_(*distinct_users))

        # Perform the update and return the updated user
        stmt = update(User).where(*where).values(**values).returning(User)
        result = await self.session.execute(stmt)
        await self.session.flush() # Flush to apply the update
        return result.scalars().first()

    async def delete_user(self, user_id: UUID) -> bool:
        stmt = delete(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount > 0
