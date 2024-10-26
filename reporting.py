import logging
import pandas as pd

from config import CONFIG, args

from indicators import generate_price_targets
from ticker_data import get_real_time_prices

def reset_decision_log():
    """
    Resets the decision log if the --reset-log argument is provided.
    """
    if args.reset_log:
        with open(CONFIG['LOG_FILE'], 'w') as f:
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
        logging.info(f"{row['Ticker']}: {row['Signal']} at {row['Current Price']} with target {row.get('Target Price', 'N/A')} and stop-loss {row.get('Stop-Loss', 'N/A')}")

def output_summary(bullish_tickers, bearish_tickers):
    """
    Generates and displays a summary of bullish and bearish tickers.

    Parameters:
        bullish_tickers (dict): Dictionary of bullish tickers.
        bearish_tickers (dict): Dictionary of bearish tickers.
    """
    logging.info("Processing summary of bullish and bearish tickers...")
    all_tickers = list(bullish_tickers.keys()) + list(bearish_tickers.keys())

    if not all_tickers:
        logging.info("No tickers passed the fundamental filters.")
        return

    prices = get_real_time_prices(all_tickers)
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
    logging.info(summary_df)
    log_summary(summary_df)
