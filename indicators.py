"""Calculates technical indicators and generates price targets."""
import talib
import numpy as np

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
    Generates buy target price and stop-loss level using ATR.

    Parameters:
        df (DataFrame): DataFrame with price data and indicators.

    Returns:
        tuple: Buy target price and stop-loss level.
    """
    atr = talib.ATR(
        df['High'].values if 'High' in df.columns else np.array([df['Close'].iloc[-1]]),
        df['Low'].values if 'Low' in df.columns else np.array([df['Close'].iloc[-1]]),
        df['Close'].values, timeperiod=14)
    current_price = df['Close'].iloc[-1]
    buy_target = current_price * 1.02  # Target price 2% higher
    stop_loss = current_price - 1.5 * atr[-1]  # Stop-loss at 1.5x ATR
    return buy_target, stop_loss
