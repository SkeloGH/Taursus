"""Reporting module for the trading analysis script."""
import logging
import pandas as pd

from config import CONFIG, args

from indicators import generate_price_targets
from ticker_data import fetch_real_time_prices

def reset_decision_log():
    """
    Resets the decision log if the --reset-log argument is provided.
    """
    if args.reset_log:
        with open(file=CONFIG['LOG_FILE'], mode='w', encoding='utf-8') as f:
            f.write('')  # Reset the log file
        logging.info("The decision log has been reset.")
    else:
        logging.info("The decision log will continue to be appended.")

def log_summary(summary_df):
    """
    Logs the suggested trades and their details.

    Parameters:
        summary_df (DataFrame): DataFrame containing the summary of trades.
    """
    logging.info("Logging summary of trading actions...")
    for _, row in summary_df.iterrows():
       logging.info("%s: %s at %s with target %s and stop-loss %s",
             row['Ticker'], row['Signal'], row['Current Price'],
             row.get('Target Price', 'N/A'), row.get('Stop-Loss', 'N/A'))

def output_summary(bullish_tickers, bearish_tickers):
    """
    Generates and displays a summary of bullish and bearish tickers.

    Parameters:
        bullish_tickers (dict): Dictionary of bullish tickers.
        bearish_tickers (dict): Dictionary of bearish tickers.
    """
    logging.info("Generating summary of bullish and bearish tickers...")
    all_tickers = list(bullish_tickers.keys()) + list(bearish_tickers.keys())

    if not all_tickers:
        logging.info("No bullish or bearish tickers found.")
        return

    prices = fetch_real_time_prices(all_tickers)
    summary = []
    for ticker, data in bullish_tickers.items():
        price = prices.get(ticker)
        if price is None:
            continue
        df = pd.DataFrame([data])
        df['Close'] = price
        buy_target, stop_loss = generate_price_targets(df)
        summary.append({
            'Ticker': ticker,
            'Signal': 'Buy',
            'Current Price': price,
            'Target Price': buy_target,
            'Stop-Loss': stop_loss
        })
    for ticker, data in bearish_tickers.items():
        price = prices.get(ticker)
        if price is None:
            continue
        summary.append({
            'Ticker': ticker,
            'Signal': 'Sell',
            'Current Price': price
        })
    summary_df = pd.DataFrame(summary)
    logging.info("""Summary of trading actions: \n%s""", summary_df)
    log_summary(summary_df)
