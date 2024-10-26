import yfinance as yf
import time
import logging
import datetime
import pytz
import requests_cache
from concurrent.futures import ThreadPoolExecutor, as_completed


from config import CONFIG
from tickers import tickers
import filters

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'

def fetch_ticker_data(ticker_symbol, session=None):
    retry_attempts = CONFIG['RETRY_ATTEMPTS']
    for attempt in range(retry_attempts):
        try:
            ticker = yf.Ticker(ticker_symbol, session="test")
            info = ticker.info
            ticker_data = {
                'PE_ratio': info.get('trailingPE'),
                'PB_ratio': info.get('priceToBook'),
                'ROE': info.get('returnOnEquity', 0) * 100,
                'Current_Ratio': info.get('currentRatio'),
                'Debt_Equity': info.get('debtToEquity', 0) / 100
            }
            if filters.fundamentals(ticker_data):
                return ticker_symbol
            else:
                return None
        except Exception as e:
            logging.error(
                f"Error fetching data for {ticker_symbol}, attempt {attempt + 1}/{retry_attempts}: {e}"
            )
            time.sleep(2)
    return None

def get_nasdaq_assets():
    """
    Retrieves tickers that pass the fundamental filters using ThreadPoolExecutor.

    Returns:
        list: List of tickers that meet fundamental criteria.
    """
    fundamental_tickers = []

    # Limit the number of threads to limit the connection pool size
    max_workers = min(CONFIG['MAX_WORKERS'], len(tickers))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks to the executor
        future_to_ticker = {executor.submit(fetch_ticker_data, ticker): ticker for ticker in tickers}

        for future in as_completed(future_to_ticker):
            ticker_symbol = future_to_ticker[future]
            try:
                result = future.result()
                if result:
                    fundamental_tickers.append(result)
            except Exception as e:
                logging.error(f"Error processing ticker {ticker_symbol}: {e}")

    return fundamental_tickers

def fetch_tickers(tickers, period="5d", interval="15m", group_by=None, progress=False):
    """
    Retrieves the real-time prices for multiple tickers using yfinance.

    Parameters:
        tickers (list): List of ticker symbols.
        period (str): Time period for the data (e.g. "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max").
        interval (str): Time interval between data points (e.g. "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo").
        group_by (str): Group data by ticker or date (e.g. "ticker", "date").
        progress (bool): Show progress bar.

    Returns:
        dict: Dictionary with ticker symbols as keys and current prices as values.
    """
    if not tickers:
        return {}

    data = yf.download(
        tickers=tickers,
        period=period,
        interval=interval,
        group_by=group_by,
        progress=progress,
        threads=CONFIG['MAX_WORKERS']
    )
    return data


def get_real_time_prices(tickers):
    """
    Retrieves the real-time prices for multiple tickers.

    Parameters:
        tickers (list): List of ticker symbols.

    Returns:
        dict: Dictionary with ticker symbols as keys and current prices as values.
    """
    try:
        data = yf.download(
            tickers=tickers,
            period="1d",
            interval="1m",
            group_by='ticker',
            progress=False
        )
        prices = {}
        for ticker in tickers:
            try:
                ticker_data = data.xs(ticker, level=1, axis=1)
                latest_close = ticker_data['Close'].iloc[-1]
                prices[ticker] = latest_close
            except Exception as e:
                logging.error(f"Error extracting price for {ticker}: {e}")
                prices[ticker] = None
        return prices
    except Exception as e:
        logging.error(f"Error fetching real-time prices: {e}")
        return {ticker: None for ticker in tickers}


def is_market_open():
    """
    Checks if the market is currently open based on New York time.

    Returns:
        bool: True if the market is open, False otherwise.
    """
    ny_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
    if ny_time.weekday() < 5 and datetime.time(9, 30) <= ny_time.time() <= datetime.time(16, 0):
        return True
    return False
