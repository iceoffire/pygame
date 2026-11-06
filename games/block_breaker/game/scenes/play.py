import pygame

import settings
from game import assets
from game.entities.ball import Ball
from game.entities.paddle import Paddle
from game.entities.particles import Particles
from game.fx import FloatingText, ScreenShake
from game.levels import LEVELS
from game.scene import Scene, draw_text
from game.scenes.game_over import GameOverScene, WinScene
from game.scenes.pause import PauseScene


class PlayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.lives = settings.LIVES
        self.score = 0
        self.level = 0  # index into LEVELS
        self.paddle = Paddle()
        self.ball = Ball()
        self.particles = Particles()
        self.texts = []
        self.shake = ScreenShake()
        self.bricks = []
        self.banner_time = 0.0
        self.start_level(0)

    # --- flow --------------------------------------------------------
    def start_level(self, index):
        self.level = index
        self.bricks = LEVELS[index]()
        self.paddle.reset()
        self.ball.reset(self.paddle)
        self.banner_time = settings.LEVEL_BANNER_TIME

    def launch(self):
        if not self.ball.launched and self.banner_time <= 0:
            self.ball.launch(self.paddle.last_direction)

    def lose_life(self):
        self.lives -= 1
        self.shake.start(strength=6, duration=0.35)
        if self.lives <= 0:
            self.game.switch(GameOverScene(self.game, self.score, below=self))
        else:
            self.ball.reset(self.paddle)

    def level_cleared(self):
        if self.level + 1 >= len(LEVELS):
            self.game.switch(WinScene(self.game, self.score, below=self))
        else:
            self.start_level(self.level + 1)

    # --- input -------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_p, pygame.K_ESCAPE):
                self.game.push(PauseScene(self.game, self))
            elif event.key == pygame.K_SPACE:
                self.launch()
        elif event.type == pygame.MOUSEMOTION:
            self.paddle.follow_mouse(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.launch()

    # --- update ------------------------------------------------------
    def update_fx(self, dt):
        self.shake.update(dt)
        self.particles.update(dt)
        for text in self.texts:
            text.update(dt)
        self.texts = [t for t in self.texts if t.alive]

    def update(self, dt):
        self.update_fx(dt)
        self.banner_time = max(0.0, self.banner_time - dt)

        keys = pygame.key.get_pressed()
        direction = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.paddle.move(direction, dt)

        if not self.ball.launched:
            self.ball.stick_to(self.paddle)
            return

        for brick, destroyed in self.ball.update(dt, self.paddle, self.bricks):
            if destroyed:
                self.score += brick.points
                self.particles.burst(brick.rect.center, brick.base_color)
                self.texts.append(FloatingText(f"+{brick.points}", brick.rect.center, brick.base_color))
            else:
                self.particles.burst(brick.rect.center, brick.color, count=4)
        self.bricks = [b for b in self.bricks if b.alive]

        if self.ball.lost:
            self.lose_life()
        elif not self.bricks:
            self.level_cleared()

    # --- draw --------------------------------------------------------
    def draw(self, surface):
        surface.fill(settings.BACKGROUND)
        offset = self.shake.offset
        for brick in self.bricks:
            brick.draw(surface, offset)
        self.paddle.draw(surface, offset)
        self.ball.draw(surface, offset)
        self.particles.draw(surface, offset)
        for text in self.texts:
            text.draw(surface, offset)
        self.draw_hud(surface)

        w, h = surface.get_size()
        if self.banner_time > 0:
            draw_text(surface, f"LEVEL {self.level + 1}", 72, settings.TEXT, center=(w // 2, h // 2 + 40))
        elif not self.ball.launched:
            draw_text(surface, "Press SPACE to launch", 32, settings.TEXT, center=(w // 2, h // 2 + 60))

    def draw_hud(self, surface):
        size = settings.HUD_FONT_SIZE
        draw_text(surface, "Lives:", size, settings.TEXT, topleft=(25, 9))
        for i in range(self.lives):
            center = (settings.HUD_LIVES_X + settings.HUD_LIVES_SPACING * i, 20)
            ring = max(100, int(255 / 10 * i))
            pygame.draw.circle(surface, settings.TEXT, center, settings.HUD_LIVES_RADIUS)
            pygame.draw.circle(surface, (ring, int(100 / 5 * i), int(250 / 5 * i)), center,
                               settings.HUD_LIVES_RADIUS, 2)
        w = surface.get_width()
        draw_text(surface, f"Level {self.level + 1}", size, settings.MUTED, center=(w // 2, 20))
        score = assets.font(size).render(f"Score: {self.score}", True, settings.TEXT)
        surface.blit(score, score.get_rect(topright=(w - 20, 9)))
