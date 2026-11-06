TITLE = "Block Breaker"
SCREEN_SIZE = (800, 600)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
FPS = 60

# Colors
BACKGROUND = (0, 0, 0)
TEXT = (255, 255, 255)
MUTED = (150, 150, 170)
OUTLINE = (255, 255, 255)
PADDLE_COLOR = (100, 100, 200)
BALL_COLOR = (255, 255, 255)
# Multi-hit bricks are drawn in these colors while they have more than 1 HP left.
BRICK_HP_COLORS = {2: (240, 170, 40), 3: (230, 60, 60)}

# HUD
HUD_FONT_SIZE = 28
HUD_LIVES_X = 100         # x of the first life circle
HUD_LIVES_SPACING = 30
HUD_LIVES_RADIUS = 13
PLAY_TOP = 36             # the ball bounces off this line (below the HUD)

# Bricks (grid inherited from the original game: 15 columns of 52 x 15 px)
BRICK_COLUMNS = 15
BRICK_LEFT = 10
BRICK_TOP = 40
BRICK_WIDTH = 780 / BRICK_COLUMNS
BRICK_HEIGHT = 15

# Paddle (speeds are units per second, not per frame)
FLOOR_LEVEL = 550         # top of the paddle
PADDLE_SIZE = (160, 20)
PADDLE_SPEED = 480

# Ball
BALL_RADIUS = 10
BALL_SPEED_START = 360
BALL_SPEED_STEP = 15      # added on every paddle hit
BALL_SPEED_MAX = 720
BALL_MAX_BOUNCE_ANGLE = 60  # degrees from vertical at the paddle's edge
BALL_LAUNCH_ANGLE = 20      # degrees from vertical, toward the last paddle movement
BALL_MAX_STEP = 5           # px per physics sub-step (prevents tunnelling)

# Rules
LIVES = 5
LEVEL_BANNER_TIME = 1.5   # seconds
