"""Main script that executes the trading analysis."""
import logging

from config import CONFIG
import user_inputs
import tickers
import ticker_data
import classifier
import indicators
import reporting

@user_inputs.handle_keyboard_interrupt
def main():
    """
    Main function that executes the trading analysis.
    """
    choice = user_inputs.prompt_ticker_selection()
    # Get the tickers list based on the user's choice
    selected_tickers = tickers.get_tickers_list_by_index(int(choice)-1)
    list_name = CONFIG['TICKERS_LISTS'][int(choice) - 1].get('name')
    # If user chose a custom list, get the selected tickers
    if list_name == 'custom_tickers':
        selected_tickers = user_inputs.prompt_custom_ticker_list()

    logging.info("Starting trading analysis...")

    # Apply fundamental filters
    compliant_tickers_data = ticker_data.fetch_tickers_by_fundamentals(selected_tickers)
    compliant_ticker_names = [ticker.info['symbol'] for ticker in compliant_tickers_data]
    num_compliant_tickers = len(compliant_ticker_names)
    if not compliant_tickers_data:
        logging.info("No tickers passed the fundamental filters.")
        return
    else:
        logging.info("%d tickers passed the fundamental filters", num_compliant_tickers)

    # Identify the top movers
    bullish_tickers, bearish_tickers = classifier.filter_bullish_bearish(compliant_tickers_data)
    buy_targets, sell_targets = indicators.generate_targets(bullish_tickers, bearish_tickers)
    trading_signals = reporting.format_summary(compliant_tickers_data, buy_targets, sell_targets)

    # Print the summary
    reporting.print_trading_signals(trading_signals)

if __name__ == "__main__":
    main()
