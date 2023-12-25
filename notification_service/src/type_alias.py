from typing import Callable, Coroutine, TypeAlias

from models import QueueMessage
from models.user import UserInfo

SenderType: TypeAlias = Callable[[QueueMessage, UserInfo], Coroutine]
