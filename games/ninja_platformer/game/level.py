"""Builds a level from a map image: one pixel = one tile.

Color schema:
    black (0, 0, 0)    dirt / floor (solid)
    blue  (0, 0, 255)  player spawn
    red   (255, 0, 0)  objective (touch it to finish the map)
    anything else      empty
"""
import math
import re

import pygame

import settings
from game import assets

DIRT = (0, 0, 0)
SPAWN = (0, 0, 255)
OBJECTIVE = (255, 0, 0)

MAP_PATTERN = "images/maps/map_{}.png"
TILE_PATTERN = "images/tiles/floor_{}.png"
OBJECTIVE_IMAGE = "images/tiles/objective.png"


def map_numbers():
    """Sorted numbers of every assets/images/maps/map_<n>.png file (one entry per map)."""
    return sorted(
        int(match.group(1))
        for path in (assets.ASSETS / "images" / "maps").glob("map_*.png")
        if (match := re.fullmatch(r"map_(\d+)\.png", path.name))
    )


def floor_suffix(color, left, right, up, down):
    """Pick the floor tile from its neighbours (None = outside the map).

    Side: l/m/r = left end, middle, right end.
    Vertical: u = top surface (grass), d = dirt below another tile, f = floating.
    This is the exact selection the original game used.
    """
    if left is not None and left != color:
        side = "l"
    elif left == color and left == right:
        side = "m"
    elif left != color and right != color:
        side = "m"
    elif right != color:
        side = "r"
    else:  # left is outside the map and right is dirt
        side = "l"

    if down == color and up != color:
        vertical = "u"
    elif up == color:
        vertical = "d"
    elif down is None and up is None:
        vertical = "u"
    else:
        vertical = "f"
    return side + vertical


class Level:
    def __init__(self, number):
        self.number = number
        # Read the raw pixels: no convert(), so the colors stay exactly as drawn.
        pixels = pygame.image.load(assets.ASSETS / MAP_PATTERN.format(number))
        self.columns, self.rows = pixels.get_size()
        size = settings.TILE_SIZE
        self.width = self.columns * size
        self.height = self.rows * size

        self.tiles = []        # (image name, world position) to draw
        self.solids = {}       # (column, row) -> FRect of the solid part of that tile
        self.spawn_cell = None
        self.objective = None  # FRect
        self.objective_pos = None

        def color_at(column, row):
            if 0 <= column < self.columns and 0 <= row < self.rows:
                return tuple(pixels.get_at((column, row)))
            return None

        # Column-major like the original, so the first spawn found wins the same way.
        for column in range(self.columns):
            for row in range(self.rows):
                color = color_at(column, row)
                rgb = color[:3]
                pos = (column * size, row * size)
                if rgb == DIRT:
                    suffix = floor_suffix(
                        color,
                        color_at(column - 1, row),
                        color_at(column + 1, row),
                        color_at(column, row - 1),
                        color_at(column, row + 1),
                    )
                    name = TILE_PATTERN.format(suffix)
                    self.tiles.append((name, pos))
                    # Floating tiles are shorter (94 px); collide with what is drawn.
                    width, height = assets.image(name).get_size()
                    self.solids[(column, row)] = pygame.FRect(pos, (width, height))
                elif rgb == SPAWN and self.spawn_cell is None:
                    self.spawn_cell = (column, row)
                elif rgb == OBJECTIVE and self.objective is None:
                    self.objective_pos = pos
                    self.objective = pygame.FRect(pos, assets.image(OBJECTIVE_IMAGE).get_size())

        if self.spawn_cell is None:
            self.spawn_cell = (0, 0)

    @property
    def spawn_point(self):
        """Mid-bottom of the spawn tile: the player is placed standing there."""
        column, row = self.spawn_cell
        size = settings.TILE_SIZE
        return (column * size + size / 2, (row + 1) * size)

    def solids_near(self, rect):
        """Solid tile rects in the grid cells `rect` touches (no scan over every object)."""
        size = settings.TILE_SIZE
        first_column = max(0, math.floor(rect.left / size))
        last_column = min(self.columns - 1, math.floor(rect.right / size))
        first_row = max(0, math.floor(rect.top / size))
        last_row = min(self.rows - 1, math.floor(rect.bottom / size))
        for column in range(first_column, last_column + 1):
            for row in range(first_row, last_row + 1):
                solid = self.solids.get((column, row))
                if solid is not None:
                    yield solid

    def draw(self, surface, view, offset):
        ox, oy = offset
        size = settings.TILE_SIZE
        for name, (x, y) in self.tiles:
            if view.colliderect((x, y, size, size)):
                surface.blit(assets.image(name), (x - ox, y - oy))

    def draw_objective(self, surface, offset):
        if self.objective_pos is not None:
            x, y = self.objective_pos
            surface.blit(assets.image(OBJECTIVE_IMAGE), (x - offset[0], y - offset[1]))
