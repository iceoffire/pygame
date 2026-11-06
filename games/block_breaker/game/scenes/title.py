import pygame

import settings
from game import save
from game.scene import Scene, draw_text

CONTROLS = (
    ("A / D  or  Left / Right", "move the paddle"),
    ("Mouse", "move the paddle"),
    ("Space  or  left click", "launch the ball"),
    ("P  or  Esc", "pause"),
)


class TitleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.high_score = save.high_score()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                from game.scenes.play import PlayScene

                self.game.switch(PlayScene(self.game))
            elif event.key == pygame.K_ESCAPE:
                self.game.quit()

    def draw(self, surface):
        surface.fill(settings.BACKGROUND)
        w, h = surface.get_size()
        draw_text(surface, settings.TITLE, 72, settings.TEXT, center=(w // 2, h // 4))
        draw_text(surface, f"Best: {self.high_score}", 28, settings.MUTED, center=(w // 2, h // 4 + 50))
        y = h // 2 - 20
        for keys, action in CONTROLS:
            draw_text(surface, keys, 26, settings.TEXT, center=(w // 2 - 110, y))
            draw_text(surface, action, 26, settings.MUTED, center=(w // 2 + 130, y))
            y += 32
        draw_text(surface, "Press ENTER to start", 34, settings.TEXT, center=(w // 2, h - 110))
        draw_text(surface, "Esc to quit", 22, settings.MUTED, center=(w // 2, h - 40))
