import pdb
import yfinance as yf
import talib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import logging
import datetime
import pytz
from tickers import tickers

# Ensure tickers is a list of strings
tickers = list(tickers)

# Set up logging
logging.basicConfig(filename='trading_decision_log.txt', level=logging.INFO)

# Define fundamental filters
def apply_fundamental_filters(ticker_data):
    if None in ticker_data.values():
        return False
    return (
        10 <= ticker_data['PE_ratio'] <= 25 and
        ticker_data['PB_ratio'] < 3 and
        ticker_data['ROE'] > 10 and
        ticker_data['Current_Ratio'] > 1.5 and
        ticker_data['Debt_Equity'] < 0.5
    )

# Get NASDAQ assets
def get_nasdaq_assets():
    fundamental_tickers = []
    for ticker_symbol in tickers:
        retry_attempts = 3
        for attempt in range(retry_attempts):
            try:
                ticker = yf.Ticker(ticker_symbol)
                info = ticker.info
                ticker_data = {
                    'PE_ratio': info.get('trailingPE'),
                    'PB_ratio': info.get('priceToBook'),
                    'ROE': info.get('returnOnEquity', 0) * 100,
                    'Current_Ratio': info.get('currentRatio'),
                    'Debt_Equity': info.get('debtToEquity', 0) / 100
                }
                if apply_fundamental_filters(ticker_data):
                    fundamental_tickers.append(ticker_symbol)
                break
            except Exception as e:
                print(f"Error fetching data for {ticker_symbol}, attempt {attempt + 1}/{retry_attempts}: {e}")
                time.sleep(2)
    return fundamental_tickers

# Calculate technical indicators with TA-Lib
def calculate_indicators(df):
    close_values = df['Close'].values.flatten()
    df['RSI'] = talib.RSI(close_values, timeperiod=14)
    df['MACD'], df['MACD_signal'], _ = talib.MACD(close_values, fastperiod=12, slowperiod=26, signalperiod=9)
    df['SMA_50'] = talib.SMA(close_values, timeperiod=50)
    df['SMA_200'] = talib.SMA(close_values, timeperiod=200)
    df['ATR'] = talib.ATR(df['High'].values if 'High' in df.columns else np.array([df['Close'].iloc[-1]]), 
                          df['Low'].values if 'Low' in df.columns else np.array([df['Close'].iloc[-1]]),
                          df['Close'].values, timeperiod=14)
    return df

# Suggest entry and exit conditions
def suggest_entries_exits(df):
    buy_signals = (df['RSI'] < 25) & (df['MACD'] > df['MACD_signal'])
    sell_signals = (df['RSI'] > 75) & (df['MACD'] < df['MACD_signal'])
    
    buy_dates = df.index[buy_signals]
    sell_dates = df.index[sell_signals]
    buy_prices = df['Close'][buy_signals]
    sell_prices = df['Close'][sell_signals]
    
    suggestions = [('Buy', date, price) for date, price in zip(buy_dates, buy_prices)]
    suggestions.extend([('Sell', date, price) for date, price in zip(sell_dates, sell_prices)])
    suggestions.sort(key=lambda x: x[1])
    
    return suggestions

# Check real-time price
def check_real_time_price(ticker):
    ticker_data = yf.Ticker(ticker)
    try:
        latest_data = ticker_data.history(period="1d", interval="1m").tail(1)
        if latest_data.empty:
            print(f"No real-time data available for ticker {ticker}")
            return None
        return latest_data['Close'].iloc[0]
    except Exception as e:
        print(f"Error fetching real-time price for {ticker}: {e}")
        return None

# Generate price targets
def generate_price_targets(df):
    atr = talib.ATR(df['High'].values if 'High' in df.columns else np.array([df['Close'].iloc[-1]]), 
                    df['Low'].values if 'Low' in df.columns else np.array([df['Close'].iloc[-1]]),
                    df['Close'].values, timeperiod=14)
    current_price = df['Close'].iloc[-1]
    buy_target = current_price * 1.02  # Example: target price is 2% higher
    stop_loss = current_price - 1.5 * atr[-1]  # Example: stop-loss at 1.5x ATR
    return buy_target, stop_loss

# Identify bullish and bearish tickers
def identify_bullish_bearish(data):
    bullish_tickers = {}
    bearish_tickers = {}
    try:
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
                
                if rsi_value < 25 and macd_value > macd_signal_value:
                    bullish_tickers[ticker] = {
                        'RSI': rsi_value,
                        'MACD': macd_value,
                        'MACD Signal': macd_signal_value,
                        'High': ticker_high,
                        'Low': ticker_low,
                        'Close': close_prices_value
                    }
                elif rsi_value > 75 and macd_value < macd_signal_value:
                    bearish_tickers[ticker] = {
                        'RSI': rsi_value,
                        'MACD': macd_value,
                        'MACD Signal': macd_signal_value,
                        'High': ticker_high,
                        'Low': ticker_low,
                        'Close': close_prices_value
                    }
            except KeyError as e:
                pass  # Suppressed detailed error message for iterator details
    except Exception as e:
        print("Error identifying bullish and bearish tickers:", e)
    return bullish_tickers, bearish_tickers

# Output actionable summary
def output_summary(bullish_tickers, bearish_tickers):
    print("Processing summary of bullish and bearish tickers...")
    summary = []
    for ticker, data in bullish_tickers.items():
        price = check_real_time_price(ticker)
        if price is None:
            continue
        buy_target, stop_loss = generate_price_targets(pd.DataFrame([data]))
        summary.append({
            'Ticker': ticker,
            'Signal': 'Buy',
            'Current Price': price,
            'Target Price': buy_target,
            'Stop-Loss': stop_loss
        })
    for ticker, data in bearish_tickers.items():
        price = check_real_time_price(ticker)
        if price is None:
            continue
        summary.append({
            'Ticker': ticker,
            'Signal': 'Sell',
            'Current Price': price
        })
    summary_df = pd.DataFrame(summary)
    print(summary_df)
    log_summary(summary_df)

# Log trading summary
def log_summary(summary_df):
    print("Logging summary of trading actions...")
    for _, row in summary_df.iterrows():
        logging.info(f"{row['Ticker']}: {row['Signal']} at {row['Current Price']} with target {row.get('Target Price', 'N/A')} and stop-loss {row.get('Stop-Loss', 'N/A')}")

# Check if the market is open
def is_market_open():
    ny_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
    if ny_time.weekday() < 5 and ny_time.time() >= datetime.time(9, 30) and ny_time.time() <= datetime.time(16, 0):
        return True
    return False

# Run the system
def main():
    print("Starting trading analysis...")
    # Determine the appropriate data to download based on market status
    try:
        if is_market_open():
            print("Market is open. Fetching intraday data...")
            data = yf.download(tickers, period="1d", interval="5m", group_by='ticker', progress=False)
        else:
            print("Market is closed or pre-market. Fetching extended data...")
            # Use a longer timeframe with 15-minute data for pre-market or after-hours analysis
            data = yf.download(tickers, period="5d", interval="15m", group_by='ticker', progress=False)
        if data.empty:
            print("No data fetched. Please check data availability or try during trading hours.")
            return
    except Exception as e:
        print(f"Error downloading data: {e}")
        return
    
    print("Identifying bullish and bearish tickers...")
    bullish_tickers, bearish_tickers = identify_bullish_bearish(data)
    
    # Show bullish and bearish tickers
    print("Generating output summary...")
    output_summary(bullish_tickers, bearish_tickers)

if __name__ == "__main__":
    main()
