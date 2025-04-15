from pymongo import MongoClient
from datetime import datetime
from redis_handler import get_redis_hash
import mibian as mb
from datetime import date, datetime

connection = MongoClient("mongodb://localhost:27017/")
db = connection['option_chain']
collection = db['master_data']

def find_recent_expiry(index, strike):
    if index == "NIFTY" or index == "BANKNIFTY":
        query = {
            "Name": index,
            "StrikePrice": str(strike),
            "Series": "OPTIDX"
        }
    if index == "SENSEX":
        query = {
            "Name": index,
            "StrikePrice": str(strike),
            "Series": "IO"
        }
    contracts = list(collection.find(query))
    today = datetime.now()
    closest_contract = None
    min_diff = None
    for contract in contracts:
        expiration = datetime.fromisoformat(contract['ContractExpiration'])
        if expiration > today: 
            diff = expiration - today
            if min_diff is None or diff < min_diff:
                min_diff = diff
                closest_contract = contract
    if closest_contract:
        return closest_contract.get("ContractExpiration")


def find_recent_put_expiry_contract(index, strike, expiry):
    if index == "SENSEX": 
        query = {
            "Name": index,
            "StrikePrice": str(strike),
            "Series": "IO",
            "OptionType": "4",
            "ContractExpiration": expiry
        }
    if index == "NIFTY" or index == "BANKNIFTY":
        query = {
            "Name": index,
            "StrikePrice": str(strike),
            "Series": "OPTIDX",
            "OptionType": "4",
            "ContractExpiration": expiry
        }
    contracts = list(collection.find(query))
    if len(contracts) != 0:
        closest_contract = contracts[0]
        return closest_contract.get("ExchangeInstrumentID")
    return "NA"


def find_recent_call_expiry_contract(index, strike, expiry):
    if index == "SENSEX": 
        query = {
            "Name": index,
            "StrikePrice": str(strike),
            "Series": "IO",
            "OptionType": "3",
            "ContractExpiration": expiry
        }
    if index == "NIFTY" or index == "BANKNIFTY":
        query = {
            "Name": index,
            "StrikePrice": str(strike),
            "Series": "OPTIDX",
            "OptionType": "3",
            "ContractExpiration": expiry
        }
    contracts = list(collection.find(query))
    if len(contracts) != 0:
        closest_contract = contracts[0]
        return closest_contract.get("ExchangeInstrumentID")
    return "0"

def update_call_in_df(
        segment_id, 
        instrument_id, 
        redis_connection,
        index_ltp,
        strike,
        contract_expiry_str
        ):
    
    market_data = get_redis_hash(f"{segment_id}_{instrument_id}", redis_connection)
    instrument_ltp = market_data.get("last_traded_price")
    interest_rate = 6
    now = datetime.now()
    contract_expiry = datetime.strptime(contract_expiry_str, "%Y-%m-%dT%H:%M:%S")
    time_diff = contract_expiry - now
    delta_expiry = time_diff.days + (time_diff.seconds / (24 * 3600))
    print(f"Days to expiry: {delta_expiry:.3f}")
    if delta_expiry <= 0:
        raise ValueError("Contract expiry must be a future date. The provided expiry date is not valid.")
    temp = mb.BS([index_ltp, strike, interest_rate, delta_expiry], callPrice=instrument_ltp)
    option_volatility = temp.impliedVolatility
    greeks_calc = mb.BS([index_ltp, strike, interest_rate, delta_expiry], volatility=option_volatility)    
    return {
        "instrument_ltp": instrument_ltp,
        "bid_price": market_data.get("bid_price"),
        "bid_quantity": market_data.get("bid_quantity"),
        "ask_price": market_data.get("ask_price"),
        "ask_quantity": market_data.get("ask_quantity"),
        "volume": market_data.get("volume"),
        "change": market_data.get("change"),
        "OI": market_data.get("OI"),
        "OI_Change": market_data.get("OI_change"),
        "delta": round(greeks_calc.callDelta, 2),
        "theta": round(greeks_calc.callTheta, 2),
        "gamma": round(greeks_calc.gamma, 6),
        "vega": round(greeks_calc.vega, 2),
        'IV': round(option_volatility, 2)
    }

def update_put_in_df(
        segment_id, 
        instrument_id, 
        redis_connection,
        index_ltp,
        strike,
        contract_expiry_str
        ):
    
    market_data = get_redis_hash(f"{segment_id}_{instrument_id}", redis_connection)
    instrument_ltp = market_data.get("last_traded_price")
    interest_rate = 6
    now = datetime.now()
    contract_expiry = datetime.strptime(contract_expiry_str, "%Y-%m-%dT%H:%M:%S")
    time_diff = contract_expiry - now
    delta_expiry = time_diff.days + (time_diff.seconds / (24 * 3600))
    print(f"Days to expiry: {delta_expiry:.3f}")
    if delta_expiry <= 0:
        raise ValueError("Contract expiry must be a future date. The provided expiry date is not valid.")
    temp = mb.BS([index_ltp, strike, interest_rate, delta_expiry], callPrice=instrument_ltp)
    option_volatility = temp.impliedVolatility
    greeks_calc = mb.BS([index_ltp, strike, interest_rate, delta_expiry], volatility=option_volatility)    
    return {
        "instrument_ltp": instrument_ltp,
        "bid_price": market_data.get("bid_price"),
        "bid_quantity": market_data.get("bid_quantity"),
        "ask_price": market_data.get("ask_price"),
        "ask_quantity": market_data.get("ask_quantity"),
        "volume": market_data.get("volume"),
        "change": market_data.get("change"),
        "OI": market_data.get("OI"),
        "OI_Change": market_data.get("OI_change"),
        "delta": round(greeks_calc.putDelta, 2),
        "theta": round(greeks_calc.putTheta, 2),
        "gamma": round(greeks_calc.gamma, 6),
        "vega": round(greeks_calc.vega, 2),
        'IV': round(option_volatility, 2)
    }

if __name__ == "__main__":
    print(find_recent_put_expiry_contract("BANKNIFTY", 51100))