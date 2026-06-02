from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admins import Admin


class AdminRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_admin_by_user_id(self, user_id: UUID) -> Admin | None:
        stmt = select(Admin).where(Admin.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_admin(self, admin: Admin) -> Admin:
        self.session.add(admin)
        await self.session.flush()
        await self.session.refresh(admin)
        return admin

    async def delete_admin_by_user_id(self, user_id: UUID) -> bool:
        stmt = delete(Admin).where(Admin.user_id == user_id)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount > 0
