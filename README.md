# SectorPulse

## Inspiration
When we look at a stock chart every day, we are usually making a short horizon judgment without realizing it. Are we in a strong trend, a choppy regime, or a high volatility period where signals are unreliable.

This project is our attempt to turn that vague intuition into a repeatable pipeline. Given a ticker and a horizon, we want the system to pull fresh data, compute a small set of technical signals, run a baseline model, and show results in a way that is easy to explain and critique. 

## What It Does
SectorPulse is a small web demo that tries to **predict short-term stock/ETF movement** and visualize the results.

You type a ticker (for example **SPY** or **XLK**) and choose a horizon (**next day** or **next week**).  
The backend downloads recent price data, builds a set of simple technical indicators, trains a baseline ML model, and returns:
- a short-horizon **predicted price**
- a quick explanation of **which features mattered most** (feature importance)
- a simple **performance comparison** against a market benchmark

## How We built it
### Data
We use Yahoo Finance data through yfinance, extracted daily prices and volume.

### Features
We build a compact feature set that captures three things
- Trend: moving averages and their relative positioning
- Momentum and mean reversion: short and medium horizon returns
- Risk and activity: volatility measures and volume based signals

In the backend implementation, these include common indicators such as MA, RSI, MACD, Bollinger Bands, returns, volatility, and volume ratios.

### Model
We use Random Forest and Gradient Boosting variants because they are fast to train and handle non linear interactions reasonably well.

The prediction target is short horizon, either
- next day close, or
- next week close, typically five trading days ahead

### Validation logic
Time series validation is not the same as standard machine learning.
We split chronologically, training on earlier data and evaluating on later data.
We also avoid look ahead in backtest style calculations by shifting signals so that decisions use information available at the time.

### Frontend
The frontend is a lightweight dashboard using HTML, CSS, JavaScript, and ECharts.
It visualizes prediction output, feature importance, and a simple benchmark comparison.


### Backend
The backend is built with **FastAPI** and exposes a `/predict` endpoint that returns prediction results and model summaries in JSON format.

## Challenges we ran into
- **Data reliability:** `yfinance` sometimes returns empty data due to network or upstream availability. We added basic checks and retries.
- **Missing values:** rolling indicators (like moving averages and volatility) naturally create NaNs at the beginning, which can break model training if not handled consistently.
- **Time-series pitfalls:** random train/test splits can introduce look-ahead bias. We had to keep the split chronological and double-check label alignment.
- **Frontend/backend integration:** getting the API response format to match what the charts need took a few iterations.


## Accomplishments that we're proud of
- Built an end-to-end workflow: ticker input → data download → feature engineering → model training → prediction → visualization.
- Added interpretability through feature importance so the output is easier to explain.
- Included a benchmark comparison so results have context (instead of showing a prediction alone).

## What we learned
- **Financial prediction is noisy:** even reasonable models can be uncertain, so evaluation and benchmarks matter as much as the prediction itself.
- **Time order matters:** time-series validation and avoiding look-ahead bias are critical for any market-related modeling.
- **Implementation details change results:** NaN handling, feature alignment, and signal timing can significantly affect backtest outcomes.
- **Team workflow:** we learned knowledges about stocks and trading, practiced machine learning and integrated code, debugged together, and communicating design choices clearly.

## What's next 
