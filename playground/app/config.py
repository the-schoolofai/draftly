import os
from pathlib import Path

from dotenv import load_dotenv


# Load playground/.env no matter which folder the script is run from
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

PROVIDER = os.getenv("PROVIDER", "ollama").strip()
MODEL = os.getenv("MODEL", "qwen3.5:4b").strip()
API_KEY = os.getenv("API_KEY", "").strip()

DB_URI = os.getenv("DB_URI", "").strip()

if PROVIDER != "ollama" and not API_KEY:
    raise SystemExit(f"PROVIDER is '{PROVIDER}' but API_KEY is empty. Set it in .env")

if not DB_URI:
    raise SystemExit("DB_URI is empty. Set it in .env")
