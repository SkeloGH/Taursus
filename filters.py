"""
This module contains functions for applying filters to stock data.
"""

from config import CONFIG

def filter_by_fundamentals(ticker_data):
    """
    Inclusively filters tickers based on fundamental data.

    Parameters:
        ticker_data (dict): Dictionary containing financial data for the ticker.

    Returns:
        bool: True if the ticker passes the filters, False otherwise.
    """
    if None in ticker_data.values():
        return False

    return (
        ticker_data['trailing_eps'] >= CONFIG['TRAILING_EPS_MIN'] or
        ticker_data['earnings_growth'] >= CONFIG['EARNINGS_GROWTH_MIN'] or
        ticker_data['revenue_growth'] >= CONFIG['REVENUE_GROWTH_MIN'] or
        ticker_data['current_ratio'] >= CONFIG['CURRENT_RATIO_MIN'] or
        ticker_data['short_ratio'] <= CONFIG['SHORT_RATIO_MAX'] or
        ticker_data['debt_equity'] <= CONFIG['DEBT_EQUITY_MAX'] or
        (ticker_data['peg_ratio'] >= CONFIG['PEG_RATIO_MIN'] and
        ticker_data['peg_ratio'] <= CONFIG['PEG_RATIO_MAX']) or
        (ticker_data['pb_ratio'] >= CONFIG['PB_RATIO_MIN'] and
        ticker_data['pb_ratio'] <= CONFIG['PB_RATIO_MAX']) or
        (ticker_data['pe_ratio'] >= CONFIG['PE_RATIO_MIN'] and
        ticker_data['pe_ratio'] <= CONFIG['PE_RATIO_MAX']) or
        (ticker_data['recommendation_mean'] >= CONFIG['RECOMMENDATION_MEAN_MIN'] and
        ticker_data['recommendation_mean'] <= CONFIG['RECOMMENDATION_MEAN_MAX']) or
        (ticker_data['return_on_equity'] >= CONFIG['ROE_RATIO_MIN'] and
        ticker_data['return_on_equity'] <= CONFIG['ROE_RATIO_MAX'])
    )
