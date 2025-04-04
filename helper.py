from pymongo import MongoClient
from datetime import datetime

connection = MongoClient("mongodb://localhost:27017/")
db = connection['option_chain']
collection = db['master_data']


def find_recent_put_expiry_contract(index, strike):
    if index == "SENSEX": 
        query = {
            "Name": index,
            "StrikePrice": str(strike),
            "Series": "IO",
            "OptionType": "4"
        }
    if index == "NIFTY" or index == "BANKNIFTY":
        query = {
            "Name": index,
            "StrikePrice": str(strike),
            "Series": "OPTIDX",
            "OptionType": "4"
        }
    contracts = list(collection.find(query))
    today = datetime.now()
    closest_contract = None
    min_diff = None
    for contract in contracts:
        expiration = datetime.fromisoformat(contract['ContractExpiration'])
        if expiration > today:  # Only consider future expiries
            diff = expiration - today
            if min_diff is None or diff < min_diff:
                min_diff = diff
                closest_contract = contract
    return closest_contract.get("ExchangeInstrumentID") if closest_contract else None

def find_recent_call_expiry_contract(index, strike):
    if index == "SENSEX": 
        query = {
            "Name": index,
            "StrikePrice": str(strike),
            "Series": "IO",
            "OptionType": "3"
        }
    if index == "NIFTY" or index == "BANKNIFTY":
        query = {
            "Name": index,
            "StrikePrice": str(strike),
            "Series": "OPTIDX",
            "OptionType": "3"
        }
    contracts = list(collection.find(query))
    today = datetime.now()
    closest_contract = None
    min_diff = None
    for contract in contracts:
        expiration = datetime.fromisoformat(contract['ContractExpiration'])
        if expiration > today:  # Only consider future expiries
            diff = expiration - today
            if min_diff is None or diff < min_diff:
                min_diff = diff
                closest_contract = contract
    return closest_contract.get("ExchangeInstrumentID") if closest_contract else None


if __name__ == "__main__":
    print(find_recent_put_expiry_contract("BANKNIFTY", 51100))