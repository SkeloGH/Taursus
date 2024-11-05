"""Main script that executes the trading analysis."""
import logging

from config import CONFIG
from user_inputs import handle_keyboard_interrupt, prompt_ticker_selection, prompt_custom_ticker_list
from tickers import get_tickers_list_by_index
from ticker_data import fetch_tickers_by_fundamentals, get_tickers_historical_data, fetch_tickers, fetch_tickers_prices, is_market_open
from classify import classify_tickers
from indicators import generate_targets
from reporting import reset_decision_log, output_summary, format_summary

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
    compliant_tickers_data = fetch_tickers_by_fundamentals(selected_tickers)
    compliant_ticker_names = [ticker.info['symbol'] for ticker in compliant_tickers_data]
    if not compliant_tickers_data:
        logging.info("No tickers passed the fundamental filters.")
        return
    else:
        logging.info("""%d tickers passed the fundamental filters:
                      %s""", len(compliant_ticker_names), ', '.join(compliant_ticker_names))

    # Identify the top movers
    bullish_tickers, bearish_tickers = classify_tickers(compliant_tickers_data)
    # Fetch prices
    # prices = fetch_tickers_prices(compliant_ticker_names)
    # Generate buy and sell targets
    buy_targets, sell_targets = generate_targets(bullish_tickers, bearish_tickers)
    formatted_summary = format_summary(compliant_tickers_data, buy_targets, sell_targets)

    # Generate and display summary
    output_summary(formatted_summary)

if __name__ == "__main__":
    main()
