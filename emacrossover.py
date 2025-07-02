import time
import ccxt
from tradingview_ta import TA_Handler, Interval

# Initialize the Binance exchange with ccxt
exchange_ccxt = ccxt.binance()

def fetch_indicators(tv_symbol, screener, exchange, interval, ccxt_symbol):
    try:
        # Initialize TA_Handler for the given TradingView symbol
        analysis = TA_Handler(
            symbol=tv_symbol,
            screener=screener,
            exchange=exchange,
            interval=interval
        )
        
        # Fetch the indicators
        indicators = analysis.get_analysis().indicators
        
        # Extract specific values
        ema10 = indicators.get("EMA10")
        ema20 = indicators.get("EMA20")
        ema50 = indicators.get("EMA50")
        ema100 = indicators.get("EMA100")
        
        # Get the current price using ccxt
        try:
            current_price = exchange_ccxt.fetch_ticker(ccxt_symbol)['last']
        except Exception as e:
            return {"error": f"Failed to fetch current price: {str(e)}"}
        
        return {
            "EMA10": ema10,
            "EMA20": ema20,
            "EMA50": ema50,
            "EMA100": ema100,
            "current_price": current_price,
        }
    except Exception as e:
        return {"error": str(e)}

def check_crossovers(prev_indicators, current_indicators):
    crossover_10_20 = False
    crossover_50_100 = False

    if prev_indicators and current_indicators:
        prev_ema10 = prev_indicators.get("EMA10")
        prev_ema20 = prev_indicators.get("EMA20")
        prev_ema50 = prev_indicators.get("EMA50")
        prev_ema100 = prev_indicators.get("EMA100")

        curr_ema10 = current_indicators.get("EMA10")
        curr_ema20 = current_indicators.get("EMA20")
        curr_ema50 = current_indicators.get("EMA50")
        curr_ema100 = current_indicators.get("EMA100")

        # Check for crossover between EMA10 and EMA20
        if prev_ema10 is not None and prev_ema20 is not None:
            if (prev_ema10 < prev_ema20 and curr_ema10 > curr_ema20) or (prev_ema10 > prev_ema20 and curr_ema10 < curr_ema20):
                crossover_10_20 = True

        # Check for crossover between EMA50 and EMA100
        if prev_ema50 is not None and prev_ema100 is not None:
            if (prev_ema50 < prev_ema100 and curr_ema50 > curr_ema100) or (prev_ema50 > prev_ema100 and curr_ema50 < curr_ema100):
                crossover_50_100 = True

    return crossover_10_20, crossover_50_100

def check_price_in_zone(indicators):
    ema20 = indicators.get("EMA20")
    ema50 = indicators.get("EMA50")
    current_price = indicators.get("current_price")

    if None in [ema20, ema50, current_price]:
        return False

    return ema20 < current_price < ema50

# Continuous live fetching with added conditions
def continuous_fetch(tv_symbol, screener, exchange, interval, ccxt_symbol, delay=5):
    print(f"Starting live data fetch for {tv_symbol} every {delay} seconds...")

    previous_indicators = None

    try:
        markets = exchange_ccxt.load_markets()
        if ccxt_symbol not in markets:
            raise ValueError(f"Symbol '{ccxt_symbol}' not found on the exchange.")

        print(f"Symbol '{ccxt_symbol}' found on Binance exchange.")

        while True:
            current_indicators = fetch_indicators(tv_symbol, screener, exchange, interval, ccxt_symbol)
            if "error" in current_indicators:
                print(f"Error: {current_indicators['error']}")
                break

            print("Live Indicators:")
            print(current_indicators)
            print("-" * 40)

            # Check crossovers
            crossover_10_20, crossover_50_100 = check_crossovers(previous_indicators, current_indicators)

            if crossover_10_20:
                print("Crossover Detected: EMA10 and EMA20 crossed.")
            if crossover_50_100:
                print("Crossover Detected: EMA50 and EMA100 crossed.")

            # Check if the current price is in the retracement zone
            if check_price_in_zone(current_indicators):
                print("Condition: Current price is in the retracement zone (between EMA20 and EMA50).")
            else:
                print("Condition: Current price is not in the retracement zone.")

            print("-" * 40)

            # Update previous indicators
            previous_indicators = current_indicators

            time.sleep(delay)  # Delay between fetches (in seconds)
    except KeyboardInterrupt:
        print("Live fetching stopped.")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Live fetching stopped.")

# Parameters for fetching
tv_symbol = "BTCUSDT"  # Symbol format for TradingView
ccxt_symbol = "BTC/USDT"  # Symbol format for ccxt
screener = "crypto"
exchange = "Binance"
interval = Interval.INTERVAL_1_MINUTE

# Start continuous fetching
continuous_fetch(tv_symbol, screener, exchange, interval, ccxt_symbol, delay=5)
