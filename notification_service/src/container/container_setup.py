import consumer
import producer
from resolver import type_resolver, user_resolver
from sender import smtp_sender, test_sender

from .container import Container


def setup():
    container = Container()
    container.init_resources()
    container.wire(
        modules=[
            producer,
            smtp_sender,
            test_sender,
            consumer,
            type_resolver,
            user_resolver,
        ],
    )
