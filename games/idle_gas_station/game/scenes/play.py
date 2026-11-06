import random
import time

import pygame

import settings
from game import assets, save
from game import format as fmt
from game.economy import UPGRADES, Economy, offline_earnings
from game.fx import FloatingText
from game.scene import Scene, dim, draw_text
from game.ui import FLAG, UpgradeList, bill_image, flag_image

OFFLINE_CAP_SECONDS = settings.OFFLINE_CAP_HOURS * 3600
BUY_KEYS = {pygame.K_1 + i: i for i in range(min(9, len(UPGRADES)))}


class Bill:
    """A banknote tossed from the click point: falls with gravity and spins."""

    def __init__(self, value, pos):
        self.image = bill_image(value)
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(random.uniform(-settings.BILL_DRIFT, settings.BILL_DRIFT), -120)
        self.angle = 0.0
        self.spin = random.uniform(-settings.BILL_SPIN, settings.BILL_SPIN)

    def update(self, dt):
        self.velocity.y += settings.BILL_GRAVITY * dt
        self.pos += self.velocity * dt
        self.angle += self.spin * dt

    def off_screen(self, height):
        return self.pos.y - settings.BILL_SIZE[0] > height

    def draw(self, surface):
        rotated = pygame.transform.rotate(self.image, self.angle)
        surface.blit(rotated, rotated.get_rect(center=(round(self.pos.x), round(self.pos.y))))


class PlayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        data = save.load()
        self.economy = Economy.from_save(data)
        self.flag_rect = pygame.Rect(settings.FLAG_POS, settings.FLAG_SIZE)
        self.upgrades = UpgradeList()
        self.bills = []
        self.texts = []
        self.pulse = 0.0
        self.autosave_timer = settings.AUTOSAVE_INTERVAL
        self.hovered = None
        self.away_message = None
        self.away_timer = 0.0
        self._apply_offline_earnings(data.get("timestamp"))

    # --- saving ----------------------------------------------------------
    def _apply_offline_earnings(self, last_timestamp):
        try:
            last_timestamp = float(last_timestamp or 0)
        except (TypeError, ValueError):
            last_timestamp = 0.0
        earned, seconds = offline_earnings(self.economy.idle_income, last_timestamp, time.time(), OFFLINE_CAP_SECONDS)
        if earned >= 1:
            self.economy.money += earned
            capped = f" (max {settings.OFFLINE_CAP_HOURS}h)" if seconds >= OFFLINE_CAP_SECONDS else ""
            self.away_message = (
                f"While you were away: +{fmt.money(earned)}",
                f"{fmt.duration(seconds)} offline{capped}",
            )
            self.away_timer = settings.AWAY_MESSAGE_TIME
        self.save()

    def save(self):
        save.store(self.economy.to_save())

    def on_exit(self):
        self.save()

    # --- input -----------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.click_at(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            self.upgrades.scroll_by(-event.y * settings.SCROLL_STEP)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.click_flag(self.flag_rect.center)  # keyboard click on the flag
            elif event.key in (pygame.K_p, pygame.K_ESCAPE):
                self.game.push(PauseScene(self.game, self))
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.upgrades.scroll_by(-settings.SCROLL_STEP)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.upgrades.scroll_by(settings.SCROLL_STEP)
            elif event.key in BUY_KEYS:
                self.buy(BUY_KEYS[event.key])

    def click_at(self, pos):
        if self.flag_rect.collidepoint(pos):
            self.click_flag(pos)
            return
        index = self.upgrades.hit(pos)
        if index is not None:
            self.buy(index)

    def click_flag(self, pos):
        value = self.economy.click()
        self.bills.append(Bill(value, pos))
        self.texts.append(FloatingText(f"+{fmt.money(value)}", (pos[0], pos[1] - 20), settings.FLOAT_TEXT, 26))
        self.pulse = settings.FLAG_PULSE_TIME

    def buy(self, index):
        upgrade = UPGRADES[index]
        if self.economy.try_buy(upgrade):
            card = self.upgrades.card_rect(index)
            if self.upgrades.rect.colliderect(card):
                self.texts.append(
                    FloatingText(f"Lv {self.economy.level(upgrade)}", (card.right - 30, card.y + 10), settings.MAXED, 20)
                )

    # --- update ----------------------------------------------------------
    def update(self, dt):
        self.economy.add_idle_income(dt)

        height = self.game.screen.get_height()
        for bill in self.bills:
            bill.update(dt)
        self.bills = [bill for bill in self.bills if not bill.off_screen(height)]
        for text in self.texts:
            text.update(dt)
        self.texts = [text for text in self.texts if text.alive]

        self.pulse = max(0.0, self.pulse - dt)
        self.away_timer = max(0.0, self.away_timer - dt)
        self.hovered = self.upgrades.hit(pygame.mouse.get_pos()) if pygame.mouse.get_focused() else None

        self.autosave_timer -= dt
        if self.autosave_timer <= 0:
            self.autosave_timer = settings.AUTOSAVE_INTERVAL
            self.save()

    # --- draw ------------------------------------------------------------
    def draw(self, surface):
        surface.fill(settings.BACKGROUND)
        self._draw_flag(surface)

        center_x = surface.get_width() // 2
        money_text = fmt.money(self.economy.money)
        draw_text(surface, money_text, 44, settings.DARK_TEXT, center=(center_x + 2, settings.MONEY_Y + 2))
        draw_text(surface, money_text, 44, settings.MONEY, center=(center_x, settings.MONEY_Y))
        info = f"{fmt.rate(self.economy.idle_income)}   |   {fmt.money(self.economy.bill_value)} per click"
        draw_text(surface, info, 20, settings.INCOME, center=(center_x, settings.INCOME_Y))

        self.upgrades.draw(surface, self.economy, self.hovered)
        for bill in self.bills:
            bill.draw(surface)
        for text in self.texts:
            text.draw(surface)
        if self.away_timer > 0 and self.away_message:
            self._draw_away_message(surface)

    def _draw_flag(self, surface):
        if self.pulse > 0:
            # Squash-and-stretch: wider and shorter right after a click, easing back.
            t = self.pulse / settings.FLAG_PULSE_TIME
            amount = settings.FLAG_PULSE_AMOUNT * t
            w, h = settings.FLAG_SIZE
            size = (round(w * (1 + amount)), round(h * (1 - amount)))
            image = pygame.transform.scale(assets.image(FLAG), size)
        else:
            image = flag_image()
        surface.blit(image, image.get_rect(center=self.flag_rect.center))

    def _draw_away_message(self, surface):
        line1, line2 = self.away_message
        panel = pygame.Rect(0, 0, surface.get_width() - 40, 64)
        panel.center = self.flag_rect.center
        alpha = int(255 * min(1.0, self.away_timer))  # fade out during the last second
        layer = pygame.Surface(panel.size, pygame.SRCALPHA)
        pygame.draw.rect(layer, (*settings.PANEL, 225), layer.get_rect(), border_radius=8)
        draw_text(layer, line1, 22, settings.MAXED, center=(panel.width // 2, 22))
        draw_text(layer, line2, 18, settings.TEXT, center=(panel.width // 2, 44))
        layer.set_alpha(alpha)
        surface.blit(layer, panel)


class PauseScene(Scene):
    """Pushed on top of the play scene; draws it frozen underneath."""

    def __init__(self, game, below):
        super().__init__(game)
        self.below = below

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_p, pygame.K_ESCAPE, pygame.K_RETURN):
                self.game.pop()
            elif event.key == pygame.K_q:
                from game.scenes.title import TitleScene

                self.game.switch(TitleScene(self.game))  # play scene saves in on_exit
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.game.pop()

    def draw(self, surface):
        self.below.draw(surface)
        dim(surface)
        w, h = surface.get_size()
        draw_text(surface, "PAUSED", 48, settings.TEXT, center=(w // 2, h // 2 - 20))
        draw_text(surface, "P to resume  |  Q to quit to title", 20, settings.CARD_LOCKED_TEXT, center=(w // 2, h // 2 + 24))
