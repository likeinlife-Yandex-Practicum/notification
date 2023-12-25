import asyncio

import consumer
import notification_type_resolver
import producer
import sender
from container import Container


async def run():
    task = asyncio.create_task(
        consumer.consumer(
            callback=notification_type_resolver.resolver,
        ),
    )

    await task


def configure_container():
    container = Container()
    container.init_resources()
    container.wire(
        modules=[
            producer,
            sender,
            consumer,
            notification_type_resolver,
        ],
    )


def main():
    configure_container()
    asyncio.run(run())


if __name__ == "__main__":
    main()
