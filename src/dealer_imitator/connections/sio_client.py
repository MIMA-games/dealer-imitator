import os
import asyncio
import socketio
import logging

from fastapi.logger import logger

from dealer_imitator.common.enums import GameStates
from dealer_imitator.common.managers.dealer_manager import DealerManager
from dealer_imitator.common.enums import SendEvents, ActionTypes
from dealer_imitator.models.events.send import ScanCardModel


class SioClient:
    GAMES = {
        "blackjack": {
            "url": os.environ.get("BLACKJACK_BACKEND_URL"),
            "socketio_path": "/ws/blackjack/socket.io"
        }
    }

    round_id = None


    async def _generate_scan_card_event(self, game_id: str):
        new_card = await DealerManager(game_id).generate_new_card()
        event_data = ScanCardModel(card=new_card, round_id=self.round_id)
        return event_data.dict()

    async def _scan_dealer_card(self, game_id: str, sio: socketio.AsyncClient, ):
        await asyncio.sleep(0.5)
        event_data = await self._generate_scan_card_event(game_id)
        await sio.emit(SendEvents.DEALER_CARDS, event_data)
        logger.info(f"Scanning DEALER card {event_data}")
    
    async def _scan_card(self, game_id: str, sio: socketio.AsyncClient):
        await asyncio.sleep(0.5)
        event_data = await self._generate_scan_card_event(game_id)
        await sio.emit(SendEvents.SCAN_CARD, event_data)
        logger.info(f"Dealing INITIAL cards {event_data}")
    
    async def _scan_action_card(self, game_id: str, sio: socketio.AsyncClient):
        await asyncio.sleep(0.5)
        event_data = await self._generate_scan_card_event(game_id)
        await sio.emit(SendEvents.ACTION_CARDS, event_data) 
        logger.info(f"Dealing ACTION card {event_data}")
            
    async def start_socketio(self, game: str, game_id: str):
        sio = socketio.AsyncClient()

        @sio.event
        async def connect():
            logger.debug("miro")
            logger.info("Connected to the server")
        
        @sio.event
        async def on_connect_data(data):
            logger.info(f"Connected to the game with a state - {data['game_state']}")
            self.round_id = data["round_id_long"]

            if data["game_state"] == GameStates.DEALING.value:
                await self._scan_card(game_id, sio)
            elif data["game_state"] == GameStates.WAITING_DEALER_SCAN_DEALER_CARD.value:
                await self._scan_dealer_card(game_id, sio)
            elif data["game_state"] == GameStates.WAITING_DEALER_SCAN_PLAER_CARD.value:
                await self._scan_action_card(game_id, sio)

        @sio.event
        async def start_dealing(data):
            logger.info("Start Dealing")
            await self._scan_card(game_id, sio)
        
        @sio.event
        async def request_card(dara):
            await self._scan_card(game_id, sio)
        
        @sio.event
        async def change_state(data):
            if data["state"] == GameStates.SHUFFLING.value:
                await DealerManager(game_id).shuffle()
                logger.info("Shuffled")
        
        @sio.event
        async def scan_dealer_card(data):
            await self._scan_dealer_card(game_id, sio)
        
        @sio.event
        async def start_new_round(data):
            self.round_id = data["round_id_long"]
            logger.info("Round Updated")
        
        @sio.event
        async def player_action(data):
            if any([
                data["action_type"] == ActionTypes.HIT,
                data["action_type"] == ActionTypes.DOUBLE,
            ]):
                await self._scan_action_card(game_id, sio)
            elif data ["action_type"] == ActionTypes.SPLIT:
                for _ in range(2):
                    await self._scan_action_card(game_id, sio)

        @sio.event
        async def message(data):
            print(data)
        
        @sio.event
        async def error(data):
            print(data)
        
        @sio.event
        async def disconnect(data):
            print(data)
        
        await sio.connect(
            f"{self.GAMES[game]['url']}/?game_id={game_id}&jwt_token=4793557e-1831-46cd-88f4-a69c69c9aa03",
            transports=["websocket"],
            socketio_path=self.GAMES[game]["socketio_path"],
            wait_timeout=10,
        )
        await sio.wait()

        # Should send a send_card event

sio_client = SioClient()
