import os
import logging
import socketio

from dealer_imitator.common.utils import singleton


@singleton
class SioConn:
    def __init__(self):
        self.sio: socketio.AsyncServer = self._connect_async_server()
        self.external_sio: socketio.AsyncRedisManager = (
            self._connect_async_redis_manager()
        )
        self.sio_app: socketio.ASGIApp

    def _connect_async_server(self) -> socketio.AsyncServer:
        logger = logging.getLogger("player_actions")
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        mgr = socketio.AsyncRedisManager(os.environ.get("DEALER_IMITATOR_WS_MESSAGE_QUEUE"))
        return socketio.AsyncServer(
            async_mode="asgi",
            cors_allowed_origins="*",
            client_manager=mgr,
            logger=True,
            engineio_logger=True,
        )

    def _connect_async_redis_manager(self) -> socketio.AsyncRedisManager:
        return socketio.AsyncRedisManager(
            os.environ.get("DEALER_IMITATOR_WS_MESSAGE_QUEUE"), write_only=True
        )

    def setup_sio_app(self) -> socketio.ASGIApp:
        sio_app = socketio.ASGIApp(self.sio)
        return sio_app

    async def send_event(self, event_name, data, room, external=False):
        if external:
            await self.external_sio.emit(event_name, data, room=room)
        else:
            await self.sio.emit(event_name, data, to=room)

    async def send_events(self, events: list):
        for event in events:
            await self.send_event(*event)


sio = SioConn()
