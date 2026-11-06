import random

import pygame

import settings
from game import assets, save
from game.entities.background import Background
from game.entities.bullet import ENEMY_BULLET, PLAYER_BULLET, Bullet
from game.entities.effects import Explosion, MuzzleFlash
from game.entities.player import Player
from game.fx import FloatingText, ScreenShake
from game.scene import Scene, draw_text
from game.waves import build_wave


def any_pressed(keys, bindings):
    return any(keys[key] for key in bindings)


class PlayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.width, self.height = settings.SCREEN_SIZE
        # The world is drawn here first, then blitted with the screen-shake offset.
        self.canvas = pygame.Surface(settings.SCREEN_SIZE).convert()
        self.background = Background()
        self.player = Player()
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.flashes = []
        self.explosions = []
        self.texts = []
        self.shake = ScreenShake()

        self.score = 0
        self.best = save.high_score()
        self.new_record = False

        self.wave = 0
        self.wave_active = False
        self.banner_time = 0.0
        self.enemy_fire_interval = settings.WAVE_BASE_FIRE_INTERVAL
        self.enemy_fire_timer = 0.0
        self.death_timer = 0.0

        self.lives_panel = assets.image("images/hud/lives_panel.png")
        self.life_icon = assets.image("images/hud/life.png")
        self.next_wave()

    # --- input -------------------------------------------------------
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in settings.PAUSE_KEYS and self.player.alive:
            from game.scenes.pause import PauseScene

            self.game.push(PauseScene(self.game, self))
        elif event.key in settings.FIRE_KEYS:
            self.try_fire()  # a tap fires immediately; holding the key auto-fires in update()

    # --- waves -------------------------------------------------------
    def next_wave(self):
        self.wave += 1
        self.wave_active = False
        self.banner_time = settings.WAVE_BANNER_TIME

    def start_wave(self):
        self.enemies, self.enemy_fire_interval = build_wave(self.wave)
        self.enemy_fire_timer = self.enemy_fire_interval
        self.wave_active = True

    # --- actions -----------------------------------------------------
    def try_fire(self):
        if not self.player.can_fire:
            return
        self.player.cooldown = settings.PLAYER_FIRE_COOLDOWN
        x, y = self.player.rect.topleft
        for gun_x in (0, 24):
            self.player_bullets.append(Bullet(PLAYER_BULLET, (x + gun_x, y + 3), -settings.PLAYER_BULLET_SPEED))
        for flash_x in (0, 22):
            self.flashes.append(MuzzleFlash(self.player, (flash_x, -14), from_player=True))

    def enemy_fire(self):
        shooters = [enemy for enemy in self.enemies if enemy.on_screen]
        if not shooters:
            return
        enemy = random.choice(shooters)
        bullet = Bullet(ENEMY_BULLET, (0, 0), settings.ENEMY_BULLET_SPEED)
        bullet.rect.midtop = enemy.rect.midbottom
        self.enemy_bullets.append(bullet)
        flash_offset = (enemy.rect.width / 2 - 9, enemy.rect.height)
        self.flashes.append(MuzzleFlash(enemy, flash_offset, from_player=False))

    def damage_player(self):
        """Every way of losing a life goes through here, so the invulnerability window applies to all."""
        if not self.player.hit():
            return
        self.shake.start(strength=5, duration=0.35)
        if not self.player.alive:
            self.on_player_death()

    def on_player_death(self):
        center = self.player.rect.center
        for dx, dy in ((0, 0), (-12, 6), (12, -6)):
            self.explosions.append(Explosion((center[0] + dx, center[1] + dy)))
        self.shake.start(strength=8, duration=0.6)
        self.death_timer = settings.DEATH_DELAY
        self.new_record = save.submit_score(self.score)
        self.best = max(self.best, self.score)

    def kill_enemy(self, enemy, award=True):
        enemy.hp = 0
        self.explosions.append(Explosion(enemy.rect.center))
        if award:
            self.score += enemy.score
            self.best = max(self.best, self.score)
            self.texts.append(FloatingText(f"+{enemy.score}", enemy.rect.center, settings.ACCENT, size=18))
        self.shake.start(strength=2, duration=0.12)

    # --- update ------------------------------------------------------
    def update(self, dt):
        self.shake.update(dt)
        self.background.update(dt, self.player.rect.x)

        if self.player.alive:
            keys = pygame.key.get_pressed()
            direction = any_pressed(keys, settings.RIGHT_KEYS) - any_pressed(keys, settings.LEFT_KEYS)
            self.player.update(dt, direction, self.width)
            if any_pressed(keys, settings.FIRE_KEYS):
                self.try_fire()

        self.update_wave(dt)

        for enemy in self.enemies:
            enemy.update(dt)
        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.update(dt, self.height)
        for effect in self.flashes + self.explosions + self.texts:
            effect.update(dt)

        self.check_collisions()

        # Rebuild the lists instead of removing items while looping over them.
        self.enemies = [e for e in self.enemies if e.alive]
        self.player_bullets = [b for b in self.player_bullets if b.alive]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.alive]
        self.flashes = [f for f in self.flashes if f.alive]
        self.explosions = [e for e in self.explosions if e.alive]
        self.texts = [t for t in self.texts if t.alive]

        if not self.player.alive:
            self.death_timer -= dt
            if self.death_timer <= 0:
                from game.scenes.game_over import GameOverScene

                self.shake.stop()
                self.game.switch(GameOverScene(self.game, self))

    def update_wave(self, dt):
        if not self.wave_active:
            self.banner_time -= dt
            if self.banner_time <= 0:
                self.start_wave()
            return
        if not self.enemies:
            self.next_wave()
            return
        if self.player.alive:
            self.enemy_fire_timer -= dt
            if self.enemy_fire_timer <= 0:
                self.enemy_fire_timer += self.enemy_fire_interval
                self.enemy_fire()

    def check_collisions(self):
        # Player bullets vs enemies: each bullet hits at most one enemy.
        for bullet in self.player_bullets:
            for enemy in self.enemies:
                if enemy.alive and bullet.rect.colliderect(enemy.rect):
                    bullet.alive = False
                    self.explosions.append(Explosion(bullet.rect.center))
                    enemy.take_damage()
                    if not enemy.alive:
                        self.kill_enemy(enemy)
                    break

        if not self.player.alive:
            return
        hitbox = self.player.hitbox

        # Enemy bullets vs player. A bullet is absorbed even during invulnerability.
        for bullet in self.enemy_bullets:
            if bullet.rect.colliderect(hitbox):
                bullet.alive = False
                self.explosions.append(Explosion(bullet.rect.center))
                self.damage_player()

        for enemy in self.enemies:
            if not enemy.alive:
                continue
            # Ramming the player destroys the enemy (no score) and costs a life.
            if self.player.invulnerable <= 0 and enemy.rect.colliderect(hitbox):
                self.kill_enemy(enemy, award=False)
                self.damage_player()
            # An enemy slipping past the bottom edge costs a life.
            elif enemy.rect.top > self.height:
                enemy.hp = 0
                self.damage_player()

    # --- draw --------------------------------------------------------
    def draw(self, surface):
        canvas = self.canvas
        self.background.draw(canvas)
        for enemy in self.enemies:
            enemy.draw(canvas)
        for flash in self.flashes:
            flash.draw(canvas)
        self.player.draw(canvas)
        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.draw(canvas)
        for explosion in self.explosions:
            explosion.draw(canvas)
        for text in self.texts:
            text.draw(canvas)

        surface.fill((0, 0, 0))
        surface.blit(canvas, self.shake.offset)
        self.draw_hud(surface)

    def draw_hud(self, surface):
        panel_x, panel_y = settings.LIVES_PANEL_POS
        surface.blit(self.lives_panel, (panel_x, panel_y))
        # The ship on screen is the current life; the icons are the spares.
        for i in range(max(0, self.player.hp - 1)):
            surface.blit(self.life_icon, (panel_x + 5 + 22 * i, panel_y + 5))

        draw_text(surface, f"SCORE {self.score}", 20, settings.TEXT, topleft=(8, 6))
        best = assets.font(20).render(f"BEST {self.best}", True, settings.MUTED)
        surface.blit(best, best.get_rect(topright=(self.width - 8, 6)))
        draw_text(surface, f"WAVE {self.wave}", 20, settings.MUTED, center=(self.width // 2, 14))

        if not self.wave_active and self.banner_time > 0:
            # Fade the banner in and out over its lifetime.
            progress = 1 - self.banner_time / settings.WAVE_BANNER_TIME
            alpha = int(255 * min(1.0, progress * 4, (1 - progress) * 4))
            banner = assets.font(48).render(f"WAVE {self.wave}", True, settings.ACCENT)
            banner.set_alpha(max(0, alpha))
            surface.blit(banner, banner.get_rect(center=(self.width // 2, self.height // 2 - 20)))
