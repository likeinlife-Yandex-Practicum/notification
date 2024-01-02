import uuid
from enum import Enum

from pydantic import BaseModel


class NotifyStatusEnum(str, Enum):
    PG = "PG"
    OK = "OK"
    ER = "ER"


class NotifyStatus(BaseModel):
    id: uuid.UUID
    task_id: uuid.UUID
    subject: str
    status: NotifyStatusEnum
    description: str | None
