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
    
    async def add_initial_cards_list(self, game_id: str, cards: list[str]):
        await self.cache.rpush(game_id, *cards)
    
    async def remove_card_from_list(self, game_id: str, card: str):
        await self.cache.lrem(game_id, 0, card)
    
    async def get_remaining_cards_list(self, game_id: str):
        return await self.cache.lrange(game_id, 0, -1)
    
    async def remove_all_remaining_cards(self, game_id: str):
        await self.cache.delete(game_id)
    
    async def add_launched_game_to_the_list(self, game_type: str, game_id: str):
        await self.cache.rpush("games", f"{game_type}:{game_id}")
    
    async def get_launched_games(self):
        return await self.cache.lrange("games", 0, -1)

    async def flush(self):
        await self.cache.flushdb()


r = AsyncRedisConn()
