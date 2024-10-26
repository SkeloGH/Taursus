import pdb
import yfinance as yf
import logging

from reporting import reset_decision_log, output_summary
from ticker_data import fetch_tickers, get_nasdaq_assets, is_market_open
from classify import identify_bullish_bearish

def main():
    """
    Main function that executes the trading analysis.
    """
    logging.info("Starting trading analysis...")

    # Reset the decision log if the --reset-log argument is provided
    reset_decision_log()

    # Apply fundamental filters
    logging.info("Applying fundamental filters...")
    fundamental_tickers = get_nasdaq_assets()
    if not fundamental_tickers:
        logging.info("No tickers passed the fundamental filters.")
        return
    else:
        logging.info(f"{len(fundamental_tickers)} tickers passed the fundamental filters: {', '.join(fundamental_tickers)}")

    # Determine appropriate data to download based on market status
    try:
        if is_market_open():
            logging.info("Market is open. Fetching intraday data...")
            data = fetch_tickers(fundamental_tickers, period="1d", interval="5m", group_by='ticker')
        else:
            logging.info("Market is closed or pre-market. Fetching extended data...")
            # Use a longer timeframe with 15-minute data for pre-market or after-hours analysis
            data = fetch_tickers(fundamental_tickers, period="5d", interval="15m", group_by='ticker')
        if data.empty:
            logging.info("No data fetched. Please check data availability or try during trading hours.")
            return
    except Exception as e:
        logging.error(f"Error downloading data: {e}")
        return

    # Identify bullish and bearish tickers
    logging.info("Identifying bullish and bearish tickers...")
    bullish_tickers, bearish_tickers = identify_bullish_bearish(data, fundamental_tickers)

    # Generate and display summary
    logging.info("Generating output summary...")
    output_summary(bullish_tickers, bearish_tickers)

if __name__ == "__main__":
    main()
