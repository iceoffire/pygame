import pygame

import settings
from game.scene import draw_text
from game.scenes.pause import FrozenOverlay


class GameOverScene(FrozenOverlay):
    def __init__(self, game, play_scene):
        super().__init__(game, play_scene)
        self.score = play_scene.score
        self.best = play_scene.best
        self.wave = play_scene.wave
        self.new_record = play_scene.new_record
        self.time = 0.0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_r, pygame.K_RETURN):
            from game.scenes.play import PlayScene

            self.game.switch(PlayScene(self.game))
        elif event.key == pygame.K_ESCAPE:
            from game.scenes.title import TitleScene

            self.game.switch(TitleScene(self.game))

    def update(self, dt):
        self.time += dt

    def draw(self, surface):
        self.draw_below(surface)
        w, h = surface.get_size()
        draw_text(surface, "GAME OVER", 52, settings.DANGER, center=(w // 2, h // 2 - 70))
        draw_text(surface, f"Score {self.score}", 28, settings.TEXT, center=(w // 2, h // 2 - 22))
        draw_text(surface, f"Best {self.best}", 22, settings.MUTED, center=(w // 2, h // 2 + 6))
        draw_text(surface, f"Reached wave {self.wave}", 20, settings.MUTED, center=(w // 2, h // 2 + 30))
        if self.new_record and int(self.time * 3) % 2 == 0:
            draw_text(surface, "NEW RECORD!", 26, settings.ACCENT, center=(w // 2, h // 2 + 60))
        draw_text(surface, "R to retry   -   Esc to title", 20, settings.TEXT, center=(w // 2, h - 30))
