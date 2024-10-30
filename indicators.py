"""Calculates technical indicators and generates price targets."""
import logging
import talib
import pandas as pd
import numpy as np
from ticker_data import fetch_tickers

def calculate_indicators(df):
    """
    Calculates technical indicators using TA-Lib.

    Parameters:
        df (DataFrame): DataFrame containing stock price data.

    Returns:
        DataFrame: DataFrame with added technical indicators.
    """
    close_values = df['Close'].values.flatten()
    df['RSI'] = talib.RSI(close_values, timeperiod=14)
    df['MACD'], df['MACD_signal'], _ = talib.MACD(close_values, fastperiod=12, slowperiod=26, signalperiod=9)
    df['SMA_50'] = talib.SMA(close_values, timeperiod=50)
    df['SMA_200'] = talib.SMA(close_values, timeperiod=200)
    df['ATR'] = talib.ATR(
        df['High'].values if 'High' in df.columns else np.array([df['Close'].iloc[-1]]),
        df['Low'].values if 'Low' in df.columns else np.array([df['Close'].iloc[-1]]),
        df['Close'].values, timeperiod=14)
    return df

def generate_price_targets(df):
    """
    Generates buy target price and stop-loss level using Average True Range (ATR).

    Parameters:
        df (DataFrame): DataFrame with price data and indicators.

    Returns:
        tuple: Buy target price and stop-loss level.
    """
    high = df['High'].values if 'High' in df.columns and df['High'].notna().any() else None
    low = df['Low'].values if 'Low' in df.columns and df['Low'].notna().any() else None
    if high is None or low is None:
        return None, None

    # Values rounded to 2 decimal places
    close = df['Close'].values
    atr = talib.ATR(high, low, close, timeperiod=14)
    current_price = close[-1]
    buy_target = current_price * 1.02  # Target price 2% higher
    stop_loss = current_price - 1.5 * atr[-1]  # Stop-loss at 1.5x ATR
    return buy_target, stop_loss

def generate_buy_targets(bullish_tickers, prices):
    buy_targets = []
    for ticker, data in bullish_tickers.items():
        price = prices.get(ticker)
        df = pd.DataFrame([data])
        df['Close'] = price

        # If data frame size is under the ATR period, we don't have enough data to generate targets
        # so we need to pull from a broader period
        if len(df) < 14 or np.isnan(price):
            extended_prices = fetch_tickers([ticker], period='1mo', interval='1d')
            # Validate that we have data for the ticker
            if ticker in extended_prices:
                df = pd.DataFrame(extended_prices[ticker])
                price = df['Close'].iloc[-1]
            else:
                logging.warning("No data found for ticker %s", ticker)
                continue
            
        buy_target, stop_loss = generate_price_targets(df)
        current_price = round(price, 2)
        buy_target = round(buy_target, 2)
        stop_loss = round(stop_loss, 2)
        risk = round(price - stop_loss, 2)
        reward = round(buy_target - current_price, 2)
        rrr = round(reward/risk, 2)
        buy_targets.append({
            'Ticker': ticker,
            'Signal': 'Buy',
            'Current Price': current_price,
            'Target Price': buy_target,
            'Stop-Loss': stop_loss,
            'Risk-Reward Ratio': rrr
        })

    return buy_targets

def generate_sell_targets(bearish_tickers, prices):
    sell_targets = []
    for ticker, data in bearish_tickers.items():
        price = prices.get(ticker)
        if price is None:
            continue
        current_price = round(price, 2)
        stop_loss = round(current_price*1.02, 2) # Stop-loss at 2% higher
        target_price = round(current_price*0.98, 2) # Target price 2% lower
        risk = round(current_price - stop_loss, 2)
        reward = round(target_price - current_price, 2)
        rrr = round(reward/risk, 2)
        sell_targets.append({
            'Ticker': ticker,
            'Signal': 'Sell',
            'Current Price': current_price,
            'Target Price': target_price,
            'Stop-Loss': stop_loss,
            'Risk-Reward Ratio': rrr
        })

    return sell_targets

def generate_targets(bullish_tickers, bearish_tickers, prices):
    buy_targets = generate_buy_targets(bullish_tickers, prices)
    sell_targets = generate_sell_targets(bearish_tickers, prices)
    return buy_targets, sell_targets
