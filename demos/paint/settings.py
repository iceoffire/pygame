"""Constants for the Paint demo."""
from pathlib import Path

TITLE = "Paint"
SCREEN_SIZE = (800, 600)
FPS = 60

SAVE_DIR = Path(__file__).resolve().parent   # S saves painting_YYYYMMDD_HHMMSS.png here

# Left UI panel; the canvas fills the rest of the window.
PANEL_WIDTH = 100
PANEL_COLOR = (200, 200, 200)
CANVAS_COLOR = (255, 255, 255)

# Red / green / blue gradient bars: bright at the top, black at the bottom.
BAR_TOP = 40
BAR_HEIGHT = 320
BAR_WIDTH = 16
BAR_XS = (14, 42, 70)
BAR_OUTLINE = (0, 0, 0)
MARKER_COLOR = (0, 0, 0)

SWATCH_RECT = (14, 375, 72, 40)

START_COLOR = (150, 200, 150)
BRUSH_SIZE = 4        # brush radius in pixels
BRUSH_SIZE_MIN = 1
BRUSH_SIZE_MAX = 50

TEXT_COLOR = (20, 20, 20)
FONT_SIZE = 20
MESSAGE_TIME = 2.0    # seconds the "Saved ..." message stays on screen
