"""
This module contains functions for applying filters to stock data.
"""

def fundamentals(ticker_data):
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
        10 <= ticker_data['PE_ratio'] <= 25 or
        ticker_data['PB_ratio'] < 3 or
        ticker_data['ROE'] > 10 or
        ticker_data['Current_Ratio'] > 1.5 or
        ticker_data['Debt_Equity'] < 0.5
    )
