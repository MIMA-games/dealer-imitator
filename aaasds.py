import socketio


sio = socketio.Client()


@sio.event
def connect():
    print('Connected to server')


@sio.event
def on_connect_data(data):
    print("On connect data", data)


@sio.event
def message(data):
    print('Message from server:', data)


@sio.event
def error(data):
    print("Error: ", data)


@sio.event
def disconnect():
    print('Disconnected from server')


url = "http://localhost:8005"
transports = ["websocket"]


sio.connect(
    f"{url}/?game_id=651df594469589db0a4c7dab&jwt_token=4793557e-1831-46cd-88f4-a69c69c9aa03",
    transports=transports,
    socketio_path="/ws/blackjack/socket.io"
)

sio.wait()
