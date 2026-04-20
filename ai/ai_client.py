# ai/ai_client.py

import os
from dotenv import load_dotenv
from google import genai

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

# =========================
# GET CLIENT
# =========================
def get_ai_client():
    # Stelle sicher, dass in deiner .env "GOOGLE_API_KEY" steht
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "❌ GOOGLE_API_KEY not found. "
            "Create a .env file in project root and add: GOOGLE_API_KEY=your_key"
        )

    client = genai.Client(api_key=api_key)
    return client

# =========================
# OPTIONAL TEST
# =========================
def test_connection():
    client = get_ai_client()

    # FIX: Hier "gemini-flash-latest" nutzen, da dies in deinem Test funktioniert hat
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Say hello in one short sentence."
    )

    print("✅ AI connection successful:")
    print(response.text)

if __name__ == "__main__":
    test_connection()
