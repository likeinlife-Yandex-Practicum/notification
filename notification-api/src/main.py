from contextlib import asynccontextmanager

from api.v1 import events
from core.settings import settings
from db import postgres, rabbit
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbit.rabbitmq_client = await rabbit.get_connection(settings.rabbit_dsn)
    rabbit.rabbitmq_channel = await rabbit.rabbitmq_client.channel()
    postgres.connection = await postgres.get_connection_pool(settings.postgres_dsn)
    yield
    await postgres.connection.close()
    await rabbit.rabbitmq_channel.close()
    await rabbit.rabbitmq_client.close()


app = FastAPI(
    title="Notification service",
    description="Sending service for sending various notifications to one or a group of users",
    version="0.0.1",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
