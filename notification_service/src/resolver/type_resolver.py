import structlog
from aio_pika.message import IncomingMessage
from misc.type_alias import SenderType
from models.queue_message import UserProvidedQueueMessage
from pydantic import TypeAdapter
from sender import smtp_sender, test_sender

logger = structlog.get_logger()


notification_resolve_ways: dict[str, SenderType] = {
    "email": smtp_sender.sender,
    "test": test_sender.sender,
}


async def resolver(
    message: IncomingMessage,
) -> None:
    """Resolve notification type."""
    logger.info("[x] Received message", id=message.message_id)
    adapted_message = TypeAdapter(UserProvidedQueueMessage).validate_json(message.body)
    logger.debug(adapted_message)
    sender = notification_resolve_ways.get(adapted_message.type_)
    if not sender:
        logger.error("Notification type not found", type=adapted_message.type_)
        return

    result = await sender(adapted_message)
    if not result:
        return await message.reject()
    return await message.ack()
