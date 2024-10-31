"""Classify tickers as bullish or bearish based on indicators."""
import logging
import talib

from config import CONFIG
from ticker_data import fetch_tickers

def classify_tickers(indicators):
    """
    Classifies tickers as bullish or bearish based on the given indicators.

    Args:
        indicators (pandas.DataFrame): Indicators to classify tickers with.

    Returns:
        tuple: Dictionaries of bullish and bearish tickers.
    """
    bullish_tickers = {}
    bearish_tickers = {}
    for ticker, data in indicators.items():
        if data['RSI'] < 30 and data['MACD'] > data['MACD_signal']:
            bullish_tickers[ticker] = data
        elif data['RSI'] > 70 and data['MACD'] < data['MACD_signal']:
            bearish_tickers[ticker] = data
    return bullish_tickers, bearish_tickers

def identify_bullish_bearish(data, tickers):
    """
    Identifies bullish and bearish tickers, adapting criteria if necessary.

    Parameters:
        data (DataFrame): Downloaded data for tickers.
        tickers (list): List of tickers to analyze.

    Returns:
        tuple: Dictionaries of bullish and bearish tickers.
    """
    bullish_tickers = {}
    bearish_tickers = {}
    rsi_threshold_buy = CONFIG['RSI_THRESHOLD_BUY']
    rsi_threshold_sell = CONFIG['RSI_THRESHOLD_SELL']
    time_periods = ["1d", "5d", "1mo"]
    interval = "5m"
    attempts = 0
    min_results = CONFIG['MIN_RESULTS']

    logging.info("Identifying bullish and bearish tickers...")

    while len(bullish_tickers) + len(bearish_tickers) < min_results and attempts < len(time_periods):
        logging.info(f"Attempt {attempts + 1}: RSI thresholds - Buy < {rsi_threshold_buy}, Sell > {rsi_threshold_sell}, Time period - {time_periods[attempts]}")
        for ticker in tickers:
            try:
                ticker_data = data[ticker]
                close_prices = ticker_data['Close'].ffill()
                rsi = talib.RSI(close_prices, timeperiod=14)
                macd, macd_signal, _ = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)

                close_prices_value = close_prices.iloc[-1]
                rsi_value = rsi.iloc[-1]
                macd_value = macd.iloc[-1]
                macd_signal_value = macd_signal.iloc[-1]
                ticker_high = ticker_data['High'].iloc[-1] if 'High' in ticker_data else close_prices_value
                ticker_low = ticker_data['Low'].iloc[-1] if 'Low' in ticker_data else close_prices_value

                if rsi_value < rsi_threshold_buy and macd_value > macd_signal_value:
                    bullish_tickers[ticker] = {
                        'RSI': rsi_value,
                        'MACD': macd_value,
                        'MACD Signal': macd_signal_value,
                        'High': ticker_high,
                        'Low': ticker_low,
                        'Close': close_prices_value
                    }
                elif rsi_value > rsi_threshold_sell and macd_value < macd_signal_value:
                    bearish_tickers[ticker] = {
                        'RSI': rsi_value,
                        'MACD': macd_value,
                        'MACD Signal': macd_signal_value,
                        'High': ticker_high,
                        'Low': ticker_low,
                        'Close': close_prices_value
                    }
            except KeyError as e:
                logging.error(f"Error processing data for {ticker}: {e}")
                continue
            except Exception as e:
                logging.error(f"Unexpected error processing {ticker}: {e}")
                continue

        if len(bullish_tickers) + len(bearish_tickers) < min_results:
            # Adjust thresholds to be more lenient
            rsi_threshold_buy += 5
            rsi_threshold_sell -= 5
            attempts += 1
            if attempts < len(time_periods):
                logging.info(f"Adjusting data period to {time_periods[attempts]} and retrying...")
                data = fetch_tickers(tickers, period=time_periods[attempts], interval=interval, group_by='ticker', progress=False)

    return bullish_tickers, bearish_tickers
