import logging
from http import HTTPStatus

from django.utils import timezone

from notifications.models import Notification, Template
from notifications.celery import app
from notifications.event_api.register_event import prepare_event_model, register_event

logger = logging.getLogger(__name__)


@app.task
def send_notifications():
    current_datetime = timezone.now()
    notifications = Notification.objects.filter(start_at__lte=current_datetime, finish_at__gte=current_datetime)
    for notification in notifications:
        try:
            template = Template.objects.get(slug=notification.template.slug)
            params = dict(item.split('=') for item in template.params)
            event = prepare_event_model(notification, params)
        except Exception as err:
            logger.debug('Failed to prepare event for notification_id=%s\nError: %s', notification.id, err)
        else:
            try:
                response = register_event(event)
            except Exception as err:
                logger.debug('Failed to sent event for notification_id=%s. Error: %s', notification.id, err)
            else:
                if response.status_code == HTTPStatus.OK:
                    logger.debug('Event was successfully registered for notification_id=%s', notification.id)
                else:
                    logger.debug('Event registration failed for notification_id=%s. Response:\n%s',
                                 notification.id, response.text)
