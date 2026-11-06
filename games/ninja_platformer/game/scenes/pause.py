import pygame

import settings
from game.scene import Scene, dim, draw_text


class PauseScene(Scene):
    """Pushed on top of the play scene; draws it frozen underneath."""

    def __init__(self, game, below):
        super().__init__(game)
        self.below = below

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in settings.PAUSE_KEYS or event.key == pygame.K_RETURN:
            self.game.pop()
        elif event.key in settings.RESTART_KEYS:
            self.game.pop()
            self.below.fade_then(self.below.respawn)
        elif event.key == pygame.K_q:
            from game.scenes.title import TitleScene

            self.game.switch(TitleScene(self.game))

    def draw(self, surface):
        self.below.draw(surface)
        dim(surface)
        w, h = surface.get_size()
        draw_text(surface, "PAUSED", 64, settings.TEXT, center=(w // 2, h // 2 - 30))
        draw_text(surface, "P / Esc to resume   ·   R to restart map   ·   Q to quit to title",
                  22, settings.MUTED, center=(w // 2, h // 2 + 24))
