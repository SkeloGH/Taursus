"""Classify tickers as bullish or bearish based on indicators."""
import logging
import talib

from config import CONFIG
from ticker_data import get_tickers_historical_data

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
    close_prices = ticker_data['Close'].ffill().sort_index(ascending=True)
    rsi = talib.RSI(close_prices, timeperiod=CONFIG['RSI_PERIOD']).dropna()
    macd, macd_signal, _ = talib.MACD(close_prices,
                                      fastperiod=CONFIG['MACD_FAST_PERIOD'],
                                      slowperiod=CONFIG['MACD_SLOW_PERIOD'],
                                      signalperiod=CONFIG['MACD_SIGNAL_PERIOD'])

    close_price_value = close_prices.iloc[-1]
    close_rsi = rsi.iloc[-1]
    macd_value = macd.iloc[-1]
    macd_signal_value = macd_signal.iloc[-1]
    # These default to the last close price
    ticker_high = ticker_data['High'].iloc[-1] if 'High' in ticker_data else close_price_value
    ticker_low = ticker_data['Low'].iloc[-1] if 'Low' in ticker_data else close_price_value

    ticker_signals = {
            'RSI': close_rsi,
            'MACD': macd_value,
            'MACD Signal': macd_signal_value,
            'High': ticker_high,
            'Low': ticker_low,
            'Close': close_price_value
        }
    return ticker_signals

def classify_tickers(ticker_price_data,
                             rsi_buy=CONFIG['RSI_THRESHOLD_BUY'],
                             rsi_sell=CONFIG['RSI_THRESHOLD_SELL']):
    """
    Identifies bullish and bearish tickers, adapting criteria if necessary.

    Parameters:
        tickers_data (DataFrame): Downloaded data for tickers.
        rsi_buy (int): RSI buy threshold.
        rsi_sell (int): RSI sell threshold.

    Returns:
        tuple: Dictionaries of bullish and bearish tickers.
    """
    bullish_tickers = {}
    bearish_tickers = {}

    logging.info("Identifying bullish and bearish tickers...")
    for ticker in ticker_price_data:
        try:
            is_empty = ticker_price_data[ticker].empty
            is_rsi_compliant = len(ticker_price_data[ticker]) >= CONFIG['RSI_PERIOD']
            if is_empty or not is_rsi_compliant:
                continue
            ticker_signals = get_ticker_signals(ticker_price_data, ticker)
            rsi = ticker_signals['RSI']
            macd = ticker_signals['MACD']
            macd_signal = ticker_signals['MACD Signal']
            is_rsi_buy = rsi <= rsi_buy
            is_rsi_sell = rsi >= rsi_sell
            is_macd_buy = macd >= macd_signal
            is_macd_sell = macd <= macd_signal
            is_bullish = is_rsi_buy and is_macd_buy
            is_bearish = is_rsi_sell and is_macd_sell

            if is_bullish:
                bullish_tickers[ticker] = ticker_price_data[ticker]
            elif is_bearish:
                bearish_tickers[ticker] = ticker_price_data[ticker]
        except Exception as e:
            logging.error(f"Unexpected error processing {ticker}: {e}")
            continue

    return bullish_tickers, bearish_tickers

def get_bullish_bearish(ticker_objects):
    """
    This is the strategy that identifies bullish and bearish tickers.
    It is based on RSI and MACD over a month.

    Args:
        ticker_objects (list): List of yfinance.Ticker objects.

    Returns:
        tuple: Dictionaries of bullish and bearish tickers.
    """
    # Identify bullish and bearish tickers
    rsi_threshold_buy = CONFIG['RSI_THRESHOLD_BUY']
    rsi_threshold_sell = CONFIG['RSI_THRESHOLD_SELL']
    min_results = CONFIG['MIN_RESULTS']
    time_periods = ["1mo"]
    interval = ["30m"]
    attempts = 0
    bullish_tickers = {}
    bearish_tickers = {}

    # Try different time periods until we get enough bullish and bearish tickers
    while (len(bullish_tickers) < min_results or len(bearish_tickers) < min_results) and attempts < len(time_periods):
        # Adjust thresholds to be more lenient
        rsi_threshold_buy += (5 if attempts > 0 else 0)
        rsi_threshold_sell -= (5 if attempts > 0 else 0)
        logging.info(
            f"Attempt {attempts + 1}: "
            f"RSI thresholds - Buy < {rsi_threshold_buy}, Sell > {rsi_threshold_sell}, "
            f"Time period - {time_periods[attempts]}, "
            f"Interval - 1d"
        )
        if attempts < len(time_periods):
            ticker_price_data = get_tickers_historical_data(ticker_objects,
                                               period=time_periods[attempts],
                                               interval=interval[attempts])
            bullish_tickers, bearish_tickers = classify_tickers(ticker_price_data,
                                                                        rsi_buy=rsi_threshold_buy,
                                                                        rsi_sell=rsi_threshold_sell)
            attempts += 1

    logging.info(
        f"Final results - Bullish: {len(bullish_tickers)}, Bearish: {len(bearish_tickers)}"
    )

    return bullish_tickers, bearish_tickers
