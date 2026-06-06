from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import not_found
from app.models.admins import Admin
from app.repositories.admins import AdminRepository
from app.repositories.users import UserRepository
from app.schemas.admins import AdminRead, AdminUserRead
from app.schemas.common import Message
from app.schemas.users import UserRead


class AdminService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AdminRepository(session)
        self.user_repo = UserRepository(session)

    async def get_users_with_admin_status(self) -> list[AdminUserRead]:
        users = await self.user_repo.get_all_users()
        admin_user_ids = await self.repo.get_admin_user_ids()

        return [
            AdminUserRead(
                **UserRead.model_validate(user, from_attributes=True).model_dump(),
                is_admin=user.id in admin_user_ids,
            )
            for user in users
        ]

    async def grant_admin(self, *, user_id: UUID) -> AdminRead:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise not_found("User")

        existing_admin = await self.repo.get_admin_by_user_id(user_id)
        if existing_admin:
            return AdminRead.model_validate(existing_admin, from_attributes=True)

        admin = Admin()
        admin.user_id = user_id

        try:
            admin = await self.repo.create_admin(admin)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return AdminRead.model_validate(admin, from_attributes=True)

    async def revoke_admin(self, *, user_id: UUID) -> Message:
        try:
            deleted = await self.repo.delete_admin_by_user_id(user_id)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        if not deleted:
            raise not_found("Admin")

        return Message(message="Admin access revoked successfully")
