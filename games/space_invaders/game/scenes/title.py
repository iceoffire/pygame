import math

import pygame

import settings
from game import assets, save
from game.entities.background import Background
from game.scene import Scene, dim, draw_text

CONTROLS = (
    ("A / D  or  Left / Right", "move"),
    ("Space", "shoot (hold for auto-fire)"),
    ("P  or  Esc", "pause"),
)


class TitleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.background = Background()
        self.best = save.high_score()
        self.time = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                from game.scenes.play import PlayScene

                self.game.switch(PlayScene(self.game))
            elif event.key == pygame.K_ESCAPE:
                self.game.quit()

    def update(self, dt):
        self.time += dt
        # No player here, so drift the parallax slowly from side to side.
        self.background.update(dt, 205 + 180 * math.sin(self.time * 0.4))

    def draw(self, surface):
        self.background.draw(surface)
        dim(surface, 120)
        w, h = surface.get_size()
        draw_text(surface, settings.TITLE.upper(), 48, settings.ACCENT, center=(w // 2, 60))
        if self.best:
            draw_text(surface, f"Best {self.best}", 20, settings.MUTED, center=(w // 2, 92))

        # Two columns: keys right-aligned, actions left-aligned, meeting at the center.
        font = assets.font(18)
        y = 128
        for keys, action in CONTROLS:
            key_text = font.render(keys, True, settings.TEXT)
            surface.blit(key_text, key_text.get_rect(topright=(w // 2 - 8, y)))
            surface.blit(font.render(action, True, settings.MUTED), (w // 2 + 8, y))
            y += 24

        if int(self.time * 2) % 2 == 0:
            draw_text(surface, "Press ENTER to start", 26, settings.TEXT, center=(w // 2, h - 70))
        draw_text(surface, "Esc to quit", 18, settings.MUTED, center=(w // 2, h - 30))
