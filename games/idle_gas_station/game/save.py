"""Tiny JSON save file next to main.py (gitignored)."""
import json
import os
import tempfile
from pathlib import Path

SAVE_FILE = Path(__file__).resolve().parent.parent / "save.json"
if os.environ.get("SMOKE_FRAMES"):
    # Headless smoke runs must not touch the player's real progress.
    SAVE_FILE = Path(tempfile.gettempdir()) / "idle_gas_station_smoke_save.json"


def load():
    try:
        data = json.loads(SAVE_FILE.read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def store(data):
    try:
        SAVE_FILE.write_text(json.dumps(data, indent=2))
    except OSError:
        pass  # a read-only folder must never crash the game
