import pygame

TITLE = "Space Invaders"
SCREEN_SIZE = (450, 333)
FPS = 60

# Colors
TEXT = (235, 235, 245)
MUTED = (150, 155, 180)
ACCENT = (255, 210, 90)
DANGER = (255, 100, 100)

# Key bindings
LEFT_KEYS = (pygame.K_a, pygame.K_LEFT)
RIGHT_KEYS = (pygame.K_d, pygame.K_RIGHT)
FIRE_KEYS = (pygame.K_SPACE,)
PAUSE_KEYS = (pygame.K_p, pygame.K_ESCAPE)

# Player (speeds in pixels per second; the old game ran at 60 FPS with per-frame speeds)
PLAYER_START = (200, 280)
PLAYER_MAX_HP = 4  # one ship sprite per HP level: ship_hp1..4
PLAYER_ACCELERATION = 5040  # 1.4 px/frame per frame
PLAYER_MAX_SPEED = 300  # 5 px/frame
PLAYER_FRICTION = 1 / 1.1  # velocity multiplier per 1/60 s while no key is held
PLAYER_FIRE_COOLDOWN = 0.24
PLAYER_INVULNERABLE_TIME = 1.0
PLAYER_BLINK_INTERVAL = 0.08
PLAYER_HITBOX_SHRINK = (10, 8)  # the sprite has transparent margins

# Bullets
PLAYER_BULLET_SPEED = 240
ENEMY_BULLET_SPEED = 240

# Enemies: index = enemy type (0, 1, 2). HP is type + 2.
ENEMY_SCORES = (10, 20, 30)
ENEMY_HIT_FLASH_TIME = 0.1
ENEMY_HIT_FLASH_COLORS = ((255, 255, 255), (255, 130, 130))

# Waves 1-3 are hand-designed (see game/waves.py); after that the curve below applies.
WAVE_BANNER_TIME = 1.5
WAVE_BASE_FIRE_INTERVAL = 0.5  # seconds between enemy shots
WAVE_MIN_FIRE_INTERVAL = 0.22
WAVE_FIRE_INTERVAL_STEP = 0.025
WAVE_BASE_SPEED = 48
WAVE_SPEED_STEP = 6
WAVE_MAX_SPEED = 110
WAVE_FAST_MULTIPLIER = 1.6
WAVE_FAST_CHANCE_STEP = 0.08
WAVE_MAX_FAST_CHANCE = 0.4
WAVE_MAX_ROWS = 7

# Animation timing (seconds per frame)
BACKGROUND_FRAMES = 200
BACKGROUND_FRAME_TIME = 0.02
BACKGROUND_PARALLAX = 25 / 225  # background shift per pixel of player x
THRUSTER_FRAME_TIME = 0.02
EXPLOSION_FRAME_TIME = 1 / 60
MUZZLE_FLASH_FRAME_TIME = 1 / 60

# Flow
DEATH_DELAY = 1.2  # seconds between the last life lost and the game over screen

# HUD
LIVES_PANEL_POS = (20, 300)
