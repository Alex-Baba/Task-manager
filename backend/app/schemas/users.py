from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from typing import Optional

from .common import TimeStamp

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

    @field_validator("username", "email", "password", mode="before")
    @classmethod
    def strip_strings(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("password")
    @classmethod
    def validate_bcrypt_password_length(cls, value: str):
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes")
        return value

class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)

    @field_validator("username", "email", "password", mode="before")
    @classmethod
    def strip_strings(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("password")
    @classmethod
    def validate_bcrypt_password_length(cls, value: Optional[str]):
        if value is not None and len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes")
        return value

class UserRead(UserBase, TimeStamp):
    id: UUID
