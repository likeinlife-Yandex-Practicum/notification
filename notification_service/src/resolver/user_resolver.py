import structlog
from aio_pika.abc import AbstractIncomingMessage
from container import Container
from core import settings
from dependency_injector.wiring import Provide, inject
from models import QueueMessage
from models.queue_message import UserProvidedQueueMessage
from producer import produce
from pydantic import TypeAdapter
from user_provider import UserProvider

logger = structlog.get_logger()


async def resolver(
    message: AbstractIncomingMessage,
):
    """Resolve users."""
    async with message.process():
        logger.info("[x] Received message", id=message.message_id)
        adapted_message = TypeAdapter(QueueMessage).validate_json(message.body)
        logger.debug(adapted_message)

        await resolve_user_id(adapted_message)
        await resolve_role(adapted_message)


@inject
async def resolve_user_id(
    message: QueueMessage,
    user_provider: UserProvider = Provide[Container.user_provider],
):
    """Resolve user ids."""
    for id_ in message.to_id:
        user = await user_provider.from_id(id_)
        if not user:
            logger.warning("User not found", id=id_)
            continue
        formed_message = UserProvidedQueueMessage(
            id=message.id,
            user=user,
            type_=message.type_,
            message=message.message,
            subject=message.subject,
        )
        await produce(
            pika_queue_name=settings.queue.user_provided,
            message=formed_message.model_dump_json().encode(),
        )


@inject
async def resolve_role(
    message: QueueMessage,
    user_provider: UserProvider = Provide[Container.user_provider],
):
    """Resolve user roles."""
    for role in message.to_role:
        user_list = await user_provider.from_role(role)
        if not user_list:
            logger.warning("Users not found", role=role)
            continue
        for user in user_list:
            formed_message = UserProvidedQueueMessage(
                id=message.id,
                user=user,
                type_=message.type_,
                message=message.message,
                subject=message.subject,
            )
            await produce(
                pika_queue_name=settings.queue.user_provided,
                message=formed_message.model_dump_json().encode(),
            )
