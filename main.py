import asyncio
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import socketio

url = "http://localhost:8005"
transports = ["websocket"]
app = FastAPI()


sio_instances = {}


# Async function to start Socket.IO connection based on game_id
async def start_socketio(game_id: str):
    sio = socketio.AsyncClient()
    
    @sio.event
    async def connect():
        print(f'Connected to server for game_id={game_id}')

    @sio.event
    async def on_connect_data(data):
        print("data: ", data)


    @sio.event
    async def message(data):
        print(f'Message from server for game_id={game_id}:', data)

    @sio.event
    async def disconnect():
        print(f'Disconnected from server for game_id={game_id}')

    sio_instances[game_id] = sio
    print(url)
    await sio.connect(
        f"{url}/?game_id={game_id}&jwt_token=4793557e-1831-46cd-88f4-a69c69c9aa03",
        transports=transports,
        socketio_path="/ws/blackjack/socket.io",
        wait_timeout=10,
    )
    await sio.wait()

# FastAPI endpoint to start a new Socket.IO connection
@app.post("/connect/{game_id}")
async def connect_to_socketio(game_id: str):
    asyncio.create_task(start_socketio(game_id))
    return {"message": f"Connecting to Socket.IO for game_id={game_id}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
