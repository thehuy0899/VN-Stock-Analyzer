import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def load_json(ticker: str, filename: str) -> dict:
    filepath = KNOWLEDGE_DIR / ticker / filename

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)