import structlog
from aio_pika.abc import AbstractIncomingMessage
from models.queue_message import UserProvidedQueueMessage
from pydantic import TypeAdapter
from sender import smtp_sender, test_sender
from type_alias import SenderType

logger = structlog.get_logger()


notification_resolve_ways: dict[str, SenderType] = {
    "email": smtp_sender.sender,
    "test": test_sender.sender,
}


async def resolver(
    message: AbstractIncomingMessage,
):
    """Resolve notification type."""
    async with message.process():
        logger.info("[x] Received message", id=message.message_id)
        adapted_message = TypeAdapter(UserProvidedQueueMessage).validate_json(message.body)
        logger.debug(adapted_message)
        sender = notification_resolve_ways.get(adapted_message.type_)
        if not sender:
            logger.error("Notification type not found", type=adapted_message.type_)
            return

        await sender(adapted_message)
