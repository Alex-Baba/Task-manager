from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from app.core.exceptions import conflict, not_found
from app.models import Tag
from app.repositories.tags import TagsRepository
from app.schemas.tags import TagRead, TagCreate, TagUpdate
from app.schemas.common import Message


class TagService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = TagsRepository(session)

    @staticmethod
    def build_tag(*, user_id: UUID, payload: TagCreate) -> Tag:
        tag = Tag()
        tag.name = payload.name
        tag.user_id = user_id

        return tag

    @staticmethod
    def build_update_tag(*, payload: TagUpdate) -> dict:
        return payload.model_dump(exclude_unset=True)

    async def save_tag(self, user_id: UUID, payload: TagCreate) -> TagRead:
        tag = self.build_tag(user_id=user_id, payload=payload)
        try:
            tag = await self.repo.create_tag(tag)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise conflict("Tag already exists")
        except Exception:
            await self.session.rollback()
            raise

        return TagRead.model_validate(tag, from_attributes=True)

    async def get_all_user_tags(self, user_id: UUID) -> list[TagRead]:
        tags = await self.repo.get_all_user_tags(user_id=user_id)
        return [TagRead.model_validate(tag, from_attributes=True) for tag in tags]

    async def get_tag_by_user_id(self, user_id: UUID, tag_id: UUID) -> TagRead:
        tag = await self.repo.get_tag_by_user_id(user_id, tag_id)
        if not tag:
            raise not_found("Tag")
        return TagRead.model_validate(tag, from_attributes=True)

    async def get_user_tags_by_name(self, user_id: UUID, name: str) -> list[TagRead]:
        tags = await self.repo.get_user_tags_by_name(user_id, name)
        return [TagRead.model_validate(tag, from_attributes=True) for tag in tags]

    async def update_tag(
        self, user_id: UUID, tag_id: UUID, payload: TagUpdate
    ) -> TagRead:
        data = self.build_update_tag(payload=payload)
        try:
            tag = await self.repo.update_tag(user_id, tag_id, **data)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise conflict("Tag already exists")
        except Exception:
            await self.session.rollback()
            raise
        if not tag:
            raise not_found("Tag")

        return TagRead.model_validate(tag, from_attributes=True)

    async def delete_tag(self, user_id: UUID, tag_id: UUID) -> Message:
        try:
            deleted = await self.repo.delete_tag(user_id, tag_id)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        if not deleted:
            raise not_found("Tag")

        return Message(message="Tag deleted successfully")
