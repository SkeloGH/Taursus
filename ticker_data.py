""" Ticker data functions. """
import datetime
import logging
import time
import pytz
import requests_cache
from tqdm import tqdm
import yfinance as yf

from config import CONFIG
import filters

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'

def fetch_ticker(ticker_symbol):
    """
    Fetches ticker data using yfinance.

    Parameters:
        ticker_symbol (str): Ticker symbol to fetch data for.
        session (Session): Session object to use for fetching data.

    Returns:
        Ticker: Ticker object containing financial data.
    """
    retry_attempts = CONFIG['RETRY_ATTEMPTS']
    for attempt in range(retry_attempts):
        try:
            ticker_data = yf.Ticker(ticker_symbol, session=session)
            # Ticker might not exist or has been delisted, also ticker might return as a string
            if not ticker_data.info or isinstance(ticker_data.info, str):
                logging.warning("Ticker %s does not exist or has been delisted.", ticker_symbol)
                return None
            return ticker_data
        except Exception as e:
            logging.error(
                "Error fetching data for %s, attempt %d/%d: %s",
                ticker_symbol, attempt + 1, retry_attempts, e
            )
            time.sleep(2)
    return None

def fetch_tickers(tickers_list, period="5d", interval="15m", group_by=None, progress=False):
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
    if not tickers_list:
        return {}

    data = yf.download(
        tickers=tickers_list,
        period=period,
        interval=interval,
        group_by=group_by,
        progress=progress,
        threads=CONFIG['CONNECTION_POOL_SIZE']
    )
    return data

def fetch_real_time_prices(tickers_list):
    """
    Retrieves the real-time prices for multiple tickers.

    Parameters:
        tickers_list (list): List of ticker symbols.

    Returns:
        dict: Dictionary with ticker symbols as keys and current prices as values.
    """
    try:
        data = yf.download(
            tickers=tickers_list,
            period="1d",
            interval="1m",
            group_by='ticker',
            progress=False,
            threads=CONFIG['CONNECTION_POOL_SIZE']
        )
        prices = {}
        for ticker in tickers_list:
            try:
                ticker_data = data[ticker]
                if ticker_data.empty:
                    prices[ticker] = None
                else:
                    latest_close = ticker_data['Close'].iloc[-1]
                    prices[ticker] = latest_close
            except Exception as e:
                logging.error(f"Error extracting price for {ticker}: {e}")
                prices[ticker] = None
        return prices
    except Exception as e:
        logging.error(f"Error fetching real-time prices: {e}")
        return {ticker: None for ticker in tickers_list}

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

def get_ticker_fundamentals(ticker_data):
    """
    Retrieves fundamental data for a ticker.

    Parameters:
        ticker_data (Ticker): Ticker object containing financial data.

    Returns:
        dict: Dictionary with fundamental data for the ticker.
    """
    info = ticker_data.info
    fundamentals = {
        'PE_ratio': info.get('trailingPE'),
        'PB_ratio': info.get('priceToBook'),
        'ROE': info.get('returnOnEquity', 0) * 100,
        'Current_Ratio': info.get('currentRatio'),
        'Debt_Equity': info.get('debtToEquity', 0) / 100
    }
    return fundamentals

def get_tickers_fundamentals(tickers):
    """
    Retrieves tickers that pass the fundamental filters.

    Returns:
        list: List of tickers that meet fundamental criteria.
    """
    fundamental_tickers = []

    for ticker in tqdm(tickers):
        # fetch ticker data
        ticker_data = fetch_ticker(ticker)
        ticker_fundamentals = get_ticker_fundamentals(ticker_data)

        # check if ticker passes fundamental filters
        if ticker_fundamentals is not None and filters.fundamentals(ticker_fundamentals):
            fundamental_tickers.append(ticker)


    return fundamental_tickers
