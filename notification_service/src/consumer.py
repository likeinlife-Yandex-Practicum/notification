import asyncio
from typing import Callable, Coroutine

import structlog
from aio_pika.abc import AbstractChannel, AbstractIncomingMessage
from aio_pika.pool import Pool
from container import Container
from dependency_injector.wiring import Provide, inject

logger = structlog.get_logger()


@inject
async def consumer(
    queue_name: str,
    callback: Callable[[AbstractIncomingMessage], Coroutine],
    channel_pool: Pool[AbstractChannel] = Provide[Container.rabbit_channel_pool],
):
    async with channel_pool.acquire() as channel:
        logger.info("ACQUIRED CONSUMER")
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(
            queue_name,
            auto_delete=False,
            durable=True,
            arguments={"x-queue-type": "quorum"},
        )

        await queue.consume(callback)

        await asyncio.Future()
