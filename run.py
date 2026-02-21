import os
import sys
import subprocess

REQ = ["pandas", "yfinance", "numpy"]

SECTOR_ETFS = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY"]
TICKERS = SECTOR_ETFS + ["SPY"]

START = "2010-01-01"
OUT_PATH = os.path.join("data", "prices.csv")


def ensure_packages():
    missing = []
    for pkg in REQ:
        try:
            __import__(pkg)
        except Exception:
            missing.append(pkg)

    if missing:
        print(f"[setup] Missing packages: {missing}")
        print("[setup] Installing with pip using current Python...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])


def download_and_save():
    import pandas as pd
    import yfinance as yf

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    print(f"[data] Downloading Adj Close for {len(TICKERS)} tickers from {START} to today...")
    df = yf.download(
        TICKERS,
        start=START,
        end=None,
        auto_adjust=False,
        progress=False,
        group_by="column",
        threads=True,
    )

    if df.empty:
        raise RuntimeError("No data downloaded. Check internet connection or Yahoo availability.")

    # Extract Adj Close (handles multi-ticker MultiIndex)
    if isinstance(df.columns, pd.MultiIndex):
        prices = df["Adj Close"].copy()
    else:
        prices = df.rename(columns={"Adj Close": TICKERS[0]})[TICKERS[0]].to_frame()

    prices.index = pd.to_datetime(prices.index)
    prices = prices.sort_index()

    # Basic research cleaning
    prices = prices.dropna(how="all").ffill()
    prices = prices.dropna()  # drop any remaining rows with missing values

    prices.to_csv(OUT_PATH)

    print(f"[ok] Saved: {OUT_PATH}")
    print(f"[ok] Date range: {prices.index.min().date()} -> {prices.index.max().date()}")
    print(f"[ok] Columns: {list(prices.columns)}")
    print(f"[ok] Rows: {prices.shape[0]}")


def main():
    ensure_packages()
    download_and_save()


if __name__ == "__main__":
    main()