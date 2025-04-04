import socketio
import os 
from dotenv import load_dotenv
from redis_handler import (
    connect_with_redis_server,
    redis_push
)
from get_access_token import (
    generate_access_token,
    load_access_token
)

load_dotenv()

sio = socketio.Client()

def web_socket():
    token = generate_access_token()
    access_token = load_access_token()
    userID = os.getenv("userID")
    publishFormat = "JSON"
    broadcastFormat = "Partial"
    url = os.getenv("xts_url")

    socket_connection_url = f"{url}/?token={access_token}&userID={userID}&publishFormat={publishFormat}&broadcastMode={broadcastFormat}"
    redis_connection = connect_with_redis_server()

    @sio.on('connect')
    def connect(data=None):
        print("connected with websocket...")

    @sio.event
    def connect_error(data):
        print('Connection failed:', data)

    @sio.event
    def disconnect():
        print("disconnected with websocket...")

    @sio.on('1501-json-partial')
    def on_message_from_1501(data):
        if isinstance(data, str):
            web_socket_data = data.split(",")
            print(web_socket_data)
            if 'ltp:' in web_socket_data[1]:
                ltp = web_socket_data[1].replace("ltp:", "")
                segment = web_socket_data[0].replace("t:", "")
                redis_push(key=segment, value=ltp, redis_server=redis_connection)

    sio.connect(
        socket_connection_url,
        headers={},
        namespaces=None,
        transports='websocket',
        socketio_path='/apimarketdata/socket.io'
    )

    sio.wait()

if __name__ == "__main__":
    web_socket()