import pygame

import settings
from game.scene import Scene, dim, draw_text


class PauseScene(Scene):
    """Pushed on top of the play scene; draws it frozen underneath."""

    def __init__(self, game, below):
        super().__init__(game)
        self.below = below

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_p, pygame.K_ESCAPE, pygame.K_RETURN):
                self.game.pop()
            elif event.key == pygame.K_q:
                from game.scenes.title import TitleScene

                self.game.switch(TitleScene(self.game))

    def draw(self, surface):
        self.below.draw(surface)
        dim(surface)
        w, h = surface.get_size()
        draw_text(surface, "PAUSED", 64, settings.TEXT, center=(w // 2, h // 2 - 20))
        draw_text(surface, "P / Esc to resume  ·  Q to quit to title", 26, settings.MUTED,
                  center=(w // 2, h // 2 + 30))
