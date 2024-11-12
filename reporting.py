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
    # Clears entries that don't meet the presentation criteria
    buy_targets, sell_targets = filter_targets(sorted_bullish, sorted_bearish)
    trading_signals = buy_targets + sell_targets
    return trading_signals

def filter_targets(sorted_bullish, sorted_bearish):
    """
    Filters the targets that are too risky, or without relevant information.

    Parameters:
        sorted_bullish (list): Sorted list of buy targets.
        sorted_bearish (list): Sorted list of sell targets.

    Returns:
        tuple: Filtered buy and sell targets.
    """
    buy_targets = []
    sell_targets = []
    for target in sorted_bullish + sorted_bearish:
        is_finite_rrr = target['RRR'] != float('inf')
        is_within_max_rrr = target['RRR'] >= CONFIG['MAX_RRR']
        has_sector = target['Sector'] is not None
        has_industry = target['Industry'] is not None
        is_bullish = target['Signal'] == 'Buy'
        meets_criteria = is_finite_rrr and is_within_max_rrr and has_sector and has_industry

        if is_bullish and meets_criteria:
            buy_targets.append(target)
        elif not is_bullish and meets_criteria:
            sell_targets.append(target)

    return buy_targets, sell_targets

def print_trading_signals(summary):
    """
    Generates and displays a summary of the trading actions.

    Parameters:
        summary (list): List of trading actions.
    """
    # Resets the decision log when using --reset-log
    reset_decision_log()
    logging.info("Generating summary...")
    summary_df = pd.DataFrame(summary)
    logging.info("""Summary of trading signals: \n%s""", summary_df)
    # Save summary as a CSV file
    logging.info("""Saving summary as a CSV file: %s""", CONFIG['SUMMARY_FILE'])
    summary_df.to_csv(CONFIG['SUMMARY_FILE'], index=False)
    # Concatenated list of tickers
    if summary_df.empty:
        logging.info("No tickers in the summary.")
        return
    logging.info("Tickers in the summary: %s", ', '.join(summary_df['Ticker'].tolist()))
