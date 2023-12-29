import structlog
from container import Container
from core import settings
from dependency_injector.wiring import Provide, inject
from models import SMTPNotificationDetails
from models.queue_message import UserProvidedQueueMessage
from notification_provider import SMTPProvider
from producer import produce

logger = structlog.get_logger()


@inject
async def sender(
    message: UserProvidedQueueMessage,
    provider: SMTPProvider = Provide[Container.smtp_provider],
):
    details = SMTPNotificationDetails(
        id=message.id,
        message=message.message,
        subject=message.subject,
        from_=message.user.email,
        to=message.user.email,
    )
    result = await provider.send(details)
    if not result:
        logger.error("Cant send email, resending", id=message.id)
        await produce(settings.queue.dead_letter, message.model_dump_json().encode())
