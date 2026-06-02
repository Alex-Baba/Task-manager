from pydantic import BaseModel
from datetime import datetime


class TimeStamp(BaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Message(BaseModel):
    message: str
