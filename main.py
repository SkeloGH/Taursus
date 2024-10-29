"""Main script that executes the trading analysis."""
import logging

from reporting import reset_decision_log, output_summary
from tickers import get_tickers_list_by_index
from user_prompts import prompt_ticker_selection, prompt_custom_ticker_list
from ticker_data import fetch_tickers, get_tickers_fundamentals, is_market_open
from classify import identify_bullish_bearish
from config import CONFIG

def main():
    """
    Main function that executes the trading analysis.
    """
    choice = prompt_ticker_selection()
    # Get the tickers list based on the user's choice
    selected_tickers = get_tickers_list_by_index(int(choice)-1)
    list_name = CONFIG['TICKERS_LISTS'][int(choice) - 1].get('name')
    # If user chose a custom list, get the selected tickers
    if list_name == 'custom_tickers':
        selected_tickers = prompt_custom_ticker_list()

    logging.info("Starting trading analysis...")

    # Reset the decision log if the --reset-log argument is provided
    reset_decision_log()

    # Apply fundamental filters
    logging.info("Collecting tickers data...")
    filtered_tickers = get_tickers_fundamentals(selected_tickers)
    if not filtered_tickers:
        logging.info("No tickers passed the fundamental filters.")
        return
    else:
        logging.info("%d tickers passed the fundamental filters: %s", len(filtered_tickers), ', '.join(filtered_tickers))

    # Determine appropriate data to download based on market status
    try:
        if is_market_open():
            logging.info("Market is open. Fetching intraday data...")
            data = fetch_tickers(filtered_tickers, period="1d", interval="5m", group_by='ticker', progress=True)
        else:
            logging.info("Market is closed or pre-market. Fetching extended data...")
            # Use a longer timeframe with 15-minute data for pre-market or after-hours analysis
            data = fetch_tickers(filtered_tickers, period="5d", interval="15m", group_by='ticker', progress=True)
        if data.empty:
            logging.info("No data fetched. Please check data availability or try during trading hours.")
            return
    except Exception as e:
        logging.error(f"Error downloading data: {e}")
        return

    # Identify bullish and bearish tickers
    bullish_tickers, bearish_tickers = identify_bullish_bearish(data, filtered_tickers)

    # Generate and display summary
    output_summary(bullish_tickers, bearish_tickers)

if __name__ == "__main__":
    main()
