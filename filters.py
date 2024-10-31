"""
This module contains functions for applying filters to stock data.
"""

from config import CONFIG

def fundamentals(ticker_data,
                 pe_min=CONFIG['PE_RATIO_MIN'],
                 pe_max=CONFIG['PE_RATIO_MAX'],
                 pb_max=CONFIG['PB_RATIO_MAX'],
                 roe_max=CONFIG['ROE_RATIO_MAX'],
                 current_ratio_max=CONFIG['CURRENT_RATIO_MAX'],
                 debt_equity_max=CONFIG['DEBT_EQUITY_MAX']):
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
        pe_min <= ticker_data['PE_ratio'] <= pe_max or
        ticker_data['PB_ratio'] < pb_max or
        ticker_data['ROE'] > roe_max or
        ticker_data['Current_Ratio'] > current_ratio_max or
        ticker_data['Debt_Equity'] < debt_equity_max
    )
