from contextlib import asynccontextmanager

import asyncpg
import backoff
from core import settings


@backoff.on_exception(backoff.expo, Exception, max_time=60)
async def get_connection_pool():
    pool = await asyncpg.create_pool(settings.postgres_dsn)
    return pool


@asynccontextmanager
async def postgres_contextmanager():
    connection = await get_connection_pool()
    yield connection
    await connection.close()
