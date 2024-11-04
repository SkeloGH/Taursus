"""Classify tickers as bullish or bearish based on indicators."""
import logging
import talib

from config import CONFIG
from ticker_data import fetch_tickers

def get_ticker_signals(data, ticker):
    """
    Gets the signals for a given ticker.

    Args:
        data (pandas.DataFrame): Data for the ticker.
        ticker (str): Ticker symbol.

    Returns:
        dict: Dictionary of signals for the ticker.
    """
    ticker_data = data[ticker]
    close_prices = ticker_data['Close'].ffill()
    rsi = talib.RSI(close_prices, timeperiod=CONFIG['RSI_PERIOD'])
    macd, macd_signal, _ = talib.MACD(close_prices,\
                                      fastperiod=CONFIG['MACD_FAST_PERIOD'],\
                                        slowperiod=CONFIG['MACD_SLOW_PERIOD'],\
                                        signalperiod=CONFIG['MACD_SIGNAL_PERIOD'])

    close_prices_value = close_prices.iloc[-1]
    rsi_value = rsi.iloc[-1]
    macd_value = macd.iloc[-1]
    macd_signal_value = macd_signal.iloc[-1]
    # These default to the last close price
    ticker_high = ticker_data['High'].iloc[-1] if 'High' in ticker_data else close_prices_value
    ticker_low = ticker_data['Low'].iloc[-1] if 'Low' in ticker_data else close_prices_value

    ticker_signals = {
            'RSI': rsi_value,
            'MACD': macd_value,
            'MACD Signal': macd_signal_value,
            'High': ticker_high,
            'Low': ticker_low,
            'Close': close_prices_value
        }
    return ticker_signals

def identify_bullish_bearish(data,
                             tickers,
                             rsi_buy=CONFIG['RSI_THRESHOLD_BUY'],
                             rsi_sell=CONFIG['RSI_THRESHOLD_SELL']):
    """
    Identifies bullish and bearish tickers, adapting criteria if necessary.

    Parameters:
        data (DataFrame): Downloaded data for tickers.
        tickers (list): List of tickers to analyze.
        rsi_buy (int): RSI buy threshold.
        rsi_sell (int): RSI sell threshold.

    Returns:
        tuple: Dictionaries of bullish and bearish tickers.
    """
    bullish_tickers = {}
    bearish_tickers = {}
    rsi_threshold_buy = rsi_buy
    rsi_threshold_sell = rsi_sell

    logging.info("Identifying bullish and bearish tickers...")
    for ticker in tickers:
        try:
            ticker_signals = get_ticker_signals(data, ticker)
            is_rsi_buy = ticker_signals['RSI'] <= rsi_threshold_buy
            is_rsi_sell = ticker_signals['RSI'] >= rsi_threshold_sell
            is_macd_buy = ticker_signals['MACD'] >= ticker_signals['MACD Signal']
            is_macd_sell = ticker_signals['MACD'] <= ticker_signals['MACD Signal']

            if is_rsi_buy and is_macd_buy:
                bullish_tickers[ticker] = ticker_signals
            elif is_rsi_sell and is_macd_sell:
                bearish_tickers[ticker] = ticker_signals
        except KeyError as e:
            logging.error(f"Error processing data for {ticker}: {e}")
            continue
        except Exception as e:
            logging.error(f"Unexpected error processing {ticker}: {e}")
            continue

    return bullish_tickers, bearish_tickers

def classify_tickers(data, tickers):
    """
    Classifies tickers as bullish or bearish based on the given indicators.

    Args:
        data (pandas.DataFrame): Data for tickers.
        tickers (list): List of tickers to classify.

    Returns:
        tuple: Dictionaries of bullish and bearish tickers.
    """
    # Identify bullish and bearish tickers
    time_periods = ["1d", "5d", "1mo"]
    interval = "5m" # I removed the refetch call
    rsi_threshold_buy = CONFIG['RSI_THRESHOLD_BUY']
    rsi_threshold_sell = CONFIG['RSI_THRESHOLD_SELL']
    attempts = 0
    min_results = CONFIG['MIN_RESULTS']
    bullish_tickers, bearish_tickers = identify_bullish_bearish(data, tickers)
    combined_tickers = list(bullish_tickers.keys()) + list(bearish_tickers.keys())

    while (len(bullish_tickers) < min_results or len(bearish_tickers) < min_results) and attempts < len(time_periods):
        logging.info(
            f"Attempt {attempts + 1}: "
            f"RSI thresholds - Buy < {rsi_threshold_buy}, Sell > {rsi_threshold_sell}, "
            f"Time period - {time_periods[attempts]}"
        )
        # Adjust thresholds to be more lenient
        rsi_threshold_buy += 5
        rsi_threshold_sell -= 5
        attempts += 1
        if attempts < len(time_periods):
            logging.info(f"Adjusting data period to {time_periods[attempts]} and retrying...")
            data = fetch_tickers(tickers, time_periods[attempts], interval)
            bullish_tickers, bearish_tickers = identify_bullish_bearish(data, combined_tickers)

    logging.info(
        f"Final results - Bullish: {len(bullish_tickers)}, Bearish: {len(bearish_tickers)}"
    )

    return combined_tickers, bullish_tickers, bearish_tickers
