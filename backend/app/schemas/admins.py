from uuid import UUID

from pydantic import ConfigDict

from .common import TimeStamp


class AdminRead(TimeStamp):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
