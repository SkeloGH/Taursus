import logging
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Trading Analysis Script')
parser.add_argument('--reset-log', action='store_false', help='Reset the decision log')
parser.add_argument('--rsi-buy-threshold', type=int, help='Custom RSI threshold for buy signals')
parser.add_argument('--rsi-sell-threshold', type=int, help='Custom RSI threshold for sell signals')
parser.add_argument('--min-results', type=int, help='Custom minimum number of required results')
# handle empty strings, missing or unspecified arguments
parser.set_defaults(reset_log=True, rsi_buy_threshold=None, rsi_sell_threshold=None, min_results=None)
args = parser.parse_known_args()[0]

CONFIG = {
    'RSI_THRESHOLD_BUY': args.rsi_buy_threshold if args.rsi_buy_threshold else 25,
    'RSI_THRESHOLD_SELL': args.rsi_sell_threshold if args.rsi_sell_threshold else 75,
    'MIN_RESULTS': args.min_results if args.min_results else 5,
    'RETRY_ATTEMPTS': 5,
    'LOG_FILE': 'trading_decision_log.txt',
    'LOG_LEVEL': logging.INFO,
    'MAX_WORKERS': 5
}

# Configure logging with timestamps
handlers = [
    logging.StreamHandler(),
    logging.FileHandler(CONFIG['LOG_FILE'])
]

logging.basicConfig(handlers=handlers,
                    level=CONFIG['LOG_LEVEL'],
                    format='%(asctime)s - %(levelname)s - %(message)s')
