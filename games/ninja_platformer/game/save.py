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


def best_time():
    """Fastest full run in seconds, or None if the game was never finished."""
    return load().get("best_time")


def submit_time(seconds):
    """Save `seconds` if it beats the fastest run. Returns True on a new record."""
    data = load()
    best = data.get("best_time")
    if best is None or seconds < best:
        data["best_time"] = round(seconds, 3)
        store(data)
        return True
    return False
