"""Wave layouts. Waves 1-3 are the original hand-designed ones; later waves follow a difficulty curve."""
import random

import settings
from game.entities.enemy import Enemy

ENEMY_WIDTH = 44
MARGIN = 20
ROW_START_Y = -70  # rows start above the screen and fly in
ROW_SPACING = 80


def column_x(column, columns):
    """Spread `columns` enemies evenly between the side margins (the old layout overflowed the right edge)."""
    span = settings.SCREEN_SIZE[0] - 2 * MARGIN - ENEMY_WIDTH
    return MARGIN + span * column / max(columns - 1, 1)


def row_y(row):
    return ROW_START_Y - ROW_SPACING * row


def build_wave(number):
    """Return (enemies, seconds between enemy shots) for wave `number` (1-based)."""
    if number == 1:
        # One row, already on screen; every other ship is slower.
        enemies = [Enemy(20 + 40 * j, 40, 0, 30 if j % 2 else 60) for j in range(10)]
        return enemies, settings.WAVE_BASE_FIRE_INTERVAL

    if number == 2:
        # Three full rows, one per enemy type.
        enemies = [Enemy(20 + 40 * j, row_y(i), i, 48) for i in range(3) for j in range(10)]
        return enemies, settings.WAVE_BASE_FIRE_INTERVAL

    if number == 3:
        # Five rows alternating 10 and 5 ships.
        enemies = []
        for i in range(5):
            columns = 5 if i % 2 else 10
            enemies += [Enemy(column_x(j, columns), row_y(i), i % 3, 48) for j in range(columns)]
        return enemies, settings.WAVE_BASE_FIRE_INTERVAL

    # Wave 4+: more rows, faster ships, more fast ships and quicker enemy fire as `step` grows.
    step = number - 3
    rows = min(4 + step // 3, settings.WAVE_MAX_ROWS)
    speed = min(settings.WAVE_BASE_SPEED + settings.WAVE_SPEED_STEP * step, settings.WAVE_MAX_SPEED)
    fast_chance = min(settings.WAVE_FAST_CHANCE_STEP * step, settings.WAVE_MAX_FAST_CHANCE)
    fire_interval = max(
        settings.WAVE_BASE_FIRE_INTERVAL - settings.WAVE_FIRE_INTERVAL_STEP * step,
        settings.WAVE_MIN_FIRE_INTERVAL,
    )
    enemies = []
    for i in range(rows):
        columns = random.randint(5, 10)
        for j in range(columns):
            fast = random.random() < fast_chance
            enemy_speed = speed * settings.WAVE_FAST_MULTIPLIER if fast else speed
            enemies.append(Enemy(column_x(j, columns), row_y(i), i % 3, enemy_speed))
    return enemies, fire_interval
