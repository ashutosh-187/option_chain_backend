from subscription import subscribe_instruments
from redis_handler import (
    connect_with_redis_server,
    redis_get
)
from helper import (
    find_recent_put_expiry_contract,
    find_recent_call_expiry_contract
)
from get_access_token import (
    generate_access_token
)
import pandas as pd

def option_chain(index):
    redis_connection = connect_with_redis_server()
    if index == "BANKNIFTY":
        index_id = 1
        segment_id = 2
        index_instrument_id = 26001
    if index == "NIFTY":
        index_id = 1
        segment_id = 2
        index_instrument_id = 26000
    if index == "SENSEX":
        index_id = 11
        segment_id = 12
        index_instrument_id = 26065
    subscribe_index = [
        {
            "exchangeSegment": index_id,
            "exchangeInstrumentID": index_instrument_id
        },
    ]
    subscribe_instruments(subscribe_index)
    ltp = float(redis_get(f"{index_id}_{index_instrument_id}", redis_connection))
    print(f"Option chain for {index}")
    if index == "BANKNIFTY":
        strike_distance = 100
    if index == "NIFTY":
        strike_distance = 50
    if index == "SENSEX":
        strike_distance = 100
    atm = round(ltp/strike_distance)*strike_distance
    print(f"{index} ltp =>", ltp)
    print(f"{index} atm =>", atm)
    print(f"{index} spot =>", atm)
    strike_range = [atm + (i * strike_distance) for i in range(-5, 6)]
    option_chain_df = pd.DataFrame()
    option_chain_df['strike'] = strike_range
    option_chain_df['put'] = option_chain_df["strike"].apply(
        lambda strike: find_recent_put_expiry_contract(index, strike)
    )
    option_chain_df['call'] = option_chain_df["strike"].apply(
        lambda strike: find_recent_call_expiry_contract(index, strike)
    )
    call_instrument_id = option_chain_df['call'].to_list()
    put_instrument_id = option_chain_df['put'].to_list()
    total_instrument_id = call_instrument_id + put_instrument_id
    subscription_list = []
    for subscribe_id in total_instrument_id:
        subscription_list.append(
            {
                "exchangeSegment": segment_id,
                "exchangeInstrumentID": subscribe_id
            }
        )
    subscribe_instruments(subscription_list)
    option_chain_df['call_ltp'] = option_chain_df['call'].apply(
        lambda instrument_id: redis_get(f"{segment_id}_{instrument_id}", redis_connection)
    )
    option_chain_df['put_ltp'] = option_chain_df['put'].apply(
        lambda instrument_id: redis_get(f"{segment_id}_{instrument_id}", redis_connection)
    )
    option_chain_df.fillna(0)
    return {
        "spot": atm,
        "option_chain": option_chain_df.to_dict(orient="records")
    }

if __name__ == "__main__":
    print(option_chain("BANKNIFTY"))