""" Ticker data functions. """
import datetime
import logging
import pytz
import requests_cache
from tqdm import tqdm
import yfinance as yf

from config import CONFIG
import filters

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'taursus/1.0'

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
    return None

def fetch_tickers(tickers_list,
                  period="5d",
                  interval="15m",
                  group_by=None,
                  progress=False,
                  incremental=False):
    """
    Retrieves the real-time prices for multiple tickers using yfinance.

    Parameters:
        tickers (list): List of ticker symbols.
        period (enum string): Time period for the data.
        interval (str): Time interval between data points
        group_by (str): Group data by ticker or date (e.g. "ticker", "date").
        progress (bool): Show progress bar.

    Possible values for period and interval: see config.py

    Returns:
        dict: Dictionary with ticker symbols as keys and current prices as values.
    """
    if not tickers_list:
        return {}

    try:
        logging.info("Fetching tickers data for tickers: %s", ', '.join(tickers_list))
        data = yf.download(
            tickers=tickers_list,
            period=period,
            interval=interval,
            group_by=group_by,
            progress=progress,
            threads=CONFIG['CONNECTION_POOL_SIZE'],
            session=session
        )
        # If incremental=True, when the tickers list size mismatch or is empty, adjust period and interval until they match,
        # max attempt is 10
        if incremental:
            attempt = 1
            while len(data) != len(tickers_list) and attempt < 10:
                periods = CONFIG['TICKER_FETCHING_PERIODS']
                period = periods[attempt % len(periods)]

                data = yf.download(
                    tickers_list,
                    period=period,
                    interval="1d",
                    group_by=group_by,
                    progress=progress,
                    threads=CONFIG['CONNECTION_POOL_SIZE'],
                    session=session
                )
                attempt += 1
        return data
    except Exception as e:
        logging.error(f"Error fetching tickers: {e}")
        return {ticker: None for ticker in tickers_list}

def fetch_real_time_prices(tickers_list):
    """
    Retrieves the real-time prices for multiple tickers.

    Parameters:
        tickers_list (list): List of ticker symbols.

    Returns:
        dict: Dictionary with ticker symbols as keys and current prices as values.
    """
    try:
        data = fetch_tickers(tickers_list,
            period="1d",
            interval="1m",
            group_by='ticker',
            progress=False,
            incremental=True
        )
        prices = {}

        for ticker in tickers_list:
            try:
                ticker_data = data[ticker]
                latest_close = ticker_data['Close'].iloc[-1]
                prices[ticker] = latest_close
            except Exception as e:
                logging.error(f"Error extracting price for {ticker}: {e}, skipping...")
                continue

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
        'trailing_eps': info.get('trailingEps'),
        'earnings_growth': info.get('earningsGrowth'),
        'revenue_growth': info.get('revenueGrowth'),
        'current_ratio': info.get('currentRatio'),
        'short_ratio': info.get('shortRatio'),
        'debt_equity': info.get('debtToEquity'),
        'peg_ratio': info.get('trailingPegRatio'),
        'pb_ratio': info.get('priceToBook'),
        'pe_ratio': info.get('trailingPE'),
        'recommendation_mean': info.get('recommendationMean'),
        'return_on_equity': info.get('returnOnEquity'),
        'industry': info.get('industry'),
        'sector': info.get('sector'),
    }
    return fundamentals

def filter_tickers_by_fundamentals(tickers):
    """
    Retrieves tickers that pass the fundamental filters.

    Returns:
        list: List of tickers that meet fundamental criteria.
    """
    fundamental_tickers = []

    for ticker in tqdm(tickers):
        ticker_data = fetch_ticker(ticker)
        ticker_fundamentals = get_ticker_fundamentals(ticker_data)

        if ticker_fundamentals is not None and filters.fundamentals(ticker_fundamentals):
            fundamental_tickers.append(ticker)


    return fundamental_tickers
