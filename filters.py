"""
This module contains functions for applying filters to stock data.
"""
import math
from config import CONFIG

def normalize_value(value):
    """
    Normalizes a value by replacing None and 'Infinify' with 0.

    Parameters:
        value (float): The value to normalize.

    Returns:
        float: The normalized value.
    """
    if isinstance(value, str):
        return 0 if value.lower() == 'infinity' else value
    else:
        return value if value is not None and not math.isnan(value) and not math.isinf(value) else 0

def filter_by_fundamentals(ticker_data):
    """
    Inclusively filters tickers based on fundamental data.

    Parameters:
        ticker_data (dict): Dictionary containing financial data for the ticker.

    Returns:
        bool: True if the ticker passes the filter, False otherwise.
    """
    trailing_eps = normalize_value(ticker_data['trailing_eps'])
    earnings_growth = normalize_value(ticker_data['earnings_growth'])
    revenue_growth = normalize_value(ticker_data['revenue_growth'])
    current_ratio = normalize_value(ticker_data['current_ratio'])
    short_ratio = normalize_value(ticker_data['short_ratio'])
    debt_equity = normalize_value(ticker_data['debt_equity'])
    peg_ratio = normalize_value(ticker_data['peg_ratio'])
    pb_ratio = normalize_value(ticker_data['pb_ratio'])
    pe_ratio = normalize_value(ticker_data['pe_ratio'])
    recommendation_mean = normalize_value(ticker_data['recommendation_mean'])
    return_on_equity = normalize_value(ticker_data['return_on_equity'])

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
