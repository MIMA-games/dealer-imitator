from redis import asyncio as aioredis

from dealer_imitator.common.utils import singleton
from dealer_imitator.connections.mongodb_conn import db


@singleton
class AsyncRedisConn:
    """
    Class for handling redis connection and caching information.
    """

    def __init__(self) -> None:
        self.cache: aioredis.Redis

    async def connect(self, db_url: str, max_connections: int = 12, reconnect=False):
        """
        Method for connection redis database.
        """
        if not hasattr(self, "cache") or reconnect:
            conn_poll = aioredis.BlockingConnectionPool.from_url(
                db_url, max_connections=max_connections, decode_responses=True
            )
            self.cache = await aioredis.Redis(connection_pool=conn_poll)
            return self.cache

    async def set(self, key, value):
        return await self.cache.execute_command("set", key, value, "ex", 1800)

    async def get(self, key):
        return await self.cache.get(key)

    async def flush(self):
        await self.cache.flushdb()


r = AsyncRedisConn()