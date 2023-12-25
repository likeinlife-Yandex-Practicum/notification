import uuid

from pydantic import BaseModel


class UserInfo(BaseModel):
    id: uuid.UUID
    roles: list[str]
    email: str
