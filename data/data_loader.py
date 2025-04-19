import os
import pandas as pd
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from polygon import RESTClient
from dotenv import load_dotenv

load_dotenv()

# ========================
# GHLCV Data Loaders
# ========================

def get_yfinance_ghlcv(ticker, period="1y", interval="1d"):
    df = yf.download(ticker, period=period, interval=interval)
    df = df.rename(columns={
        'Open': 'O', 'High': 'H', 'Low': 'L', 'Close': 'C', 'Volume': 'V'
    })
    df = df[['O', 'H', 'L', 'C', 'V']]
    df.index = pd.to_datetime(df.index)
    return df

def get_alpha_vantage_ghlcv(ticker):
    key = os.getenv("ALPHA_VANTAGE_API_KEY")
    ts = TimeSeries(key, output_format='pandas')
    data, _ = ts.get_daily(symbol=ticker, outputsize='compact')
    data = data.rename(columns={
        '1. open': 'O', '2. high': 'H', '3. low': 'L', '4. close': 'C', '5. volume': 'V'
    })
    data = data[['O', 'H', 'L', 'C', 'V']]
    data.index = pd.to_datetime(data.index)
    return data

def get_polygon_ghlcv(ticker, timespan="day", multiplier=1, from_date=None, to_date=None):
    api_key = os.getenv("POLYGON_API_KEY")
    client = RESTClient(api_key)
    # Default to last year if no dates provided
    if not from_date or not to_date:
        from datetime import datetime, timedelta
        to_date = datetime.now().date()
        from_date = (to_date - timedelta(days=365))
    aggs = client.get_aggs(
        ticker=ticker,
        multiplier=multiplier,
        timespan=timespan,
        from_=str(from_date),
        to=str(to_date),
        limit=365
    )
    df = pd.DataFrame([{
        "O": agg.open,
        "H": agg.high,
        "L": agg.low,
        "C": agg.close,
        "V": agg.volume,
        "timestamp": pd.to_datetime(agg.timestamp, unit='ms')
    } for agg in aggs])
    if not df.empty:
        df = df.set_index("timestamp")
        df = df[['O', 'H', 'L', 'C', 'V']]
    return df

# ========================
# Fundamental Data Loaders
# ========================

def get_yfinance_fundamental(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    # Extract key fundamentals
    keys = [
        "longName", "sector", "industry", "marketCap", "trailingPE", "forwardPE",
        "pegRatio", "dividendYield", "payoutRatio", "profitMargins", "grossMargins",
        "returnOnAssets", "returnOnEquity", "debtToEquity", "currentRatio", "quickRatio",
        "totalCash", "totalDebt", "totalRevenue", "grossProfits", "freeCashflow",
        "operatingMargins", "earningsGrowth", "revenueGrowth"
    ]
    return {k: info.get(k, None) for k in keys}

def get_alpha_vantage_fundamental(ticker):
    key = os.getenv("ALPHA_VANTAGE_API_KEY")
    fd = FundamentalData(key, output_format='pandas')
    # Example: Get company overview
    data, _ = fd.get_company_overview(symbol=ticker)
    return data.T.to_dict()[0] if not data.empty else {}

def get_polygon_fundamental(ticker):
    api_key = os.getenv("POLYGON_API_KEY")
    client = RESTClient(api_key)
    try:
        fundamentals = client.get_reference_financials(symbol=ticker, limit=1)
        # Flatten and return the most recent
        if fundamentals and fundamentals.results:
            return fundamentals.results[0]
        return {}
    except Exception as e:
        print(f"Polygon fundamental error: {e}")
        return {}

# ========================
# Internal Data Loader (Example)
# ========================

def get_internal_data(path="data/internal.csv"):
    """Load internal data from CSV or other source."""
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

# ========================
# Unified Data Fetcher
# ========================

def fetch_all_data(ticker, ghlcv_source="yfinance", fundamental_source="yfinance", internal_path=None):
    # GHLCV
    if ghlcv_source == "yfinance":
        ghlcv = get_yfinance_ghlcv(ticker)
    elif ghlcv_source == "alpha_vantage":
        ghlcv = get_alpha_vantage_ghlcv(ticker)
    elif ghlcv_source == "polygon":
        ghlcv = get_polygon_ghlcv(ticker)
    else:
        raise ValueError("Unknown GHLCV source")

    # Fundamental
    if fundamental_source == "yfinance":
        fundamental = get_yfinance_fundamental(ticker)
    elif fundamental_source == "alpha_vantage":
        fundamental = get_alpha_vantage_fundamental(ticker)
    elif fundamental_source == "polygon":
        fundamental = get_polygon_fundamental(ticker)
    else:
        raise ValueError("Unknown fundamental source")

    # Internal
    internal = get_internal_data(internal_path) if internal_path else None

    return {
        "ghlcv": ghlcv,
        "fundamental": fundamental,
        "internal": internal
    }
