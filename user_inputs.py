"""Prompts for user input."""
import sys
from config import CONFIG, args

def handle_keyboard_interrupt(func):
    """Decorator to handle KeyboardInterrupt."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit()
    return wrapper

def prompt_ticker_selection():
    """Prompt the user to choose a list of tickers."""
    if args.ticker_list:
        names = [t['name'] for t in CONFIG['TICKERS_LISTS']]
        if args.ticker_list in names:
            return str(names.index(args.ticker_list) + 1)
        print(f"Unknown --ticker-list '{args.ticker_list}'. Valid options: {', '.join(names)}")
        sys.exit(1)

    if args.custom_tickers:
        names = [t['name'] for t in CONFIG['TICKERS_LISTS']]
        return str(names.index('custom_tickers') + 1)

    while True:
        print("Choose a list of tickers:")

        for i, ticker_list in enumerate(CONFIG['TICKERS_LISTS']):
            print(f"{i+1}. {ticker_list['name']} ({ticker_list['description']})")

        choice = input("Enter your choice: ")

        if choice.isdigit() and 1 <= int(choice) <= len(CONFIG['TICKERS_LISTS']):
            break
        else:
            print("Invalid choice. Please try again.")

    return choice

def prompt_custom_ticker_list():
    """Prompt the user to enter a list of tickers."""
    if args.custom_tickers:
        tickers = [t.strip() for t in args.custom_tickers.split(',') if t.strip()]
        if tickers:
            return tickers
        print("--custom-tickers was empty.")
        sys.exit(1)

    while True:
        custom_tickers = input("Enter a list of tickers separated by commas: ").strip().split(',')
        # Sanitize input
        custom_tickers = [ticker.strip() for ticker in custom_tickers if ticker.strip()]

        if not custom_tickers:
            print("Invalid input. Please try again.")
        else:
            break

    return custom_tickers
