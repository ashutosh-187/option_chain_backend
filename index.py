import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def load_access_token():
    with open('access_token.json', 'r') as file:
        data = json.load(file)
        return data['access_token']
    
def get_indexes(exchange_segment):
    token = load_access_token()
    headers = {
            "Content-Type": "application/json",
            "Authorization": token 
    }
    index_url = os.getenv("xts_url") + "/instruments/indexlist"
    params = {
        "exchangeSegment": exchange_segment
    }
    index_response = requests.get(index_url, headers=headers, params=params)
    index_json = index_response.json()
    # if int(index_json.get('result').get("exchangeSegment")) == 11:
    #     index = index_json.get("result").get("indexList")[0]
    # elif int(index_json.get('result').get("exchangeSegment")) == 1:
    #     index = index_json.get("result").get("indexList")[0:2]
    # if exchange_segment == 1:
    #     index_id = {
    #         "NIFTY": index[0].replace("NIFTY 50_", ""),
    #         "NIFTY_BANK": index[1].replace("NIFTY BANK_", "")
    #     }
    # if exchange_segment == exchange_segment:
    #     index_id = {
    #         "SENSEX": index.replace("SENSEX_", "")
    #     }
    print(index_json)
    return index_json

if __name__ =="__main__":
    get_indexes(11)