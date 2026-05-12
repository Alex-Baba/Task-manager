from uuid import UUID
from typing import Optional

from sqlalchemy import select, update, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.categories import Categories, Category


class CategoriesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_category_by_id(self, category_id: UUID) -> Optional[Categories]:
        stmt = select(Categories).where(Categories.id == category_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_category_by_name(self, name: str) -> list[Optional[Categories]]:
        # partial search
        name = name.strip()
        # cast from ENUM to string
        stmt = select(Categories).where(
            cast(Categories.name, String).ilike(f"%{name}%")
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all_categories(self) -> list[Categories]:
        stmt = select(Categories)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_category(self, category: Categories) -> Categories:
        self.session.add(category)
        await self.session.flush()
        await self.session.refresh(category)
        return category

    async def update_category(self, category_id: UUID, new_category: Category) -> Optional[Categories]:
        stmt = update(Categories).where(Categories.id == category_id).values(new_category)
        result = await self.session.execute(stmt)
        return result.scalars().first()

