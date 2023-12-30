from typing import Optional

from core.settings import settings
from db.postgres import Pool, get_connection
from fastapi import Depends
from schemas.event import TemplateSchema


class TemplateService:
    def __init__(self, con_pool: Pool):
        self.con_pool = con_pool

    async def get_template_by_slug(self, slug) -> Optional[TemplateSchema]:
        async with self.con_pool.acquire() as con:
            result = await con.fetchrow(f"SELECT * FROM {settings.postgres.table_name} WHERE slug = $1;", slug)  # noqa: S608
            if not result:
                return None
            return TemplateSchema(**result)


def get_template_service(con_pool: Pool = Depends(get_connection)):
    return TemplateService(con_pool)
