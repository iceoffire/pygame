"""Constants for the Particle System demo. Distances in pixels, time in seconds."""
from pathlib import Path

TITLE = "Particle System"
SCREEN_SIZE = (500, 500)
FPS = 120

IMAGES = Path(__file__).resolve().parent / "assets" / "images"
FIRE_IMAGE = IMAGES / "fire.png"
TORCH_IMAGE = IMAGES / "torch.png"
GLOW_IMAGE = IMAGES / "glow.png"

TORCH_SCALE = 1.4
TORCH_OFFSET = (0, 4)     # torch top-center relative to the mouse
GLOW_OFFSET = (0, 10)     # glow center relative to the mouse

# Spawn rate ("intensity") in particles per second; the mouse wheel changes it.
SPAWN_RATE = 400
SPAWN_RATE_STEP = 50
SPAWN_RATE_MIN = 0
SPAWN_RATE_MAX = 2000
MAX_PARTICLES = 1500

PARTICLE_SPEED = (90, 160)       # px/s, random range
PARTICLE_ANGLE = (230, 310)      # degrees; 270 is straight up
PARTICLE_LIFETIME = (0.25, 0.6)  # seconds, random range
PARTICLE_SCALE = (0.5, 2.0)      # start size relative to fire.png (16 px)
PARTICLE_JITTER_X = 4            # random horizontal spawn offset

# Cached fire images: one per pixel size and per brightness level.
BRIGHTNESS_LEVELS = 16

BACKGROUND_COLOR = (20, 20, 20)
TEXT_COLOR = (230, 230, 230)
FONT_SIZE = 22
