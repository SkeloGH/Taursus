"""Main script that executes the trading analysis."""
import logging

from reporting import reset_decision_log, output_summary
from tickers import get_tickers_list_by_index
from user_inputs import handle_keyboard_interrupt, prompt_ticker_selection, prompt_custom_ticker_list
from ticker_data import fetch_tickers, fetch_real_time_prices, get_tickers_fundamentals, is_market_open
from classify import identify_bullish_bearish
from indicators import generate_targets
from config import CONFIG

@handle_keyboard_interrupt
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
        logging.info("""%d tickers passed the fundamental filters:
                      %s""", len(filtered_tickers), ', '.join(filtered_tickers))

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
    combined_tickers = list(bullish_tickers.keys()) + list(bearish_tickers.keys())
    if not combined_tickers:
        logging.info("No bullish or bearish tickers found.")
        return
    prices = fetch_real_time_prices(combined_tickers)
    buy_targets, sell_targets = generate_targets(bullish_tickers, bearish_tickers, prices)
    # Sort by risk/reward ratio
    buy_targets.sort(key=lambda x: x['RRR'], reverse=True)
    sell_targets.sort(key=lambda x: x['RRR'], reverse=True)
    # Filter targets which are too risky
    buy_targets = [target for target in buy_targets if target['RRR'] > CONFIG['MAX_RRR']]
    sell_targets = [target for target in sell_targets if target['RRR'] > CONFIG['MAX_RRR']]
    combined_targets = buy_targets + sell_targets

    # Generate and display summary
    output_summary(combined_targets)

if __name__ == "__main__":
    main()
