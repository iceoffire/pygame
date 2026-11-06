import pygame

import settings
from game.scene import Scene, dim, draw_text


class PlayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.player = pygame.FRect(0, 0, 24, 24)
        self.player.center = (settings.SCREEN_SIZE[0] / 2, settings.SCREEN_SIZE[1] / 2)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
            self.game.push(PauseScene(self.game, self))

    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a]),
            (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w]),
        )
        if direction:
            self.player.move_ip(direction.normalize() * settings.PLAYER_SPEED * dt)
        self.player.clamp_ip(self.game.screen.get_rect())

    def draw(self, surface):
        surface.fill(settings.BACKGROUND)
        pygame.draw.rect(surface, settings.TEXT, self.player)


class PauseScene(Scene):
    """Pushed on top of a scene; draws it frozen underneath."""

    def __init__(self, game, below):
        super().__init__(game)
        self.below = below

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_p, pygame.K_ESCAPE, pygame.K_RETURN):
                self.game.pop()
            elif event.key == pygame.K_q:
                from game.scenes.title import TitleScene

                self.game.switch(TitleScene(self.game))

    def draw(self, surface):
        self.below.draw(surface)
        dim(surface)
        w, h = surface.get_size()
        draw_text(surface, "PAUSED", 48, settings.TEXT, center=(w // 2, h // 2 - 20))
        draw_text(surface, "P to resume  ·  Q to quit to title", 20, settings.MUTED, center=(w // 2, h // 2 + 24))
