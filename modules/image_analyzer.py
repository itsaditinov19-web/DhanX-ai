import os
import base64
import requests

import google.generativeai as genai

from dotenv import load_dotenv
from PIL import Image

print("===== IMAGE_ANALYZER V3 LOADED =====")
# ============================================
# LOAD ENV
# ============================================

load_dotenv()

ACTIVE_AI = os.getenv("ACTIVE_AI")
print("ACTIVE_AI =", ACTIVE_AI)
OPENROUTER_CHART_KEY = os.getenv(
    "OPENROUTER_CHART_KEY"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

CHART_MEMORY = {
    "symbol": "",
    "exchange": "",
    "timeframe": "",
    "current_price": "",
    "trend": "",
    "market_structure": "",
    "support": [],
    "resistance": [],
    "bias": "",
    "confidence": "",
    "entry": "",
    "stop_loss": "",
    "target1": "",
    "target2": "",
    "invalidation": ""
}

# ============================================
# CHART MEMORY
# ============================================

LAST_CHART_ANALYSIS = ""
if OPENROUTER_CHART_KEY:
    print(
        "OPENROUTER_CHART_KEY =",
        OPENROUTER_CHART_KEY[:10]
    )
else:
    print("OPENROUTER_CHART_KEY not found")
# ============================================
# GEMINI SETUP
# ============================================

if GEMINI_API_KEY:

    genai.configure(
        api_key=GEMINI_API_KEY
    )

    gemini_model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )


# ============================================
# PROMPT
# ============================================

PROMPT = """
You are DhanX AI Professional Trading Analyst.

Your job is to analyze the uploaded chart exactly like a professional trader, hedge fund analyst, or institutional technical analyst.

IMPORTANT RULES

* Analyze ONLY what is visible in the chart.
* Never invent prices.
* Never invent indicators.
* Never assume timeframe, symbol, exchange, or market conditions if not visible.
* If information is unclear, explicitly state:
  "Not clearly visible on chart."

==================================================
STEP 1: CHART IDENTIFICATION
============================

Identify if visible:

* Symbol
* Exchange
* Timeframe
* Current Price

==================================================
STEP 2: MARKET CONTEXT
======================

Determine:

* Market Structure

  * Higher Highs Higher Lows
  * Lower Highs Lower Lows
  * Range Bound
  * Compression
  * Expansion

* Overall Trend

  * Strong Bullish
  * Bullish
  * Neutral
  * Bearish
  * Strong Bearish

Explain why.

==================================================
STEP 3: PRICE ACTION ANALYSIS
=============================

Identify:

* Break of Structure (BOS)
* Change of Character (CHOCH)
* Trendline Breaks
* Key Swing Highs
* Key Swing Lows

Explain the significance.

==================================================
STEP 4: SUPPORT & RESISTANCE
============================

Identify:

* Major Support Zones
* Major Resistance Zones
* Nearest Support
* Nearest Resistance

Only if visible.

==================================================
STEP 5: CANDLESTICK ANALYSIS
============================

Identify visible patterns:

* Bullish Engulfing
* Bearish Engulfing
* Pin Bar
* Hammer
* Shooting Star
* Doji
* Inside Bar
* Outside Bar

Explain whether the pattern is meaningful or weak.

==================================================
STEP 6: VOLUME ANALYSIS
=======================

If volume is visible:

* Rising Volume
* Falling Volume
* Volume Confirmation
* Volume Divergence

Explain what it suggests.

If volume is not visible:

State:
"Volume not visible."

==================================================
STEP 7: INDICATOR ANALYSIS
==========================

Analyze ONLY indicators visible on the chart.

Examples:

* RSI
* MACD
* Moving Averages
* VWAP
* Bollinger Bands

For each indicator:

* Current reading
* Bullish / Bearish implication

If no indicators exist:

State:
"No indicators visible."

==================================================
STEP 8: TRADE SETUP
===================

If the chart is clear enough:

Provide:

Trade Direction:

* Long
* Short
* No Trade

Entry Zone

Stop Loss

Target 1

Target 2

Risk Reward Ratio

Trade Confidence:

* Low
* Medium
* High

Explain WHY.

If chart quality is poor:

State:
"No high-confidence trade setup available."

==================================================
STEP 9: RISK ANALYSIS
=====================

Mention:

* Main risk to this setup
* Invalidating condition
* What would make the analysis wrong

==================================================
STEP 10: PROFESSIONAL CONCLUSION
================================

Provide:

Trading Bias:

* Bullish
* Bearish
* Neutral

Confidence:

* Low
* Medium
* High

Final Summary:
3-6 professional trading sentences.

==================================================
STRICT RULES
============
If volume is not visible, NEVER discuss volume later in the response.
* Never guarantee profits.
* Never say a trade will definitely work.
* Never predict the future with certainty.
* Think like a professional trader.
* Use evidence from the chart.
* Keep explanations concise but actionable.
* Prioritize risk management.
"""
CHART_QA_PROMPT = """
You are DhanX Professional Trading Analyst.

Use BOTH:

1. Previous chart analysis
2. Uploaded chart image

Priority:

- Use previous analysis first.
- Use image only for confirmation.

If trend/support/resistance/entry/stop/target
already exist in previous analysis,
use them.

Never answer:

'Not visible on chart'
If volume is not visible, NEVER discuss volume later in the response.
if previous analysis already contains the answer.

Keep answers short.

Answer like a professional trader.
"""

# ============================================
# ENCODE IMAGE
# ============================================

def encode_image(image_path):

    with open(image_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# ============================================
# GEMINI ANALYSIS
# ============================================

def analyze_with_gemini(image_path):

    image = Image.open(image_path)

    response = gemini_model.generate_content(
        [PROMPT, image]
    )

    return response.text

def analyze_with_openrouter(image_path):
    print("OPENROUTER CALLED")
    print("MAX TOKENS = 1200")
    print("===== ANALYZE_WITH_OPENROUTER CALLED =====")
    base64_image = encode_image(image_path)
    try:
        print("MAX TOKENS SHOULD BE 1200")
        response = requests.post(

            url="https://openrouter.ai/api/v1/chat/completions",

            headers={

                "Authorization":
                f"Bearer {OPENROUTER_CHART_KEY}",

                "Content-Type":
                "application/json"
            },

            json={

                "model":
                "openai/gpt-4o-mini",
                "max_tokens": 1200,
                "messages": [

                    {
                        "role": "user",

                        "content": [

                            {
                                "type": "text",
                                "text": PROMPT
                            },

                            {
                                "type": "image_url",

                                "image_url": {

                                    "url":
                                    f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            },
            timeout=60
        )

        result = response.json()
    except Exception as e:

        return f"Error: {str(e)}"
    if "choices" not in result:
        return f"ERROR: {result}"

    return result["choices"][0]["message"]["content"]
# ============================================
# OPENROUTER ANALYSIS
# ============================================
def ask_chart_question_openrouter(
    image_path,
    question
):

    base64_image = encode_image(
        image_path
    )
    try:
        response = requests.post(

            url="https://openrouter.ai/api/v1/chat/completions",

            headers={

                "Authorization":
                f"Bearer {OPENROUTER_CHART_KEY}",

                "Content-Type":
                "application/json"
            },

            json={

                "model":
                "openai/gpt-4o-mini",
                "max_tokens": 1200,
                "messages": [

                    {
                        "role": "user",

                        "content": [

                            {
                                "type": "text",
                                "text":
                                f"""
                                Previous Analysis:

                                {LAST_CHART_ANALYSIS}

                                Question:

                                {question}

                                {CHART_QA_PROMPT}
                                """
                            },

                            {
                                "type": "image_url",

                                "image_url": {

                                    "url":
                                    f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            }
        )

        result = response.json()
    except Exception as e:

        return f"Error: {str(e)}"
    if "choices" not in result:
        return f"ERROR: {result}"

    return result[
        "choices"
    ][0]["message"]["content"]


# ============================================
# MAIN SWITCHER
# ============================================

def analyze_chart_image(image_path):

    global LAST_CHART_ANALYSIS

    if ACTIVE_AI == "GEMINI":

        print("\nUsing Gemini AI...\n")

        result = analyze_with_gemini(
            image_path
        )

        LAST_CHART_ANALYSIS = result

        return result

    elif ACTIVE_AI == "OPENROUTER":

        print("\nUsing OpenRouter AI...\n")

        result = analyze_with_openrouter(
            image_path
        )
        
        LAST_CHART_ANALYSIS = result[:2500]
        return result

    else:

        return "Invalid ACTIVE_AI setting in .env"
    
def answer_chart_question(
    image_path,
    question
):

    if ACTIVE_AI == "OPENROUTER":

        question_lower = question.lower()

        future_keywords = [
            "tomorrow",
            "next candle",
            "next move",
            "future",
            "predict",
            "prediction",
            "price tomorrow",
            "where will btc go",
            "where will price go",
            "btc tomorrow",
            "price prediction",
            "future price"
        ]

        if any(
            word in question_lower
            for word in future_keywords
        ):

            return """
Future price cannot be determined from a chart.

Markets are uncertain and no future price can be guaranteed.

Please use the visible trend, support, resistance, and market structure from the chart analysis instead of relying on predictions.
"""

        return ask_chart_question_openrouter(
            image_path,
            question
        )


    elif ACTIVE_AI == "GEMINI":

        image = Image.open(
            image_path
        )

        response = gemini_model.generate_content(

            [
                f"""
                Previous Analysis:

                {LAST_CHART_ANALYSIS}

                {CHART_QA_PROMPT}

                Question:

                {question}
                """,
                image
            ]

        )

        return response.text