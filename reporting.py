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

def ticker_meta(ticker):
    """
    Includes ticker metadata in the summary.

    Parameters:
        ticker (str): Ticker symbol.

    Returns:
        dict: Ticker metadata.
    """
    return {
        'ticker': ticker,
        'name': ticker.info['shortName'],
        'sector': ticker.info['sector'],
        'industry': ticker.info['industry'],
    }

def format_summary(buy_targets, sell_targets):
    """
    Formats the summary of trading actions as a string.

    Parameters:
        summary (list): List of trading actions.

    Returns:
        str: Formatted summary of trading actions.
    """
    # Sort by risk/reward ratio
    buy_targets.sort(key=lambda x: x['RRR'], reverse=True)
    sell_targets.sort(key=lambda x: x['RRR'], reverse=True)
    # Filter targets which are too risky
    buy_targets = [ticker_meta(target) for target in buy_targets if target['RRR'] > CONFIG['MAX_RRR']]
    sell_targets = [ticker_meta(target) for target in sell_targets if target['RRR'] > CONFIG['MAX_RRR']]
    combined_targets = buy_targets + sell_targets
    return combined_targets

def output_summary(summary):
    """
    Generates and displays a summary of the trading actions.

    Parameters:
        summary (list): List of trading actions.
    """
    logging.info("Generating summary...")
    summary_df = pd.DataFrame(summary)
    logging.info("""Summary of trading signals: \n%s""", summary_df)
