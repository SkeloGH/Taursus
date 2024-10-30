"""Reporting module for the trading analysis script."""
import logging
import pandas as pd
import numpy as np

from config import CONFIG, args

def reset_decision_log():
    """
    Resets the decision log if the --reset-log argument is provided.
    """
    if args.reset_log:
        with open(file=CONFIG['LOG_FILE'], mode='w', encoding='utf-8') as f:
            f.write('')  # Reset the log file
        logging.info("The decision log has been reset.")
    else:
        logging.info("The decision log will continue to be appended.")

def output_summary(summary):
    """
    Generates and displays a summary of the trading actions.

    Parameters:
        summary (list): List of trading actions.
    """
    logging.info("Generating summary...")    
    summary_df = pd.DataFrame(summary)
    logging.info("""Summary of trading actions: \n%s""", summary_df)
