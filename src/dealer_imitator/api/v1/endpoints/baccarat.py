import asyncio

from fastapi import APIRouter, Depends

from dealer_imitator.connections.async_redis_conn import r
from dealer_imitator.connections.mongodb_conn import db
from dealer_imitator.connections.sio_client import sio_client
from dealer_imitator.common.enums import Games
from dealer_imitator.common.cards.shoe import Shoe


router = APIRouter()


@router.get("/connect/{game_id}", status_code=200)
async def connect_dealer(game_id: str):
    shoe = Shoe.setup(6)
    await r.remove_all_remaining_cards(game_id)
    await r.add_initial_cards_list(game_id, list(shoe.shoe.keys()))

    asyncio.create_task(sio_client.start_socketio(Games.BACCARAT, game_id))

    return {"message": f"Connecting to Socket.IO for game_id={game_id}"}
