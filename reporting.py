"""Reporting module for the trading analysis script."""
import logging
import pandas as pd

from config import CONFIG, args

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

def ticker_meta(ticker_prices, tickers_objects):
    """
    Includes ticker metadata in the summary.

    Parameters:
        ticker_prices (dict): Ticker price data.
        tickers_objects (list): Ticker objects with metadata.

    Returns:
        dict: Ticker metadata.
    """
    tickers_collection = []
    for ticker in tickers_objects:
        symbol = ticker.info['symbol']
        if symbol not in ticker_prices:
            continue
        ticker_price_targets = ticker_prices[symbol]
        tickers_collection.append({
            'Ticker': symbol,
            'Signal': ticker_price_targets['Signal'],
            'Current Price': ticker_price_targets['Current Price'],
            'Target Price': ticker_price_targets['Target Price'],
            'Stop-Loss': ticker_price_targets['Stop-Loss'],
            'RRR': ticker_price_targets['RRR'],
            'Name': ticker.info.get('shortName'),
            'Sector': ticker.info.get('sector'),
            'Industry': ticker.info.get('industry'),
        })
    return tickers_collection

def format_summary(tickers_objects, buy_targets, sell_targets):
    """
    Formats the summary of trading actions as a string.

    Parameters:
        tickers_objects (list): Ticker objects with metadata.
        buy_targets (dict): Dictionary of buy targets.
        sell_targets (dict): Dictionary of sell targets.

    Returns:
        str: Formatted summary of trading actions.
    """
    bullish = ticker_meta(buy_targets, tickers_objects)
    bearish = ticker_meta(sell_targets, tickers_objects)
    # Sort by risk/reward ratio
    sorted_bullish = sorted(bullish, key=lambda x: x['RRR'], reverse=True)
    sorted_bearish = sorted(bearish, key=lambda x: x['RRR'], reverse=True)
    # Filter targets which are too risky
    buy_targets = [target for target in sorted_bullish if target['RRR'] > CONFIG['MAX_RRR']]
    sell_targets = [target for target in sorted_bearish if target['RRR'] > CONFIG['MAX_RRR']]
    trading_signals = buy_targets + sell_targets
    return trading_signals

def output_summary(summary):
    """
    Generates and displays a summary of the trading actions.

    Parameters:
        summary (list): List of trading actions.
    """
    logging.info("Generating summary...")
    summary_df = pd.DataFrame(summary)
    logging.info("""Summary of trading signals: \n%s""", summary_df)
    # Concatenated list of tickers
    logging.info("Tickers in the summary: %s", ', '.join(summary_df['Ticker'].tolist()))
