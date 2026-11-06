"""Load-once cache for images and fonts. Paths are relative to the project's assets/ folder."""
from functools import cache
from pathlib import Path

import pygame

ASSETS = Path(__file__).resolve().parent.parent / "assets"


@cache
def image(name, alpha=True):
    """image("images/player/ship.png") -> converted Surface, loaded only once."""
    surface = pygame.image.load(ASSETS / name)
    return surface.convert_alpha() if alpha else surface.convert()


@cache
def frames(pattern, count, alpha=True):
    """frames("images/effects/explosion_{:02d}.png", 8) -> tuple of Surfaces."""
    return tuple(image(pattern.format(i), alpha) for i in range(count))


@cache
def font(size):
    """pygame-ce's bundled default font: same look on every OS."""
    return pygame.font.Font(None, size)


@cache
def tinted(name, color):
    """A copy of an image with every opaque pixel pushed toward `color` (hit flash)."""
    surface = image(name).copy()
    surface.fill(color, special_flags=pygame.BLEND_RGB_MAX)
    return surface
