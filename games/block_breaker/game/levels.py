"""Brick layouts. Each level function returns a fresh list of Brick objects."""
import settings
from game.entities.brick import Brick


def _rect(row, column):
    return (
        settings.BRICK_LEFT + settings.BRICK_WIDTH * column,
        settings.BRICK_TOP + settings.BRICK_HEIGHT * row,
        settings.BRICK_WIDTH,
        settings.BRICK_HEIGHT,
    )


def _gradient(row, column):
    """The original game's look: every 4th row is red-ish, the rest green-ish."""
    if row % 4 == 0:
        return (250, int(230 / 12 * row), int(100 / 8 * column)), 100
    return (int(230 / 12 * row), 250, int(100 / 8 * column)), 80


def level_1():
    """The original full 12 x 15 grid."""
    bricks = []
    for row in range(12):
        for column in range(settings.BRICK_COLUMNS):
            color, score = _gradient(row, column)
            bricks.append(Brick(_rect(row, column), color, score))
    return bricks


def level_2():
    """The original second layout: a gap in columns 10-12."""
    bricks = []
    for row in range(12):
        for column in range(settings.BRICK_COLUMNS):
            if 10 <= column <= 12:
                continue
            color, score = _gradient(row, column)
            bricks.append(Brick(_rect(row, column), color, score))
    return bricks


def level_3():
    """Armored top rows (3 and 2 HP) over a checkerboard of single-hit bricks."""
    bricks = []
    for row in range(10):
        for column in range(settings.BRICK_COLUMNS):
            if row < 2:
                hp = 3
            elif row < 5:
                hp = 2
            else:
                hp = 1
                if (row + column) % 2 == 0:
                    continue
            color, score = _gradient(row, column)
            bricks.append(Brick(_rect(row, column), color, score, hp))
    return bricks


LEVELS = (level_1, level_2, level_3)
