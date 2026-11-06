import pygame

import settings
from game import assets, save
from game.scene import Scene, dim, draw_text, format_time


class WinScene(Scene):
    """Shown after the last map, with the completion time."""

    def __init__(self, game, elapsed):
        super().__init__(game)
        self.elapsed = elapsed
        self.new_record = save.submit_time(elapsed)
        self.best = save.best_time()

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) or event.key in settings.RESTART_KEYS:
            from game.scenes.play import PlayScene

            self.game.switch(PlayScene(self.game))
        elif event.key == pygame.K_ESCAPE:
            from game.scenes.title import TitleScene

            self.game.switch(TitleScene(self.game))

    def draw(self, surface):
        surface.blit(assets.scaled_to("images/background.png", surface.get_size()), (0, 0))
        dim(surface, 150)
        w, h = surface.get_size()
        draw_text(surface, "YOU WIN!", 80, settings.ACCENT, center=(w // 2, h // 3))
        draw_text(surface, f"Time  {format_time(self.elapsed)}", 40, settings.TEXT, center=(w // 2, h // 2))
        if self.new_record:
            draw_text(surface, "New best time!", 28, settings.ACCENT, center=(w // 2, h // 2 + 44))
        elif self.best is not None:
            draw_text(surface, f"Best  {format_time(self.best)}", 28, settings.MUTED, center=(w // 2, h // 2 + 44))
        draw_text(surface, "ENTER / R to play again   ·   Esc for title", 24, settings.MUTED, center=(w // 2, h - 60))
