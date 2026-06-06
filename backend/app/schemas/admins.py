from uuid import UUID

from pydantic import ConfigDict

from .users import UserRead
from .common import TimeStamp


class AdminRead(TimeStamp):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID


class AdminUserRead(UserRead):
    is_admin: bool
