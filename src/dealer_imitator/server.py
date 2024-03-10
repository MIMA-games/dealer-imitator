import os
import asyncio
import logging

from typing import Tuple

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dealer_imitator.connections.mongodb_conn import db
from dealer_imitator.connections.async_redis_conn import r
from dealer_imitator.api.v1.api import router as v1_router
from dealer_imitator.connections.sio_client import sio_client


def create_app() -> Tuple[FastAPI]:
    """
    function for seting up whole application.
    """


    fastapi_app = FastAPI(
        root_path="/dealer_imitator/api/v1"
        if os.environ.get("ENVIRONMENT") == "production"
        else ""
    )

    logging.basicConfig(level=logging.INFO)

    fastapi_app.include_router(
        v1_router,
        prefix="/v1" if not os.environ.get("ENVIRONMENT") == "production" else "",
    )
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=os.environ["ALLOWED_ORIGINS"].split(" "),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return fastapi_app


app = create_app()


@app.on_event("startup")
async def connect_db():
    """
    Function which runs only once when fastapi starts up.
    """
    await db.connect(os.environ["DEALER_IMITATOR_MONGODB_URL"], os.environ["DATABASE_NAME"])
    await r.connect(os.environ["REDIS_URL"])
    
    launched_games = await r.get_launched_games()
    for game in launched_games:
        print("Reconnection", game)
        game_type = game.split(":")[0]
        game_id = game.split(":")[1]
        asyncio.create_task(sio_client.start_socketio(game_type, game_id))
