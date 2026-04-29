from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tag
from app.repositories.tags import TagsRepository
from app.schemas.tags import TagRead, TagCreate

class TagService:
    def  __init__(self, session: AsyncSession):
        self.session=session
        self.repo = TagsRepository(session)

    @staticmethod
    def build_tag(*,payload: TagCreate)->Tag:
        tag = Tag()
        tag.name = payload.name

        return tag

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
        tags=await self.repo.get_tags()
        return [TagRead.model_validate(tag,from_attributes=True) for tag in tags]