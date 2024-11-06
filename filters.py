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
        bool: True if the ticker passes the filter, False otherwise.
    """
    trailing_eps = ticker_data['trailing_eps'] or 0
    earnings_growth = ticker_data['earnings_growth'] or 0
    revenue_growth = ticker_data['revenue_growth'] or 0
    current_ratio = ticker_data['current_ratio'] or 0
    short_ratio = ticker_data['short_ratio'] or 0
    debt_equity = ticker_data['debt_equity'] or 0
    peg_ratio = ticker_data['peg_ratio'] or 0
    pb_ratio = ticker_data['pb_ratio'] or 0
    pe_ratio = ticker_data['pe_ratio'] or 0
    recommendation_mean = ticker_data['recommendation_mean'] or 0
    return_on_equity = ticker_data['return_on_equity'] or 0

    return (
        trailing_eps >= CONFIG['TRAILING_EPS_MIN'] or
        earnings_growth >= CONFIG['EARNINGS_GROWTH_MIN'] or
        revenue_growth >= CONFIG['REVENUE_GROWTH_MIN'] or
        current_ratio >= CONFIG['CURRENT_RATIO_MIN'] or
        short_ratio <= CONFIG['SHORT_RATIO_MAX'] or
        debt_equity <= CONFIG['DEBT_EQUITY_MAX'] or
        (peg_ratio >= CONFIG['PEG_RATIO_MIN'] and
        peg_ratio <= CONFIG['PEG_RATIO_MAX']) or
        (pb_ratio >= CONFIG['PB_RATIO_MIN'] and
        pb_ratio <= CONFIG['PB_RATIO_MAX']) or
        (pe_ratio >= CONFIG['PE_RATIO_MIN'] and
        pe_ratio <= CONFIG['PE_RATIO_MAX']) or
        (recommendation_mean >= CONFIG['RECOMMENDATION_MEAN_MIN'] and
        recommendation_mean <= CONFIG['RECOMMENDATION_MEAN_MAX']) or
        (return_on_equity >= CONFIG['ROE_RATIO_MIN'] and
        return_on_equity <= CONFIG['ROE_RATIO_MAX'])
    )
