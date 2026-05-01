import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
else:
    try:
        client = genai.Client(api_key=api_key)
        print("AVAILABLE MODELS:")
        for model in client.models.list():
            print(model.name)
    except Exception as e:
        print(f"API ERROR: {e}")
