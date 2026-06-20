import ccxt
import pandas as pd


def get_market_context(symbol="BTC/USDT"):

    try:

        exchange = ccxt.binance()

        ohlcv = exchange.fetch_ohlcv(
            symbol,
            timeframe="1h",
            limit=200
        )

        df = pd.DataFrame(
            ohlcv,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        )

        df["EMA50"] = (
            df["close"]
            .ewm(span=50)
            .mean()
        )

        df["EMA200"] = (
            df["close"]
            .ewm(span=200)
            .mean()
        )

        current_price = float(
            df["close"].iloc[-1]
        )

        ema50 = float(
            df["EMA50"].iloc[-1]
        )

        ema200 = float(
            df["EMA200"].iloc[-1]
        )

        if current_price > ema50 > ema200:

            trend = "Strong Bullish"

        elif current_price < ema50 < ema200:

            trend = "Strong Bearish"

        else:

            trend = "Sideways"

        return f"""
Symbol: {symbol}

Current Price: {current_price}

EMA50: {ema50}

EMA200: {ema200}

Market Trend: {trend}
"""

    except Exception as e:

        return f"""
Market Context Unavailable

Reason:
{str(e)}
"""