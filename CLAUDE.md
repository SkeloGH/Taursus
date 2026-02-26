# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Taursus is a Python CLI tool that performs stock trading analysis. It fetches market data via yfinance, applies fundamental and technical filters, classifies tickers as bullish or bearish, and generates buy/sell price targets with risk/reward ratios.

## Running the Tool

```bash
# Activate the virtual environment first
source .venv/bin/activate

# Run the main script
python3 main.py

# With optional CLI arguments
python3 main.py --rsi-buy-threshold 30 --rsi-sell-threshold 70 --min-results 3 --reset-log
```

CLI arguments (all optional, defaults in `config.py`):
- `--rsi-buy-threshold` — RSI level to trigger buy signal (default: 35)
- `--rsi-sell-threshold` — RSI level to trigger sell signal (default: 65)
- `--min-results` — minimum bullish/bearish results required (default: 5)
- `--reset-log` — resets `trading_decision_log.txt` on each run (default: True)

## Setup

TA-Lib is a C library dependency that must be compiled before `pip install`. On Linux, `setup.sh` automates this. On macOS:

```bash
brew install ta-lib
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Troubleshooting TA-Lib on macOS:** If `pip install` fails with `ta-lib/ta_defs.h file not found`, the Homebrew headers aren't linked. Fix with:

```bash
brew link ta-lib
# or, if that doesn't work, point the compiler explicitly:
TA_INCLUDE_PATH=/usr/local/Cellar/ta-lib/0.4.0/include \
TA_LIBRARY_PATH=/usr/local/Cellar/ta-lib/0.4.0/lib \
pip install TA-Lib
```

Then re-run `pip install -r requirements.txt`.

## Claude Code + Virtual Environment

Claude Code's Bash tool spawns new subshells and won't inherit an activated venv unless `claude` itself was launched from the activated terminal. Always launch Claude Code after activating the venv:

```bash
source .venv/bin/activate
claude
```

Alternatively, prefix Python commands explicitly: `.venv/bin/python3 main.py`

## Architecture

The pipeline in `main.py` executes sequentially:

1. **User selects a ticker list** (`user_inputs.py`) — prompts for a predefined list or custom comma-separated tickers
2. **Fetch fundamentals** (`ticker_data.py`) — fetches each ticker via yfinance with retry logic and a `requests-cache` session
3. **Filter by fundamentals** (`filters.py`) — inclusive OR filter using thresholds from `config.py` (EPS, earnings growth, revenue growth, P/E, P/B, PEG, debt/equity, current ratio, short ratio, ROE, analyst recommendation)
4. **Classify bullish/bearish** (`classifier.py`) — downloads 1-month OHLCV history at 30m intervals, computes RSI and MACD via TA-Lib; a ticker is bullish if RSI ≤ buy threshold AND MACD ≥ signal, bearish if RSI ≥ sell threshold AND MACD ≤ signal
5. **Generate price targets** (`indicators.py`) — computes ATR-based stop-loss and 2% target price, calculates Risk/Reward Ratio (RRR)
6. **Report** (`reporting.py`) — filters out targets with RRR < `MAX_RRR` or missing sector/industry, prints a DataFrame to the log, and saves `trading_summary.csv`

### Key files

| File | Responsibility |
|---|---|
| `config.py` | Single source of truth: all thresholds, CLI arg parsing, logging setup, ticker list definitions |
| `ticker_data.py` | yfinance session, data fetching with retry, fundamental pre-filtering loop |
| `filters.py` | Fundamental filter logic (inclusive OR across metrics) |
| `indicators.py` | `get_ticker_fundamentals()` (extracts from yfinance `.info`), ATR/buy/sell target generation |
| `classifier.py` | RSI + MACD classification; adaptive retry loosening RSI thresholds if `MIN_RESULTS` not met |
| `reporting.py` | Post-filtering by RRR/sector/industry, CSV output, log reset |
| `tickers_lists/` | Static Python modules: `bmv_tickers`, `nasdaq_tickers`, `russell2k_tickers`, `other_tickers` |

### Output files (generated at runtime)

- `trading_decision_log.txt` — structured log of each run
- `trading_summary.csv` — final buy/sell signals with ticker metadata
- `yfinance.cache` — HTTP cache from requests-cache (speeds up repeat runs)

## Configuration

All thresholds live in the `CONFIG` dict in `config.py`. To change analysis behavior, modify values there rather than in the individual modules. The classifier has adaptive logic: if fewer than `MIN_RESULTS` bullish/bearish tickers are found, it relaxes RSI thresholds by ±5 and retries with different time periods.

## Linting

Pylint is available in the dev dependencies:
```bash
pylint *.py
```
