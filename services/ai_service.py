import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELS = ["gemini-2.5-flash-lite", "gemini-3.5-flash", "gemini-3.8-flash"]

def generate_ai_reply(prompt: str) -> str:
    for model_name in MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text
        except Exception:
            continue
    return f"[Offline Fallback — Gemini busy] Simulated AI answer for: '{prompt}'"
