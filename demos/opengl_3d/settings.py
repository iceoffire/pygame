"""Constants for the OpenGL 3D demo."""
from pathlib import Path

TITLE = "OpenGL 3D"
SCREEN_SIZE = (640, 480)
FPS = 60

TEXTURE = Path(__file__).resolve().parent / "assets" / "textures" / "dirt.jpg"

FIELD_OF_VIEW = 45     # degrees
NEAR_PLANE = 0.1
FAR_PLANE = 200.0
START_DISTANCE = -5.0  # camera starts 5 units in front of the cube

ROTATE_SPEED = 60      # degrees per second
MOVE_SPEED = 3.0       # units per second

CONTROLS = "A/S/D rotate X/Y/Z, R/F zoom out/in, arrows move, Esc quit"
