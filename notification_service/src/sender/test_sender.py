import structlog
from container import Container
from dependency_injector.wiring import Provide, inject
from models import BaseNotificationDetails, QueueMessage
from models.user import UserInfo
from notification_provider import TestProvider

logger = structlog.get_logger()


@inject
async def test_sender(
    message: QueueMessage,
    user_info: UserInfo,
    provider: TestProvider = Provide[Container.test_provider],
):
    details = BaseNotificationDetails(
        id=message.id,
        message=message.message,
        subject=message.subject,
        to=user_info.email,
    )
    await provider.send(details)
