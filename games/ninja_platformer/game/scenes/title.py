import pygame

import settings
from game import assets, save
from game.scene import Scene, dim, draw_text, format_time

CONTROLS = (
    ("A / D  or  Left / Right", "run"),
    ("Space / W / Up", "jump (hold for higher)"),
    ("P / Esc", "pause"),
    ("R", "restart map"),
)


class TitleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.best = save.best_time()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                from game.scenes.play import PlayScene

                self.game.switch(PlayScene(self.game))
            elif event.key == pygame.K_ESCAPE:
                self.game.quit()

    def draw(self, surface):
        surface.blit(assets.scaled_to("images/background.png", surface.get_size()), (0, 0))
        dim(surface, 150)
        w, h = surface.get_size()
        draw_text(surface, settings.TITLE, 72, settings.TEXT, center=(w // 2, 110))
        draw_text(surface, "Reach the objective on every map", 24, settings.MUTED, center=(w // 2, 160))

        y = 230
        for keys, action in CONTROLS:
            draw_text(surface, keys, 26, settings.ACCENT, center=(w // 2 - 110, y))
            draw_text(surface, action, 26, settings.TEXT, center=(w // 2 + 130, y))
            y += 34

        if self.best is not None:
            draw_text(surface, f"Best time  {format_time(self.best)}", 26, settings.TEXT, center=(w // 2, y + 20))
        draw_text(surface, "Press ENTER to start", 32, settings.TEXT, center=(w // 2, h - 80))
        draw_text(surface, "Esc to quit", 20, settings.MUTED, center=(w // 2, h - 40))
