"""Tiny JSON save file next to main.py (gitignored)."""
import json
from pathlib import Path

SAVE_FILE = Path(__file__).resolve().parent.parent / "save.json"


def load():
    try:
        return json.loads(SAVE_FILE.read_text())
    except (OSError, ValueError):
        return {}


def store(data):
    try:
        SAVE_FILE.write_text(json.dumps(data, indent=2))
    except OSError:
        pass  # a read-only folder must never crash the game


def high_score():
    return load().get("high_score", 0)


def submit_score(score):
    """Save `score` if it beats the record. Returns True on a new record."""
    data = load()
    if score > data.get("high_score", 0):
        data["high_score"] = score
        store(data)
        return True
    return False
