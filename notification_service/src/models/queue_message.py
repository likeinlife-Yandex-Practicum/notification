import uuid
from enum import Enum

from pydantic import BaseModel, Field


class QueueMessageType(str, Enum):
    EMAIL = "email"
    WEBSOCKET = "websocket"
    TEST = "test"


class QueueMessage(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    to_id: list[uuid.UUID]
    to_role: list[str]
    type_: QueueMessageType
    message: str
    subject: str
