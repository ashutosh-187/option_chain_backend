import socketio
import os 
from dotenv import load_dotenv
from redis_handler import (
    connect_with_redis_server,
    set_redis_hash,
    get_redis_hash
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
            if "t:" in web_socket_data[0]:
                segment = web_socket_data[0].replace("t:", "")
            for data in web_socket_data:
                if "bi:" in data:
                    bi = data.split("|")
                    bid_price = bi[1]
                    bid_quantity = bi[2]
                    continue
                if "ai:" in data:
                    ai = data.split("|")
                    ask_price = ai[1]
                    ask_quantity = ai[2]
                    continue
                if 'ltp:' in data:
                    ltp = data.replace("ltp:", "")
                    continue
                if "v:" in data:
                    volume = data.replace("v:", "")
                    continue
                if "pc:" in data:
                    change = data.replace("pc:", "")
                    continue
            market_data = {
                "segment_id": segment,
                "bid_price": bid_price,
                "bid_quantity": bid_quantity,
                "ask_price": ask_price,
                "ask_quantity": ask_quantity,
                "last_traded_price": ltp,
                "volume": volume,
                "change": change
            }
            set_redis_hash(segment, market_data, redis_connection)

    @sio.on("1510-json-partial")
    def on_message_from_1510(data):
        oi_data = data.split(",")
        if oi_data and oi_data[0].startswith("t:"):
            segment = oi_data[0][2:]
        if oi_data and oi_data[1].startswith("oi:"):
            oi_str = oi_data[1][3:]
        
        current_oi = float(oi_str)
        prev_data = get_redis_hash(segment, redis_connection)
        
        if prev_data.get("OI") == None:
            prev_data = 0
        else:
            prev_oi = float(prev_data.get("OI"))
        open_interest = {
            "OI": current_oi,
            "OI_change": current_oi - prev_oi
        }
        print(open_interest)
        set_redis_hash(segment, open_interest, redis_connection)

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