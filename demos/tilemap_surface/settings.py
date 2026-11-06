"""Constants for the Tilemap Surface demo."""
from pathlib import Path

TITLE = "Tilemap Surface"
SCREEN_SIZE = (640, 500)
FPS = 60

IMAGES = Path(__file__).resolve().parent / "assets" / "images"
MAPS = {1: IMAGES / "maps" / "map_1.png", 2: IMAGES / "maps" / "map_2.png"}
FLOOR_TILE = IMAGES / "tiles" / "floor_mf.png"

TILE_SIZE = 128              # each map pixel becomes one 128 x 128 tile
FLOOR_COLOR = (0, 0, 0)      # map pixels of this color become floor tiles

BACKGROUND_COLOR = (30, 30, 40)
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0)
FONT_SIZE = 26
