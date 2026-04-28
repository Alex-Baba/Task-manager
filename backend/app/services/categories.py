from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Categories
from app.repositories.categories import CategoriesRepository
from app.schemas.categories import CategoryCreate, CategoryRead

class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo=CategoriesRepository(session)

    async def save_category(self, payload: CategoryCreate) -> CategoryRead:
        category=Categories()
        category.name = payload.name.upper()
        try:
            category = await self.repo.create_category(category)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return CategoryRead.model_validate(category, from_attributes=True)

    async def get_categories(self) -> list[CategoryRead]:
        categories=await self.repo.get_all_categories()
        return [CategoryRead.model_validate(category, from_attributes=True) for category in categories]
