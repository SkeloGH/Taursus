"""Configuration file for the trading analysis script."""
import sys
import argparse
import logging

from tickers_lists import (
    bmv_tickers,
    nasdaq_tickers,
    russell2k_tickers,
    other_tickers
)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Trading Analysis Script')
parser.add_argument('--reset-log', action='store_false', help='Reset the decision log')
parser.add_argument('--rsi-buy-threshold', type=int, help='Custom RSI threshold for buy signals')
parser.add_argument('--rsi-sell-threshold', type=int, help='Custom RSI threshold for sell signals')
parser.add_argument('--min-results', type=int, help='Custom minimum number of required results')
parser.add_argument('--ticker-list', type=str, help='Ticker list name to use (e.g. nasdaq_tickers)')
parser.add_argument('--custom-tickers', type=str, help='Comma-separated list of custom tickers')
# handle empty strings, missing or unspecified arguments
parser.set_defaults(reset_log=True,
                    rsi_buy_threshold=None, rsi_sell_threshold=None, min_results=None,
                    ticker_list=None, custom_tickers=None)
args = parser.parse_known_args()[0]

CONFIG = {
    # Fundamental analysis thresholds
    'TRAILING_EPS_MIN': 2, # EPS over prior fiscal year
    'EARNINGS_GROWTH_MIN': 0.20,
    'REVENUE_GROWTH_MIN': 0.20,
    'CURRENT_RATIO_MIN': 1.5, # Ability to reduce risk by not paying debt (assets/liabilities)
    'SHORT_RATIO_MAX': 1, # How long it takes short sellers to repurchase (shares sold / Average daily volume)
    'DEBT_EQUITY_MAX': 2, #  How much debt is using to finance assets relative to equity
    'PE_RATIO_MIN': 20,
    'PE_RATIO_MAX': 60,
    'PB_RATIO_MIN': 10,
    'PB_RATIO_MAX': 40,
    'PEG_RATIO_MIN': 0.5,
    'PEG_RATIO_MAX': 1.5,
    'RECOMMENDATION_MEAN_MIN': 1,
    'RECOMMENDATION_MEAN_MAX': 2,
    'ROE_RATIO_MIN': 10,
    # Classification thresholds
    'MACD_FAST_PERIOD': 6,
    'MACD_SLOW_PERIOD': 13,
    'MACD_SIGNAL_PERIOD': 5,
    'RSI_PERIOD': 14,
    'RSI_THRESHOLD_BUY': args.rsi_buy_threshold if args.rsi_buy_threshold else 35,
    'RSI_THRESHOLD_SELL': args.rsi_sell_threshold if args.rsi_sell_threshold else 65,
    # Risk management
    'MAX_RRR': 0.8, # Ideal ratio is 1 and higher
    # Fetching parameters
    'MIN_RESULTS': args.min_results if args.min_results else 5,
    'RETRY_ATTEMPTS': 5,
    'MAX_WORKERS': 5,
    'CONNECTION_POOL_SIZE': False,
    'TICKER_FETCHING_PERIODS': ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
    'TICKER_FETCHING_INTERVALS': ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"],
    # Logging
    'LOG_FILE': 'trading_decision_log.txt',
    'SUMMARY_FILE': 'trading_summary.csv',
    # Tickers sources
    'TICKERS_LISTS': [
        {'name': 'bmv_nasdaq_tickers', 'tickers': bmv_tickers.tickers + nasdaq_tickers.tickers,
         'description': 'BMV and NASDAQ'},
        {'name': 'bmv_tickers', 'tickers': bmv_tickers.tickers, 'description': 'BMV'},
        {'name': 'nasdaq_tickers', 'tickers': nasdaq_tickers.tickers, 'description': 'NASDAQ'},
        {'name': 'russell2k_tickers', 'tickers': russell2k_tickers.tickers, 'description': 'Russell 2000'},
        {'name': 'other_tickers', 'tickers': other_tickers.tickers, 'description': 'Other'},
        {'name': 'all_tickers',
         'tickers': bmv_tickers.tickers + nasdaq_tickers.tickers + russell2k_tickers.tickers + other_tickers.tickers,
         'description': 'All'},
        {'name': 'custom_tickers', 'tickers': [], 'description': 'Custom'},
    ],
}

# Configure logging with timestamps
handlers = [
    logging.StreamHandler(sys.stdout),
    logging.FileHandler(CONFIG['LOG_FILE'])
]

logging.basicConfig(handlers=handlers, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
