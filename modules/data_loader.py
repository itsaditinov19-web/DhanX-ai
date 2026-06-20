import streamlit as st
import pandas as pd
import ccxt
import yfinance as yf


# =========================================================
# MAIN DATA LOADER
# =========================================================

@st.cache_data(ttl=120)

def load_market_data(

    symbol,

    timeframe,

    limit

):

    crypto_assets = [

        "BTC/USDT",

        "ETH/USDT"
    ]

    if symbol in crypto_assets:

        return load_binance_data(

            symbol,

            timeframe,

            limit
        )

    else:

        return load_yfinance_data(

            symbol,

            timeframe,

            limit
        )


# =========================================================
# BINANCE DATA
# =========================================================

def load_binance_data(

    symbol,

    timeframe,

    limit
):

    exchange = ccxt.binance()

    candles = exchange.fetch_ohlcv(

        symbol,

        timeframe=timeframe,

        limit=limit
    )

    df = pd.DataFrame(

        candles,

        columns=[

            "timestamp",

            "open",

            "high",

            "low",

            "close",

            "volume"
        ]
    )

    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        unit="ms"
    )

    return df


# =========================================================
# YFINANCE DATA
# =========================================================

def load_yfinance_data(

    symbol,

    timeframe,

    limit
):

    interval_map = {

        "1m": "1m",

        "5m": "5m",

        "15m": "15m",

        "1h": "1h",

        "1d": "1d"
    }

    symbol_map = {

        "NIFTY50": "^NSEI",

        "BANKNIFTY": "^NSEBANK",

        "RELIANCE": "RELIANCE.NS",

        "TCS": "TCS.NS",

        "GOLD": "GC=F",

        "SILVER": "SI=F",

        "USDINR": "INR=X"
    }

    yf_symbol = symbol_map.get(

        symbol,

        symbol
    )

    data = yf.download(

        yf_symbol,

        interval=interval_map[timeframe],

        period="7d",

        progress=False
    )

    data.reset_index(inplace=True)

    data = data.rename(columns={

        "Datetime": "timestamp",

        "Date": "timestamp",

        "Open": "open",

        "High": "high",

        "Low": "low",

        "Close": "close",

        "Volume": "volume"
    })

    df = data[[

        "timestamp",

        "open",

        "high",

        "low",

        "close",

        "volume"
    ]]

    return df.tail(limit)