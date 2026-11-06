import pygame

import settings
from game.scene import Scene, dim, draw_text


class FrozenOverlay(Scene):
    """Base for screens drawn over a frozen copy of the scene below (pause, game over)."""

    def __init__(self, game, below):
        super().__init__(game)
        self.below = below
        self.snapshot = None

    def draw_below(self, surface):
        # Capture the scene once, so screen shake or blinking doesn't keep moving underneath.
        if self.snapshot is None:
            self.below.draw(surface)
            self.snapshot = surface.copy()
        else:
            surface.blit(self.snapshot, (0, 0))
        dim(surface)


class PauseScene(FrozenOverlay):
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in settings.PAUSE_KEYS or event.key == pygame.K_RETURN:
            self.game.pop()
        elif event.key == pygame.K_q:
            from game.scenes.title import TitleScene

            self.game.switch(TitleScene(self.game))

    def draw(self, surface):
        self.draw_below(surface)
        w, h = surface.get_size()
        draw_text(surface, "PAUSED", 48, settings.TEXT, center=(w // 2, h // 2 - 20))
        draw_text(surface, "P / Esc to resume   -   Q to quit to title", 20, settings.MUTED, center=(w // 2, h // 2 + 24))
