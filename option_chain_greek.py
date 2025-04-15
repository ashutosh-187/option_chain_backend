import mibian as mb
from datetime import date, datetime

def find_greek_symbols(index_ltp, strike, contract_expiry_str, ltp, option_type="call"):
    interest_rate = 6  # Annual interest rate
    
    # Get the current time (date and time)
    now = datetime.now()
    contract_expiry = datetime.strptime(contract_expiry_str, "%Y-%m-%dT%H:%M:%S")
    
    # Calculate the time difference in days with decimal precision
    time_diff = contract_expiry - now
    delta_expiry = time_diff.days + (time_diff.seconds / (24 * 3600))
    print(f"Days to expiry: {delta_expiry:.3f}")
    
    # Check if the contract expiry is valid (must be in the future)
    if delta_expiry <= 0:
        raise ValueError("Contract expiry must be a future date. The provided expiry date is not valid.")
    
    # Compute implied volatility using mibian's BS class
    if option_type.lower() == "call":
        temp = mb.BS([index_ltp, strike, interest_rate, delta_expiry], callPrice=ltp)
    else:  # put option
        temp = mb.BS([index_ltp, strike, interest_rate, delta_expiry], putPrice=ltp)
    
    option_volatility = temp.impliedVolatility
    print(f"Calculated Implied Volatility: {option_volatility}")
    
    # Calculate Greeks based on the computed volatility
    greeks_calc = mb.BS([index_ltp, strike, interest_rate, delta_expiry], volatility=option_volatility)
    
    # Create the greeks dictionary based on option type
    greeks = {
        "IV": option_volatility
    }
    
    if option_type.lower() == "call":
        greeks.update({
            "delta": greeks_calc.callDelta,
            "theta": greeks_calc.callTheta,
            "gamma": greeks_calc.gamma,
            "vega": greeks_calc.vega,
        })
    else:  # put option
        greeks.update({
            "delta": greeks_calc.putDelta,
            "theta": greeks_calc.putTheta,
            "gamma": greeks_calc.gamma,
            "vega": greeks_calc.vega,
        })
        
    return greeks

if __name__ == "__main__":
    result = find_greek_symbols(23328.95, 23350, '2025-04-17T14:30:00', 84.40)
    if result:
        print("Calculated Greeks and Implied Volatility:")
        print(result)
