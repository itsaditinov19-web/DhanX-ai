import numpy as np


# =========================================================
# ADVANCED AI CONFIDENCE ENGINE
# =========================================================

def calculate_confidence(

    trend,
    macd_status,
    rsi,
    volume_strength,
    structure

):

    confidence = 50

    reasons = []

    # =====================================================
    # TREND ANALYSIS
    # =====================================================

    if trend == "Bullish":

        confidence += 10
        reasons.append("Bullish EMA Trend")

    else:

        confidence += 5
        reasons.append("Bearish EMA Trend")

    # =====================================================
    # MACD ANALYSIS
    # =====================================================

    if macd_status == "Bullish":

        confidence += 15
        reasons.append("Bullish MACD Momentum")

    else:

        confidence -= 10
        reasons.append("Bearish MACD Pressure")

    # =====================================================
    # RSI ANALYSIS
    # =====================================================

    if 45 <= rsi <= 65:

        confidence += 15
        reasons.append("Healthy RSI Momentum")

    elif rsi > 70:

        confidence -= 15
        reasons.append("Overbought RSI")

    elif rsi < 30:

        confidence += 10
        reasons.append("Oversold Reversal Zone")

    else:

        confidence += 5
        reasons.append("Neutral RSI")

    # =====================================================
    # VOLUME ANALYSIS
    # =====================================================

    if volume_strength == "HIGH":

        confidence += 10
        reasons.append("Strong Volume Confirmation")

    else:

        confidence -= 5
        reasons.append("Weak Volume")

    # =====================================================
    # MARKET STRUCTURE
    # =====================================================

    if structure == "BULLISH":

        confidence += 10
        reasons.append("Bullish Market Structure")

    elif structure == "BEARISH":

        confidence -= 10
        reasons.append("Bearish Market Structure")

    # =====================================================
    # LIMITS
    # =====================================================

    confidence = max(1, min(confidence, 100))

    # =====================================================
    # FINAL SIGNAL
    # =====================================================

    if trend == "Bullish":

        if confidence >= 80:

            signal = "STRONG BUY"

        elif confidence >= 65:

            signal = "BUY"

        else:

            signal = "WAIT"

    elif trend == "Bearish":

        if confidence <= 30:

            signal = "STRONG SELL"

        elif confidence <= 45:

            signal = "SELL"

        else:

            signal = "WAIT"

    else:

        signal = "WAIT"

    return {
        "signal": signal,
        "confidence": confidence,
        "reasons": reasons
    }