# SectorPulse

## What It Does
This project is a small demo website that tries to **predict short-term stock/ETF movement** and visualize the results.

You type a ticker (for example **SPY** or **XLK**) and choose a horizon (**next day** or **next week**).  
The backend downloads recent price data, builds a set of simple technical indicators, trains a baseline ML model, and returns:
- a short-horizon **predicted price**
- a quick explanation of **which features mattered most** (feature importance)
- a simple **performance comparison** against a market benchmark

## How We built it
- **Frontend:** HTML/CSS + JavaScript. Charts are made with **ECharts**.
- **Backend:** **FastAPI** with a `/predict` endpoint.
- **Data:** downloaded from Yahoo Finance using `yfinance`.
- **Features:** moving averages, RSI, MACD, Bollinger Bands, returns/volatility, and volume-related features.
- **Model:** a basic tree-based model (random forest / gradient boosting depending on the version we run).
- **Evaluation:** we split by time (train on earlier data, test on later data), and report common error metrics plus a simple “up/down direction” accuracy.

## Challenges we ran into

## Accomplishments that we're proud of

## What we learned
We learned knowledges about stocks and trading, practice machine learning and coding, and work together as a group

## What's next 
