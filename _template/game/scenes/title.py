import pygame

import settings
from game.scene import Scene, draw_text


class TitleScene(Scene):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                from game.scenes.play import PlayScene

                self.game.switch(PlayScene(self.game))
            elif event.key == pygame.K_ESCAPE:
                self.game.quit()

    def draw(self, surface):
        surface.fill(settings.BACKGROUND)
        w, h = surface.get_size()
        draw_text(surface, settings.TITLE, 48, settings.TEXT, center=(w // 2, h // 3))
        draw_text(surface, "Press ENTER to start", 24, settings.TEXT, center=(w // 2, h // 2))
        draw_text(surface, "Esc to quit", 18, settings.MUTED, center=(w // 2, h - 30))
