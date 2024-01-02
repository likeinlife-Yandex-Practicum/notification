import uuid
import requests

from config.settings import NOTIFICATION_API_URL
from notifications.models import Notification
from notifications.event_api.schemas import EventSchema


def prepare_event_model(notification: Notification, params) -> EventSchema:
    return EventSchema(
        type_='email',
        template=notification.template.slug,
        is_regular=True,
        subject=notification.subject,
        to_role=notification.roles,
        to_id=[],
        params=params,
    )


def register_event(event: EventSchema) -> requests.Response:
    request_id = str(uuid.uuid4())
    response = requests.post(
        f'{NOTIFICATION_API_URL}/api/v1/events',
        data=event.json(),
        headers={'X-Request-Id': request_id}
    )
    return response
