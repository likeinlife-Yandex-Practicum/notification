import structlog
from container import Container
from core import settings
from dependency_injector.wiring import Provide, inject
from models import QueueMessage, SMTPNotificationDetails
from models.user import UserInfo
from notification_provider import SMTPProvider
from producer import produce

logger = structlog.get_logger()


@inject
async def smtp_sender(
    message: QueueMessage,
    user_info: UserInfo,
    provider: SMTPProvider = Provide[Container.smtp_provider],
):
    details = SMTPNotificationDetails(
        id=message.id,
        message=message.message,
        subject=message.subject,
        from_=user_info.email,
        to=user_info.email,
    )
    result = await provider.send(details)
    if not result:
        logger.error("Cant send email, resending", id=message.id)
        await produce(settings.queue.dead_letter, message)
