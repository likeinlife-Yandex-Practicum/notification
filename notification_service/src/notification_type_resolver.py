import structlog
from aio_pika.abc import AbstractIncomingMessage
from container import Container
from dependency_injector.wiring import Provide
from models import QueueMessage
from pydantic import TypeAdapter
from sender import smtp_sender, test_sender
from type_alias import SenderType
from user_provider import UserProvider

logger = structlog.get_logger()


notification_resolve_ways: dict[str, SenderType] = {
    "email": smtp_sender,
    "test": test_sender,
}


async def resolver(
    message: AbstractIncomingMessage,
):
    """Resolve notification type."""
    async with message.process():
        logger.info("[x] Received message", id=message.message_id)
        adapted_message = TypeAdapter(QueueMessage).validate_json(message.body)
        logger.debug(adapted_message)
        sender = notification_resolve_ways.get(adapted_message.type_)
        if not sender:
            logger.error("Notification type not found", type=adapted_message.type_)
            return

        await resolve_user_id(adapted_message, sender)
        await resolve_role(adapted_message, sender)


async def resolve_user_id(
    message: QueueMessage,
    sender: SenderType,
    user_provider: UserProvider = Provide[Container.user_provider],
):
    """Resolve user ids."""
    for id_ in message.to_id:
        user = await user_provider.from_id(id_)
        if not user:
            logger.warning("User not found", id=id_)
            continue
        await sender(message, user)


async def resolve_role(
    message: QueueMessage,
    sender: SenderType,
    user_provider: UserProvider = Provide[Container.user_provider],
):
    """Resolve user roles."""
    for role in message.to_role:
        user_list = await user_provider.from_role(role)
        if not user_list:
            logger.warning("Users not found", role=role)
            continue
        for user in user_list:
            await sender(message, user)
