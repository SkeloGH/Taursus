"""List of tickers from different sources."""
from config import CONFIG

def get_tickers_list_by_index(index: int):
    """Get tickers list based on the user's choice."""
    return CONFIG['TICKERS_LISTS'][index].get('tickers')

def prompt_ticker_selection():
    """Prompt the user to choose a list of tickers."""
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
    while True:
        custom_tickers = input("Enter a list of tickers separated by commas: ").strip().split(',')
        # Sanitize input
        custom_tickers = [ticker.strip() for ticker in custom_tickers if ticker.strip()]

        if not custom_tickers:
            print("Invalid input. Please try again.")
        else:
            break

    return custom_tickers
