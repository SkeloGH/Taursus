"""
This module contains functions for applying filters to stock data.
"""

def fundamentals(ticker_data):
    """
    Applies fundamental filters to a stock's data.

    Parameters:
        ticker_data (dict): Dictionary containing financial data for the ticker.

    Returns:
        bool: True if the ticker passes the filters, False otherwise.
    """
    if None in ticker_data.values():
        return False
    return (
        10 <= ticker_data['PE_ratio'] <= 25 and
        ticker_data['PB_ratio'] < 3 and
        ticker_data['ROE'] > 10 and
        ticker_data['Current_Ratio'] > 1.5 and
        ticker_data['Debt_Equity'] < 0.5
    )
