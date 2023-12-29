import aio_pika
import structlog
from aio_pika.abc import AbstractChannel
from aio_pika.pool import Pool
from container import Container
from dependency_injector.wiring import Provide, inject

logger = structlog.get_logger()


@inject
async def produce(
    pika_queue_name: str,
    message: bytes,
    channel_pool: Pool[AbstractChannel] = Provide[Container.rabbit_channel_pool],
):
    async with channel_pool.acquire() as channel:
        logger.info("ACQUIRED PRODUCER")
        await channel.default_exchange.publish(
            aio_pika.Message(body=message),
            routing_key=pika_queue_name,
        )
        logger.info("CREATED MESSAGE")
