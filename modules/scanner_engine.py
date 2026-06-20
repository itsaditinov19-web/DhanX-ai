

import ta
import ccxt
import pandas as pd


from modules.ai_signal_engine import generate_ai_signal


exchange = ccxt.binance()
# =========================================================
# COINS TO SCAN
# =========================================================

COINS = [

    "BTC/USDT",

    "ETH/USDT",

    "SOL/USDT",

    "BNB/USDT",

    "XRP/USDT",

    "DOGE/USDT",

    "LINK/USDT",

    "MATIC/USDT"
]



# =========================================================
# MARKET SCANNER
# =========================================================

def scan_market(

    timeframe="5m",

    limit=200
):

    results = []

    # =====================================================
    # LOOP THROUGH COINS
    # =====================================================

    for symbol in COINS:

        try:

            # =============================================
            # FETCH DATA
            # =============================================

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

            # =============================================
            # INDICATORS
            # =============================================

            df["ema20"] = ta.trend.ema_indicator(

                df["close"],

                window=20
            )

            df["ema50"] = ta.trend.ema_indicator(

                df["close"],

                window=50
            )

            df["rsi"] = ta.momentum.rsi(

                df["close"],

                window=14
            )

            macd = ta.trend.MACD(

                df["close"]
            )

            df["macd"] = macd.macd()

            df["macd_signal"] = macd.macd_signal()

            # =============================================
            # AI ANALYSIS
            # =============================================

            ai_result = generate_ai_signal(df)

            results.append({

                "symbol": symbol,

                "signal": ai_result["signal"],

                "confidence": ai_result["confidence"],

                "trend": ai_result["trend"],

                "rsi": ai_result["rsi"],

                "support": ai_result["support"],

                "resistance": ai_result["resistance"]
            })

        except:

            continue

    # =====================================================
    # SORT BEST SIGNALS
    # =====================================================

    results = sorted(

        results,

        key=lambda x: x["confidence"],

        reverse=True
    )

    return results