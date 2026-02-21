import os
import pandas as pd
import yfinance as yf

SECTOR_ETFS = {
    "XLB": "Materials",
    "XLE": "Energy",
    "XLF": "Financials",
    "XLI": "Industrials",
    "XLK": "Technology",
    "XLP": "Consumer Staples",
    "XLU": "Utilities",
    "XLV": "Healthcare",
    "XLY": "Consumer Discretionary",
}

DEFAULT_TICKERS = list(SECTOR_ETFS.keys()) + ["SPY"]


def download_adj_close(tickers=DEFAULT_TICKERS, start="2010-01-01", end=None) -> pd.DataFrame:
    df = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        group_by="column",
        threads=True,
    )
    if df.empty:
        raise RuntimeError("No data downloaded. Check tickers or internet.")

    # MultiIndex columns for multiple tickers
    if isinstance(df.columns, pd.MultiIndex):
        prices = df["Adj Close"].copy()
    else:
        # single-ticker fallback
        prices = df.rename(columns={"Adj Close": tickers[0]})[tickers[0]].to_frame()

    prices.index = pd.to_datetime(prices.index)
    prices = prices.sort_index()
    return prices


def clean_prices(prices: pd.DataFrame, max_missing_frac_per_ticker=0.02) -> pd.DataFrame:
    prices = prices.dropna(how="all")
    prices = prices.ffill()

    missing_frac = prices.isna().mean().sort_values(ascending=False)
    keep_cols = missing_frac[missing_frac <= max_missing_frac_per_ticker].index.tolist()

    cleaned = prices[keep_cols].dropna()
    return cleaned


def save_prices(output_path="data/prices.csv", tickers=DEFAULT_TICKERS, start="2010-01-01", end=None) -> pd.DataFrame:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    prices = download_adj_close(tickers=tickers, start=start, end=end)
    prices = clean_prices(prices)

    prices.to_csv(output_path)

    print(f"✓ Saved: {output_path}")
    print(f"  Tickers saved ({prices.shape[1]}): {list(prices.columns)}")
    print(f"  Rows (trading days): {prices.shape[0]}")
    print(f"  Date range: {prices.index.min().date()} -> {prices.index.max().date()}")
    return prices


if __name__ == "__main__":
    save_prices()