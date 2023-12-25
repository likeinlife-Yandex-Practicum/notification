import uuid
from typing import Any

from asyncpg import Pool
from models.user import UserInfo


class UserProvider:
    def __init__(self, logger: Any, connection_pool: Pool) -> None:
        self.logger = logger
        self.connection_pool = connection_pool

    async def from_id(self, id_: uuid.UUID) -> UserInfo | None:
        self.logger.debug("Try fetch", id=id_)
        async with self.connection_pool.acquire() as con:
            result = await con.fetchrow("SELECT * FROM auth.user WHERE id=$1", id_)
        if not result:
            self.logger.debug("User not found", id=id_)
            return None
        self.logger.debug("User fetched", result=result, id=id_)
        return UserInfo(**result)

    async def from_role(self, role: str) -> list[UserInfo]:
        self.logger.debug("Try fetch", role=role)
        async with self.connection_pool.acquire() as con:
            result = await con.fetch("SELECT * FROM auth.user WHERE $1=ANY(roles)", role)
        if not result:
            self.logger.debug("Users not found", role=role)
            return []
        self.logger.debug("User fetched", result=result, role=role)
        return [UserInfo(**i) for i in result]
