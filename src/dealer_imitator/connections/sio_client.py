import os
import socketio

from dealer_imitator.common.enums import GameStates
from dealer_imitator.common.managers.dealer_manager import DealerManager


class SioClient:
    GAMES = {
        "blackjack": {
            "url": os.environ.get("BLACKJACK_BACKEND_URL"),
            "socketio_path": "/ws/blackjack/socket.io"
        }
    }

    async def start_socketio(self, game: str, game_id: str):
        sio = socketio.AsyncClient()

        @sio.event
        async def connect():
            print("Connected to server")
        
        @sio.event
        async def on_connect_data(data):
            if data["game_state"] == GameStates.DEALING.value:
                new_card = await DealerManager(game_id).generate_new_card()
                print(new_card)

        @sio.event
        async def message(data):
            print(data)
        
        @sio.event
        async def error(data):
            print(data)
        
        @sio.event
        async def disconnect(data):
            print(data)
        
        print( f"{self.GAMES[game]['url']}/?game_id={game_id}&jwt_token=4793557e-1831-46cd-88f4-a69c69c9aa03")
        print(self.GAMES[game]["socketio_path"])
        await sio.connect(
            f"{self.GAMES[game]['url']}/?game_id={game_id}&jwt_token=4793557e-1831-46cd-88f4-a69c69c9aa03",
            transports=["websocket"],
            socketio_path=self.GAMES[game]["socketio_path"],
            wait_timeout=10,
        )
        await sio.wait()

sio_client = SioClient()
