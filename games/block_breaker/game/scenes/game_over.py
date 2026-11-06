import pygame

import settings
from game import save
from game.scene import Scene, dim, draw_text


class GameOverScene(Scene):
    """Shown over the frozen play field. R / Enter retries, Esc goes to the title."""

    heading = "GAME OVER"

    def __init__(self, game, score, below=None):
        super().__init__(game)
        self.score = score
        self.below = below
        self.new_record = save.submit_score(score)
        self.high_score = save.high_score()

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_r, pygame.K_RETURN, pygame.K_KP_ENTER):
            from game.scenes.play import PlayScene

            self.game.switch(PlayScene(self.game))
        elif event.key == pygame.K_ESCAPE:
            from game.scenes.title import TitleScene

            self.game.switch(TitleScene(self.game))

    def update(self, dt):
        if self.below is not None:
            self.below.update_fx(dt)  # let particles and screen shake settle

    def draw(self, surface):
        if self.below is not None:
            self.below.draw(surface)
            dim(surface, 180)
        else:
            surface.fill(settings.BACKGROUND)
        w, h = surface.get_size()
        draw_text(surface, self.heading, 72, settings.TEXT, center=(w // 2, h // 3))
        draw_text(surface, f"Score: {self.score}", 36, settings.TEXT, center=(w // 2, h // 2))
        best = "New best score!" if self.new_record else f"Best: {self.high_score}"
        draw_text(surface, best, 28, settings.MUTED, center=(w // 2, h // 2 + 40))
        draw_text(surface, "R to retry  ·  Esc to title", 28, settings.TEXT, center=(w // 2, h - 120))


class WinScene(GameOverScene):
    heading = "YOU WIN!"
