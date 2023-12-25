import asyncio
from typing import Callable, Coroutine

import structlog
from aio_pika.abc import AbstractChannel, AbstractIncomingMessage
from aio_pika.pool import Pool
from container import Container
from core.settings import Settings
from dependency_injector.wiring import Provide, inject

logger = structlog.get_logger()


@inject
async def consumer(
    callback: Callable[[AbstractIncomingMessage], Coroutine],
    channel_pool: Pool[AbstractChannel] = Provide[Container.rabbit_channel_pool],
    settings: Settings = Provide["settings"],
):
    async with channel_pool.acquire() as channel:
        logger.info("ACQUIRED CONSUMER")
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(
            settings.queue.notify,
            auto_delete=False,
            durable=True,
            arguments={"x-queue-type": "quorum"},
        )

        await queue.consume(callback)

        await asyncio.Future()
