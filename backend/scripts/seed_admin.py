import asyncio
import os

from sqlalchemy import or_, select

from app.core.security import hash_password
from app.db.session import SessionLocal, engine
from app.models.admins import Admin
from app.models.users import User


async def seed_admin() -> None:
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_username or not admin_password:
        print(
            "ADMIN_EMAIL, ADMIN_USERNAME and ADMIN_PASSWORD are required; "
            "skipping admin seed."
        )
        return

    if len(admin_password.encode("utf-8")) > 72:
        print("ADMIN_PASSWORD must be at most 72 bytes; skipping admin seed.")
        return

    async with SessionLocal() as session:
        stmt = select(User).where(
            or_(
                User.email == admin_email,
                User.username == admin_username,
            )
        )
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            user = User()
            user.email = admin_email
            user.username = admin_username
            user.password_hash = hash_password(admin_password)
            session.add(user)
            await session.flush()
            await session.refresh(user)
            print(f"Created bootstrap admin user: {user.email}")

        existing_admin = await session.execute(
            select(Admin).where(Admin.user_id == user.id)
        )
        if existing_admin.scalars().first():
            print("Admin already seeded.")
            return

        admin = Admin()
        admin.user_id = user.id
        session.add(admin)
        await session.commit()
        print(f"Seeded admin user: {user.email}")


async def main() -> None:
    try:
        await seed_admin()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
