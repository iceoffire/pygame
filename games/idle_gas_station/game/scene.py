"""Base class for every screen of the game (title, play, pause, game over...)."""
import pygame

from game import assets


class Scene:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def on_exit(self):
        """Called when the scene leaves the stack or the game closes."""
        pass


def draw_text(surface, text, size, color, center=None, topleft=None, font=None):
    rendered = (font or assets.font(size)).render(text, True, color)
    rect = rendered.get_rect()
    if center is not None:
        rect.center = center
    elif topleft is not None:
        rect.topleft = topleft
    surface.blit(rendered, rect)
    return rect


def dim(surface, alpha=160):
    """Darken whatever is already on screen (used by pause and game-over overlays)."""
    shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    shade.fill((0, 0, 0, alpha))
    surface.blit(shade, (0, 0))
