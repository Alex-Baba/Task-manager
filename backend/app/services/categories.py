from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import conflict, not_found
from app.models import Categories
from app.repositories.categories import CategoriesRepository
from app.schemas.categories import CategoryCreate, CategoryRead

class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo=CategoriesRepository(session)

    async def save_category(self, payload: CategoryCreate) -> CategoryRead:
        category=Categories()
        category.name = payload.name
        try:
            category = await self.repo.create_category(category)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise conflict("Category already exists")
        except Exception:
            await self.session.rollback()
            raise
        return CategoryRead.model_validate(category, from_attributes=True)

    async def get_categories(self) -> list[CategoryRead]:
        categories=await self.repo.get_all_categories()
        return [CategoryRead.model_validate(category, from_attributes=True) for category in categories]

    async def get_category_by_name(self, name:str) -> list[CategoryRead]:
        categories=await self.repo.get_category_by_name(name)
        return [CategoryRead.model_validate(category, from_attributes=True) for category in categories]

    async def get_category_by_id(self, category_id:UUID) -> CategoryRead:
        categories=await self.repo.get_category_by_id(category_id)
        if not categories:
            raise not_found("Category")
        return CategoryRead.model_validate(categories, from_attributes=True)
