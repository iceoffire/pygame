"""Axis-separated AABB movement against the level's tile grid."""
import math
from dataclasses import dataclass

# Never move more than this per sub-step, so fast falls can't tunnel through a tile.
MAX_STEP = 16
# Overlaps smaller than this count as touching, not colliding (float safety).
EPSILON = 1e-6


@dataclass
class Hits:
    wall: bool = False      # hit something while moving sideways
    floor: bool = False     # landed on something
    ceiling: bool = False   # bumped the head


def overlaps(a, b):
    return (
        a.right - b.left > EPSILON
        and b.right - a.left > EPSILON
        and a.bottom - b.top > EPSILON
        and b.bottom - a.top > EPSILON
    )


def move_and_collide(rect, dx, dy, level):
    """Move `rect` (an FRect, in place) by (dx, dy), stopping at solid tiles.

    X is resolved before Y on every sub-step. Since the rect never ends a step
    inside a tile, it can't get stuck in a wall: it only ever gets pushed back to
    the edge it came from (left/right edge for X, top/bottom edge for Y).
    """
    hits = Hits()
    steps = max(1, math.ceil(max(abs(dx), abs(dy)) / MAX_STEP))
    step_x, step_y = dx / steps, dy / steps
    for _ in range(steps):
        if step_x:
            rect.x += step_x
            blocking = [s for s in level.solids_near(rect) if overlaps(rect, s)]
            if blocking:
                if step_x > 0:
                    rect.right = min(s.left for s in blocking)
                else:
                    rect.left = max(s.right for s in blocking)
                hits.wall = True
                step_x = 0
        if step_y:
            rect.y += step_y
            blocking = [s for s in level.solids_near(rect) if overlaps(rect, s)]
            if blocking:
                if step_y > 0:
                    rect.bottom = min(s.top for s in blocking)  # land exactly on the tile top
                    hits.floor = True
                else:
                    rect.top = max(s.bottom for s in blocking)  # head bump
                    hits.ceiling = True
                step_y = 0
        if not step_x and not step_y:
            break
    return hits
