"""Load-once cache for images and fonts. Paths are relative to the project's assets/ folder."""
from functools import cache
from pathlib import Path

import pygame

ASSETS = Path(__file__).resolve().parent.parent / "assets"


@cache
def image(name, alpha=True):
    """image("images/<name>.png") -> converted Surface, loaded only once."""
    surface = pygame.image.load(ASSETS / name)
    return surface.convert_alpha() if alpha else surface.convert()


@cache
def frames(pattern, count, alpha=True):
    """frames("images/<name>_{:02d}.png", count) -> tuple of Surfaces."""
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


@cache
def scaled(name, size, smooth=True):
    """An image resized to `size`, cached. Use smooth=False for pixel art (keeps hard edges)."""
    resize = pygame.transform.smoothscale if smooth else pygame.transform.scale
    return resize(image(name), size)


@cache
def fitted(name, box, smooth=True):
    """An image scaled to fit inside `box` (width, height) without changing its aspect ratio."""
    surface = image(name)
    factor = min(box[0] / surface.get_width(), box[1] / surface.get_height())
    size = (max(1, round(surface.get_width() * factor)), max(1, round(surface.get_height() * factor)))
    return scaled(name, size, smooth)
