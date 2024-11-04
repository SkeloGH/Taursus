""" Ticker data functions. """
import datetime
import logging
import pytz
import requests_cache
import pandas as pd
import numpy as np

import yfinance as yf

from config import CONFIG


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
        incremental (bool): If True, adjust period and interval until they match

    Possible values for period and interval: see config.py

    Returns:
        dict: Dictionary with ticker symbols as keys and current prices as values.
    """
    threads = CONFIG['CONNECTION_POOL_SIZE']
    periods = CONFIG['TICKER_FETCHING_PERIODS']
    max_attempts = CONFIG['RETRY_ATTEMPTS']
    if not tickers_list:
        return {}

    try:
        logging.info("Fetching tickers data for %d tickers...", len(tickers_list))
        data = yf.download(
            tickers=tickers_list,
            period=period,
            interval=interval,
            group_by=group_by,
            progress=progress,
            threads=threads,
            session=session
        )
        # If incremental=True, when the tickers list size mismatch or is empty,
        # adjust period and interval until they match,
        # max attempt is 10
        if incremental:
            attempt = 1
            while len(data) != len(tickers_list) and attempt < max_attempts:
                period = periods[attempt % len(periods)]

                data = yf.download(
                    tickers_list,
                    period="1mo",
                    interval="1d",
                    group_by=group_by,
                    progress=progress,
                    threads=threads,
                    session=session
                )
                attempt += 1
        return data
    except Exception as e:
        logging.error(f"Error fetching tickers: {e}")
        return {ticker: None for ticker in tickers_list}

def fetch_tickers_prices(tickers_list):
    """
    Retrieves the real-time prices for multiple tickers.

    Parameters:
        tickers_list (list): List of ticker symbols.

    Returns:
        dict: Dictionary with ticker symbols as keys and current prices as values.
    """
    atr_period = 14
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
                if len(prices) < atr_period or np.isnan(latest_close):
                    ticker_data = fetch_ticker(ticker)
                    extended_prices = ticker_data.history(period='1mo', interval='1d')
                    # Validate that we have at least 14 days of data
                    if len(extended_prices) >= atr_period:
                        df = pd.DataFrame(extended_prices)
                        prices[ticker] = df['Close'].iloc[-1]
                    else:
                        logging.warning("No data found for ticker %s", ticker)
                        continue
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
