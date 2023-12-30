from enum import Enum
from typing import Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class QueueMessageType(str, Enum):
    EMAIL = "email"
    TEST = "test"


class EventSchema(BaseModel):
    type_: QueueMessageType
    template: str
    is_regular: bool
    subject: str
    to_role: list[str]
    to_id: list[UUID]
    params: Dict[str, str]


class MessageSchema(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    is_regular: bool
    type_: QueueMessageType
    subject: str
    message: str
    to_id: list[UUID]
    to_role: list[str]


class TemplateSchema(BaseModel):
    slug: str
    content: str
    params: list[str]
