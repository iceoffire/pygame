import pygame

import settings
from game import assets
from game.camera import Camera
from game.entities.player import Player
from game.level import Level, map_numbers
from game.scene import Scene, dim, draw_text, format_time


def draw_shadowed(surface, text, size, color, **where):
    """HUD text with a 2 px drop shadow so it reads on any background."""
    rect = draw_text(surface, text, size, settings.SHADOW, **{k: (v[0] + 2, v[1] + 2) for k, v in where.items()})
    draw_text(surface, text, size, color, **where)
    return rect


class PlayScene(Scene):
    def __init__(self, game, map_index=0, elapsed=0.0):
        super().__init__(game)
        self.maps = map_numbers()
        self.elapsed = elapsed     # total run time, carried across maps
        self.fade = 1.0            # 0 = clear, 1 = black; starts black and fades in
        self.pending = None        # action to run once the screen is fully black
        self.load_map(map_index)

    # --- level flow -----------------------------------------------------
    def load_map(self, map_index):
        self.map_index = map_index
        self.level = Level(self.maps[map_index])
        self.player = Player(self.level.spawn_point)
        self.camera = Camera(settings.SCREEN_SIZE, (self.level.width, self.level.height))
        self.camera.snap(self.player.rect.center)
        self.banner_time = settings.BANNER_TIME

    def respawn(self):
        self.player.reset(self.level.spawn_point)
        self.camera.snap(self.player.rect.center)

    def next_map(self):
        if self.map_index + 1 < len(self.maps):
            self.load_map(self.map_index + 1)
        else:
            from game.scenes.win import WinScene

            self.game.switch(WinScene(self.game, self.elapsed))

    def fade_then(self, action):
        if self.pending is None:
            self.pending = action

    # --- scene ----------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in settings.PAUSE_KEYS:
                from game.scenes.pause import PauseScene

                self.game.push(PauseScene(self.game, self))
            elif event.key in settings.RESTART_KEYS:
                self.fade_then(self.respawn)
            elif event.key in settings.JUMP_KEYS:
                self.player.press_jump()
        elif event.type == pygame.KEYUP and event.key in settings.JUMP_KEYS:
            self.player.release_jump()

    def update(self, dt):
        self.elapsed += dt
        self.banner_time = max(0.0, self.banner_time - dt)

        if self.pending is not None:
            # Fading out: the world is frozen until the screen is black.
            self.fade = min(1.0, self.fade + dt / settings.FADE_TIME)
            if self.fade >= 1.0:
                action, self.pending = self.pending, None
                action()
            return
        self.fade = max(0.0, self.fade - dt / settings.FADE_TIME)

        keys = pygame.key.get_pressed()
        direction = any(keys[k] for k in settings.RIGHT_KEYS) - any(keys[k] for k in settings.LEFT_KEYS)
        self.player.update(dt, direction, self.level)

        look_ahead = settings.CAMERA_LOOK_AHEAD * self.player.velocity.x / settings.MAX_RUN_SPEED
        self.camera.follow(self.player.rect.center, look_ahead, dt)

        if self.player.rect.top > self.level.height:
            self.fade_then(self.respawn)  # fell off the map
        elif self.level.objective and self.player.rect.colliderect(self.level.objective):
            self.fade_then(self.next_map)

    def draw(self, surface):
        surface.blit(assets.scaled_to("images/background.png", surface.get_size()), (0, 0))
        offset = self.camera.offset
        self.level.draw(surface, self.camera.view, offset)
        self.player.draw(surface, offset)
        self.level.draw_objective(surface, offset)
        self.draw_hud(surface)
        if self.fade > 0:
            dim(surface, int(255 * self.fade))

    def draw_hud(self, surface):
        w, _ = surface.get_size()
        draw_shadowed(surface, f"Map {self.map_index + 1}/{len(self.maps)}", 32, settings.TEXT, topleft=(16, 14))
        time_text = format_time(self.elapsed)
        width = assets.font(32).size(time_text)[0]
        draw_shadowed(surface, time_text, 32, settings.TEXT, topleft=(w - 16 - width, 14))
        if self.banner_time > 0:
            draw_shadowed(surface, f"MAP {self.map_index + 1}", 64, settings.ACCENT, center=(w // 2, 120))
