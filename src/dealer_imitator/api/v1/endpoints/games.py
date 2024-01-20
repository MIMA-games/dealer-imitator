from fastapi import APIRouter, Depends

from dealer_imitator.connections.async_redis_conn import r
from dealer_imitator.connections.mongodb_conn import db


router = APIRouter()


@router.get("/connect/{game_id}", status_code=200)
async def connect_dealer(game_id: str):
    return await db.get_game_by_id(game_id)


