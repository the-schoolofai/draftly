import os
from dotenv import load_dotenv


load_dotenv(".env")

PROVIDER = os.getenv("PROVIDER", "ollama")
MODEL = os.getenv("MODEL", "llama3.2")

if PROVIDER == "google_genai" and os.getenv("GOOGLE_API_KEY", "") == "":
    raise SystemExit("PROVIDER is google_genai but GOOGLE_API_KEY is empty. " \
    "Add it to your .env file.")
