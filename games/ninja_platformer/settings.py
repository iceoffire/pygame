import pygame

TITLE = "Ninja Platformer"
SCREEN_SIZE = (700, 550)
FPS = 60

# Colors
BACKGROUND = (16, 18, 32)
TEXT = (235, 235, 245)
MUTED = (150, 155, 180)
ACCENT = (255, 205, 90)
SHADOW = (0, 0, 0)

# World
TILE_SIZE = 128     # every pixel of a map image becomes one 128x128 tile
PLAYER_SCALE = 4    # player sprites are 20x26 and drawn 4x bigger

# Player movement, in pixels per second (the old per-frame values x 60 at 60 FPS)
RUN_ACCEL = 7200          # was +2 px/frame every frame
MAX_RUN_SPEED = 480       # was 8 px/frame
STOP_DAMPING = 2.2        # with no key held, speed is divided by this every 1/60 s
STOP_SPEED = 6            # below this the player just stops
GRAVITY = 7200            # was +2 px/frame every frame
MAX_FALL_SPEED = 2400
JUMP_SPEED = 2040         # ~289 px high, the same peak the old -35 px/frame jump reached
JUMP_CUT = 0.45           # releasing jump early multiplies the upward speed by this
COYOTE_TIME = 0.1         # can still jump this long after walking off a ledge
JUMP_BUFFER_TIME = 0.1    # a jump pressed this long before landing still happens

# Player animation: name -> (frame count, seconds per frame)
PLAYER_ANIMATIONS = {
    "idle": (2, 0.6),
    "running": (4, 0.15),
    "jumping": (3, 0.04),
}

# Camera
CAMERA_SMOOTHING = 0.9    # fraction of the distance still left after 1/60 s
CAMERA_OFFSET_Y = 100     # keep the player a bit above the screen center
CAMERA_LOOK_AHEAD = 90    # pixels shown ahead of the player at full run speed

# Transitions
FADE_TIME = 0.25          # seconds to fade out (and again to fade in)
BANNER_TIME = 1.5         # "MAP N" banner at the start of each map

# Key bindings
LEFT_KEYS = (pygame.K_a, pygame.K_LEFT)
RIGHT_KEYS = (pygame.K_d, pygame.K_RIGHT)
JUMP_KEYS = (pygame.K_SPACE, pygame.K_w, pygame.K_UP)
PAUSE_KEYS = (pygame.K_p, pygame.K_ESCAPE)
RESTART_KEYS = (pygame.K_r,)
