from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from schemas.event import EventSchema
from services.errors import NotEnoughParametersError
from services.queue_service import QueueService, get_queue_service
from services.template_service import TemplateService, get_template_service

router = APIRouter()


@router.post(
    "/register-event",
    status_code=status.HTTP_201_CREATED,
)
async def add_user_event_to_queue(
    event: EventSchema,
    queue_service: QueueService = Depends(get_queue_service),
    template_service: TemplateService = Depends(get_template_service),
) -> UUID:
    template = await template_service.get_template_by_slug(event.template)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        message = await queue_service.add_message_to_queue(event, template)
    except NotEnoughParametersError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )

    return message.id_
