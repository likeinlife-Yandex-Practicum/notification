from functools import lru_cache

from aio_pika import Message
from core.settings import settings
from db.rabbit import AbstractChannel, get_channel
from fastapi import Depends
from jinja2 import Template
from schemas.event import EventSchema, MessageSchema, TemplateSchema

from .errors import NotEnoughParametersError


class QueueService:
    def __init__(self, channel: AbstractChannel, queue_name: str):
        self.channel = channel
        self.queue_name = queue_name

    async def add_message_to_queue(self, event: EventSchema, template: TemplateSchema) -> MessageSchema:
        message = self._generate_message(event, template)
        await self.channel.default_exchange.publish(
            Message(body=message.model_dump_json().encode()),
            routing_key=self.queue_name,
        )
        return message

    def _generate_message(self, event: EventSchema, template: TemplateSchema) -> MessageSchema:
        if not self._check_params(template.params, event.params):
            raise NotEnoughParametersError(template.params, list(event.params.keys()))

        jinja_template = Template(template.content)
        return MessageSchema(
            is_regular=event.is_regular,
            type_=event.type_,
            subject=event.subject,
            message=jinja_template.render(**event.params),
            to_id=event.to_id,
            to_role=event.to_role,
        )

    @staticmethod
    def _check_params(required_params: list, received_params: dict) -> bool:
        return all(el in received_params for el in required_params)


@lru_cache
def get_queue_service(
    channel: AbstractChannel = Depends(get_channel),
):
    return QueueService(channel, settings.rabbit.queue_name)
