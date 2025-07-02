# pine_scripts
# TradingView Pine Script & Strategy Collection

This repository contains a collection of TradingView Pine Scripts and related strategy files, including technical indicators and strategies based on EMA, RSI, MACD, Supertend, and options analysis. It also includes one Python file for external integration and automation.

---

## 📁 Files Overview

### 📌 Pine Scripts

#### 1. `2bulls_rsi.pine`
A custom RSI-based indicator possibly developed by "2bulls." Likely includes modifications to the traditional RSI logic for better signal generation.

#### 2. `5_20ema-strategy.pine`
A crossover strategy based on the 5 EMA and 20 EMA. This script is used to generate buy/sell signals when the short-term EMA crosses above or below the long-term EMA.

#### 3. `ema_gap.pine.txt`
This script likely identifies the price gap between two EMAs and may be used to detect overbought/oversold conditions or trend strength.

#### 4. `options.pine.txt`
A TradingView script designed for options trading. It may visualize options levels such as support/resistance based on OI, volume, or max pain theory.

#### 5. `trendline.pine`
An automated trendline detection tool. This script draws dynamic support/resistance or trendlines based on price action and pivot points.

#### 6. `HTF MACD RSI & SUPERTREND.txt`
A multi-indicator script combining:
- Higher Time Frame (HTF) MACD
- HTF RSI
- Supertend Indicator  
Likely used for confirmation-based entries across multiple timeframes.

#### 7. `mutliple time frame macd and rsi.txt`
Similar to above but might be a simplified or alternate version that plots MACD and RSI from higher timeframes on the current chart.

---

### 🐍 Python Script

#### 8. `emacrossover.py`
A Python script for analyzing EMA crossovers using external market data (e.g., via APIs like Upstox, Zerodha Kite, or Yahoo Finance). Useful for automated strategy testing or signal generation outside TradingView.

---

### 🧾 Other

#### 9. `README.md`
This file — provides an overview of the repository, file structure, and usage instructions.

---

## 🛠️ How to Use

1. Open [TradingView](https://www.tradingview.com/)
2. Go to **Pine Editor** at the bottom of your chart.
3. Paste the contents of any `.pine` or `.txt` file.
4. Click **Save** and **Add to Chart**.
5. Adjust parameters as needed from the indicator settings.

---

## 📌 Notes

- `.txt` files may need to be renamed to `.pine` or pasted directly into TradingView.
- `emacrossover.py` should be run in a Python environment. Ensure required libraries are installed.

---

## 📧 Contact

For questions or enhancements, feel free to open an issue or contact the repo maintainer.

