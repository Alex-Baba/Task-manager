from pydantic import BaseModel

from app.schemas.users import UserRead


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUserRead(UserRead):
    is_admin: bool
