import pandas as pd
import ta

from modules.confidence_engine import calculate_confidence


# =========================================================
# AI SIGNAL ENGINE
# =========================================================

def generate_ai_signal(df):

    # =====================================================
    # INDICATORS
    # =====================================================

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

    macd = ta.trend.MACD(df["close"])

    df["macd"] = macd.macd()

    df["macd_signal"] = macd.macd_signal()

    df["atr"] = ta.volatility.average_true_range(
        df["high"],
        df["low"],
        df["close"],
        window=14
    )

    # =====================================================
    # LATEST VALUES
    # =====================================================

    latest_close = round(
        df["close"].iloc[-1],
        2
    )

    latest_rsi = round(
        df["rsi"].iloc[-1],
        2
    )

    ema20 = df["ema20"].iloc[-1]

    ema50 = df["ema50"].iloc[-1]

    latest_macd = df["macd"].iloc[-1]

    latest_macd_signal = df["macd_signal"].iloc[-1]

    latest_atr = round(
        df["atr"].iloc[-1],
        2
    )

    # =====================================================
    # TREND
    # =====================================================

    if ema20 > ema50:

        trend = "Bullish"

    elif ema20 < ema50:

        trend = "Bearish"

    else:
  
        trend = "Neutral"
    # =====================================================
    # MACD STATUS
    # =====================================================

    macd_status = (
        "Bullish"
        if latest_macd > latest_macd_signal
        else "Bearish"
    )

    # =====================================================
    # RSI STATUS
    # =====================================================

    if latest_rsi > 70:

        rsi_status = "Overbought"

    elif latest_rsi < 30:

        rsi_status = "Oversold"

    else:

        rsi_status = "Neutral"

    # =====================================================
    # VOLUME ANALYSIS
    # =====================================================

    average_volume = df["volume"].rolling(20).mean().iloc[-1]

    current_volume = df["volume"].iloc[-1]

    if current_volume > average_volume:

        volume_strength = "HIGH"

    else:

        volume_strength = "LOW"

    # =====================================================
    # MARKET STRUCTURE
    # =====================================================

    recent_high = df["high"].rolling(20).max().iloc[-1]

    recent_low = df["low"].rolling(20).min().iloc[-1]

    if latest_close > ema20 > ema50:

        market_structure = "BULLISH"

    elif latest_close < ema20 < ema50:

        market_structure = "BEARISH"

    else:

        market_structure = "RANGING"

    # =====================================================
    # SUPPORT & RESISTANCE
    # =====================================================

    support = round(recent_low, 2)

    resistance = round(recent_high, 2)
    score = 0

    if trend == "Bullish":
        score += 30

    if trend == "Bearish":
        score -= 30

    if macd_status == "Bullish":
        score += 25
    else:
        score -= 25

    if latest_rsi < 30:
        score += 15

    elif latest_rsi > 70:
        score -= 15

    if volume_strength == "HIGH":
        score += 10
    # =====================================================
    # ADVANCED CONFIDENCE ENGINE
    # =====================================================

    confidence_result = calculate_confidence(

        trend=trend,

        macd_status=macd_status,

        rsi=latest_rsi,

        volume_strength=volume_strength,

        structure=market_structure
    )

    signal = confidence_result["signal"]

    confidence = confidence_result["confidence"]

    reasons = confidence_result["reasons"]

    # =====================================================
    # RISK MANAGEMENT
    # =====================================================

    stop_loss = round(
        latest_close - (latest_atr * 1.5),
        2
    )

    take_profit = round(
        latest_close + (latest_atr * 3),
        2
    )

    if "SELL" in signal:

        stop_loss = round(
            latest_close + (latest_atr * 1.5),
            2
        )

        take_profit = round(
            latest_close - (latest_atr * 3),
            2
        )
    # =====================================================
    # PREVENT CONTRADICTORY SIGNALS
    # =====================================================

    if trend == "Bearish" and "BUY" in signal:

        signal = "WAIT"
        confidence = min(confidence, 50)

        reasons.append(
            "Bullish signal rejected because trend is bearish"
        )

    if trend == "Bullish" and "SELL" in signal:

        signal = "WAIT"
        confidence = min(confidence, 50)

        reasons.append(
            "Bearish signal rejected because trend is bullish"
        )
    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "signal": signal,

        "confidence": confidence,

        "trend": trend,

        "macd": macd_status,

        "rsi": latest_rsi,

        "rsi_status": rsi_status,

        "atr": latest_atr,

        "support": support,

        "resistance": resistance,

        "stop_loss": stop_loss,

        "take_profit": take_profit,

        "reasons": reasons
    }