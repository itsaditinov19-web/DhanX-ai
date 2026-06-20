from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("OPENROUTER_CHART_KEY")

print(API_KEY[:15])

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "openai/gpt-4o-mini",
        "max_tokens": 50,
        "messages": [
            {
                "role": "user",
                "content": "Hello"
            }
        ]
    }
)

print(response.json())