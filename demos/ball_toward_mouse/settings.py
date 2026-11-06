"""Constants for the Ball Toward Mouse demo. Distances in pixels, time in seconds."""

TITLE = "Ball Toward Mouse"
SCREEN_SIZE = (640, 480)
FPS = 60

# Physics runs in fixed steps so the ball and the trajectory preview match exactly.
PHYSICS_STEP = 1 / 120

BALL_RADIUS = 12
START_POS = (60, 380)
GRAVITY = 3600            # px/s^2 (the old code added 1 px/frame every frame at 60 FPS)
LAUNCH_SCALE = 6.0        # launch speed (px/s) per pixel of distance between ball and mouse
AIR_DRAG_X = 0.98 ** 60   # fraction of horizontal speed kept after one second
RESTITUTION = 0.6         # fraction of speed kept after a bounce
FLOOR_FRICTION = 0.85     # fraction of horizontal speed kept per floor bounce
REST_SPEED = 40           # below this speed (px/s) the ball counts as resting
RESET_DELAY = 0.8         # seconds the ball rests before it resets on its own

PREVIEW_TIME = 1.2        # seconds of trajectory the dotted preview shows
PREVIEW_DOT_EVERY = 4     # one dot every N physics steps

BACKGROUND_COLOR = (0, 0, 0)
BALL_COLOR = (255, 255, 255)
AIM_COLOR = (255, 255, 0)
PREVIEW_COLOR = (120, 120, 120)
FLOOR_COLOR = (60, 60, 60)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 24
