"""List of tickers from different sources."""
from tickers_lists import (
    bmv_tickers,
    nasdaq_tickers,
    other_tickers
)

# List of unique tickers between BMV and NASDAQ
bmv_nasdaq_tickers = list(set(bmv_tickers.tickers + nasdaq_tickers.tickers))

# List of all unique tickers
all_tickers = list(set(bmv_nasdaq_tickers + other_tickers.tickers))

# Initialize list of tickers
selected_tickers = []

# Prompt the user to choose the list or lists of tickers
while True:
    print("Choose a list of tickers:")
    print("1. BMV tickers")
    print("2. NASDAQ tickers")
    print("3. Other tickers")
    print("4. BMV and NASDAQ tickers")
    print("5. All tickers")
    print("6. Specify tickers manually")

    choice = input("Enter 1, 2, 3, 4, 5, or 6: ")
    if choice == "1":
        selected_tickers = bmv_tickers.tickers
        break
    elif choice == "2":
        selected_tickers = nasdaq_tickers.tickers
        break
    elif choice == "3":
        selected_tickers = other_tickers.tickers
        break
    elif choice == "4":
        selected_tickers = bmv_nasdaq_tickers
        break
    elif choice == "5":
        selected_tickers = all_tickers
        break
    elif choice == "6":
        selected_tickers = input("Enter the tickers separated by commas: ").split(",")
        selected_tickers = [ticker.strip() for ticker in selected_tickers]
        break
    else:
        print("Invalid choice. Please try again.")
