"""List of tickers from different sources."""
from config import CONFIG

def get_tickers_list_by_index(index: int):
    """Get tickers list based on the user's choice."""
    return CONFIG['TICKERS_LISTS'][index].get('tickers')
