import requests
import pandas as pd
import time
from datetime import datetime

API_KEY = "E6VTTLWAQQWI6A00"

symbols = [
    "RELIANCE.BSE", "TCS.BSE", "INFY.BSE", "HDFCBANK.BSE", "ICICIBANK.BSE",
    "SBIN.BSE", "ITC.BSE", "HINDUNILVR.BSE", "LT.BSE", "AXISBANK.BSE",
    "KOTAKBANK.BSE", "BAJFINANCE.BSE", "BHARTIARTL.BSE", "ASIANPAINT.BSE", "MARUTI.BSE",
    "SUNPHARMA.BSE", "WIPRO.BSE", "ONGC.BSE", "TITAN.BSE", "POWERGRID.BSE"
]

# ✅ change this year if you want
YEAR = 2025

def fetch_stock_data(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",   # ✅ FREE endpoint
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "full"               # ✅ full history (needed for 1 year daily)
    }

    r = requests.get(url, params=params)
    data = r.json()

    # Rate limit / errors
    if "Note" in data:
        print("⚠️ RATE LIMIT HIT. Wait 1 minute & rerun.")
        print(data["Note"])
        return None

    if "Error Message" in data:
        print(f"❌ Invalid Symbol: {symbol}")
        return None

    if "Information" in data:
        print(f"⚠️ INFO for {symbol}: {data['Information']}")
        return None

    ts_key = "Time Series (Daily)"
    if ts_key not in data:
        print(f"❌ Data not found for {symbol}")
        return None

    df = pd.DataFrame.from_dict(data[ts_key], orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()

    # ✅ Filter only full YEAR daily-wise data
    start_date = pd.Timestamp(f"{YEAR}-01-01")
    end_date = pd.Timestamp(f"{YEAR}-12-31")
    df = df[(df.index >= start_date) & (df.index <= end_date)]

    return df


all_data = {}

for i, sym in enumerate(symbols, start=1):
    print(f"✅ ({i}/20) Fetching: {sym}")
    df = fetch_stock_data(sym)

    if df is not None and len(df) > 0:
        all_data[sym] = df

        # ✅ Save each company's data year-wise daily to CSV
        safe_name = sym.replace(".", "_")
        filename = f"{safe_name}_{YEAR}_daily.csv"
        df.to_csv(filename)
        print(f"📁 Saved: {filename} | Rows: {len(df)}")
    else:
        print(f"⚠️ No yearly data saved for {sym}")

    # ✅ IMPORTANT delay (Alpha Vantage free limit)
    time.sleep(15)

print("\n✅ DONE! Total companies fetched successfully:", len(all_data))
