import pygame

import settings
from game import format as fmt
from game import save
from game.economy import Economy
from game.scene import Scene, draw_text
from game.ui import flag_image


class TitleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        data = save.load()
        self.saved_money = Economy.from_save(data).money if data else None

    def start(self):
        from game.scenes.play import PlayScene

        self.game.switch(PlayScene(self.game))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.start()
            elif event.key == pygame.K_ESCAPE:
                self.game.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.start()

    def draw(self, surface):
        surface.fill(settings.BACKGROUND)
        w, h = surface.get_size()
        flag = flag_image()
        surface.blit(flag, flag.get_rect(center=(w // 2, 150)))
        draw_text(surface, settings.TITLE, 46, settings.DARK_TEXT, center=(w // 2 + 2, 282))
        draw_text(surface, settings.TITLE, 46, settings.TEXT, center=(w // 2, 280))
        draw_text(surface, "Click the flag to earn money", 24, settings.DARK_TEXT, center=(w // 2, 350))
        draw_text(surface, "Buy upgrades for idle income", 22, settings.MUTED, center=(w // 2, 380))
        draw_text(surface, "Bigger Bills raise each click", 22, settings.MUTED, center=(w // 2, 404))
        if self.saved_money is not None:
            draw_text(surface, f"Saved progress: {fmt.money(self.saved_money)}", 22, settings.INCOME, center=(w // 2, 450))
        draw_text(surface, "Click or press ENTER to start", 26, settings.TEXT, center=(w // 2, 510))
        draw_text(surface, "Space: click flag   Wheel/Up/Down: scroll", 18, settings.MUTED, center=(w // 2, h - 70))
        draw_text(surface, "1-6: buy upgrade   P/Esc: pause", 18, settings.MUTED, center=(w // 2, h - 50))
        draw_text(surface, "Progress saves automatically", 18, settings.MUTED, center=(w // 2, h - 30))
