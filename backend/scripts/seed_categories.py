import asyncio

from sqlalchemy import select

from app.core.enums import Category
from app.db.session import SessionLocal, engine
from app.models.categories import Categories


async def seed_categories() -> None:
    async with SessionLocal() as session:
        result = await session.execute(select(Categories.name))
        existing_categories = set(result.scalars().all())

        missing_categories = []
        for category in Category:
            if category in existing_categories:
                continue

            category_model = Categories()
            category_model.name = category
            missing_categories.append(category_model)

        if not missing_categories:
            print("Categories already seeded.")
            return

        session.add_all(missing_categories)
        await session.commit()
        print(f"Seeded {len(missing_categories)} categories.")


async def main() -> None:
    try:
        await seed_categories()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
