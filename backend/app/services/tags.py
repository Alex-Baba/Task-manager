from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models import Tag
from app.repositories.tags import TagsRepository
from app.schemas.tags import TagRead, TagCreate, TagUpdate
from app.schemas.common import Message

class TagService:
    def  __init__(self, session: AsyncSession):
        self.session=session
        self.repo = TagsRepository(session)

    @staticmethod
    def build_tag(*,payload: TagCreate)->Tag:
        tag = Tag()
        tag.name = payload.name

        return tag

    @staticmethod
    def build_update_tag(*,payload: TagUpdate)->dict:
        return payload.model_dump(exclude_unset=True)

    async def save_tag(self, payload: TagCreate)->TagRead:
        tag=self.build_tag(payload=payload)
        try:
            tag=await self.repo.create_tag(tag)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return TagRead.model_validate(tag,from_attributes=True)

    async def get_all_tags(self)->list[TagRead]:
        tags=await self.repo.get_all_tags()
        return [TagRead.model_validate(tag,from_attributes=True) for tag in tags]

    async def get_tag_by_id(self, tag_id: UUID)->TagRead:
        tag=await self.repo.get_tag_by_id(tag_id)
        return TagRead.model_validate(tag,from_attributes=True)

    async def get_tags_by_name(self, name: str) -> list[TagRead]:
        tags=await self.repo.get_tags_by_name(name)
        return [TagRead.model_validate(tag,from_attributes=True) for tag in tags]

    async def update_tag(self,tag_id:UUID, payload: TagUpdate)->TagRead:
        data=self.build_update_tag(payload=payload)
        try:
            tag=await self.repo.update_tag(tag_id,**data)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return TagRead.model_validate(tag,from_attributes=True)

    async def delete_tag(self, tag_id: UUID)->Message:
        try:
            tag = await self.repo.get_tag_by_id(tag_id)
            await self.session.delete(tag)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return Message(message="Tag deleted successfully")
