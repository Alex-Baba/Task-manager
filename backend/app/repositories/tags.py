from uuid import UUID
from typing import Optional

from sqlalchemy import select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tag

class TagsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tag_by_id(self, tag_id: UUID) -> Optional[Tag]:
        stmt = select(Tag).where(Tag.id == tag_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_tag(self, tag: Tag) -> Tag:
        self.session.add(tag)
        await self.session.flush() # Flush to get the ID of the new tag
        await self.session.refresh(tag) # Refresh to get the updated tag with ID
        return tag

    async def update_tag(self, tag_id:UUID, only_if_changed:bool=False,**values) -> Optional[Tag]:
        # Remove keys with None values to avoid overwriting existing data with None
        values={key: value for key, value in values.items() if value is not None}
        if not values:
            return await self.get_tag_by_id(tag_id)

        # Build the where clause to check for changes if only_if_changed is True
        where=[Tag.id == tag_id]
        if only_if_changed:
            # Check if any of the provided values are different from the current values in the database
            # maybe add some allowed fields to ignore for this check in the future
            distinct_tags = [getattr(Tag, k).is_distinct_from(v) for k,v in values.items()]
            # If all provided values are the same as the current values, the update will not be applied
            where.append(or_(*distinct_tags))

        # Perform the update and return the updated tag
        stmt = update(Tag).where(*where).values(**values).returning(Tag)
        result = await self.session.execute(stmt)
        await self.session.flush() # Flush to apply the update
        return result.scalars().first()

    async def delete_tag(self, tag_id:UUID) -> bool:
        tag=await self.get_tag_by_id(tag_id)
        if not tag:
            return False
        await self.session.delete(tag)
        await self.session.flush()
        return True