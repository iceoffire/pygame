"""Drawing helpers: images at their in-game size, simple drawn icons, and the upgrade list."""
from functools import cache

import pygame

import settings
from game import assets
from game import format as fmt
from game.economy import BIGGER_BILLS, UPGRADES, bill_value
from game.scene import draw_text

FLAG = "images/flag.png"


def bill_path(value):
    return f"images/bills/bill_{value}.png"


def flag_image(size=settings.FLAG_SIZE):
    # The flag is 30x21 pixel art: nearest-neighbour scaling keeps it crisp.
    return assets.scaled(FLAG, tuple(size), smooth=False)


def bill_image(value):
    return assets.scaled(bill_path(value), settings.BILL_SIZE)


# --- icons ---------------------------------------------------------------
def upgrade_icon(upgrade, level):
    box = settings.ICON_BOX
    if upgrade.icon.startswith("image:"):
        return assets.fitted(upgrade.icon.removeprefix("image:"), box)
    if upgrade.icon == "bills":
        # Show the bill this upgrade buys next (or the top bill once maxed).
        return assets.fitted(bill_path(bill_value(level + 1)), box)
    return drawn_icon(upgrade.icon)


@cache
def drawn_icon(name):
    """Small vector icons for upgrades that have no image asset."""
    w, h = settings.ICON_BOX
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    dark = (30, 30, 30)
    if name == "pump":
        pygame.draw.rect(s, (60, 60, 60), (6, 38, 30, 5))
        pygame.draw.rect(s, (200, 40, 40), (10, 6, 22, 33), border_radius=4)
        pygame.draw.rect(s, (230, 230, 230), (14, 10, 14, 10), border_radius=2)
        pygame.draw.lines(s, dark, False, [(32, 14), (41, 14), (41, 31), (37, 33)], 3)
        pygame.draw.rect(s, dark, (33, 31, 6, 5))
    elif name == "store":
        pygame.draw.rect(s, (230, 220, 190), (8, 16, 32, 24))
        for i in range(4):
            color = (210, 50, 50) if i % 2 == 0 else (245, 245, 245)
            pygame.draw.rect(s, color, (6 + i * 9, 9, 9, 8))
        pygame.draw.rect(s, (120, 80, 40), (22, 26, 9, 14))
        pygame.draw.rect(s, (150, 210, 240), (11, 22, 8, 8))
        pygame.draw.line(s, (60, 60, 60), (4, 40), (44, 40), 2)
    elif name == "car_wash":
        for center, radius in (((10, 9), 4), ((20, 5), 3), ((31, 9), 5), ((41, 5), 3)):
            pygame.draw.circle(s, (150, 200, 255), center, radius)
            pygame.draw.circle(s, (255, 255, 255), center, radius, 1)
        pygame.draw.rect(s, (40, 120, 220), (14, 17, 20, 10), border_radius=4)
        pygame.draw.rect(s, (40, 120, 220), (5, 24, 38, 11), border_radius=4)
        pygame.draw.rect(s, (190, 225, 250), (17, 19, 14, 6), border_radius=2)
        pygame.draw.circle(s, dark, (14, 35), 5)
        pygame.draw.circle(s, dark, (34, 35), 5)
    elif name == "refinery":
        pygame.draw.circle(s, (210, 210, 210), (41, 6), 4)
        pygame.draw.circle(s, (225, 225, 225), (45, 2), 2)
        pygame.draw.rect(s, (150, 60, 40), (36, 10, 7, 30))
        pygame.draw.rect(s, (170, 175, 180), (4, 20, 17, 20))
        pygame.draw.ellipse(s, (200, 205, 210), (4, 16, 17, 8))
        pygame.draw.rect(s, (170, 175, 180), (23, 26, 12, 14))
        pygame.draw.ellipse(s, (200, 205, 210), (23, 23, 12, 6))
        pygame.draw.line(s, (90, 90, 90), (20, 32), (24, 32), 2)
        pygame.draw.line(s, (60, 60, 60), (2, 41), (46, 41), 2)
    else:
        pygame.draw.circle(s, (120, 120, 120), (w // 2, h // 2), min(w, h) // 3)
    return s


# --- upgrade list ----------------------------------------------------------
class UpgradeList:
    """Vertical list of upgrade cards. Drawing and hit-testing share card_rect(), so they always match."""

    def __init__(self):
        self.rect = pygame.Rect(settings.LIST_RECT)
        self.card_w, self.card_h = settings.CARD_SIZE
        self.step = self.card_h + settings.CARD_GAP
        self.scroll = 0
        content_h = len(UPGRADES) * self.step - settings.CARD_GAP
        self.max_scroll = max(0, content_h - self.rect.height)
        self.icon_shade = pygame.Surface(settings.ICON_BOX, pygame.SRCALPHA)
        self.icon_shade.fill((*settings.CARD_LOCKED, 150))

    def scroll_by(self, pixels):
        self.scroll = max(0, min(self.max_scroll, self.scroll + pixels))

    def card_rect(self, index):
        x = self.rect.x + (self.rect.width - self.card_w) // 2
        y = self.rect.y + index * self.step - self.scroll
        return pygame.Rect(x, y, self.card_w, self.card_h)

    def hit(self, pos):
        """Index of the card under `pos`, or None. Parts scrolled out of the list don't count."""
        if pos is None or not self.rect.collidepoint(pos):
            return None
        for index in range(len(UPGRADES)):
            if self.card_rect(index).collidepoint(pos):
                return index
        return None

    def draw(self, surface, economy, hovered):
        surface.set_clip(self.rect)
        for index, upgrade in enumerate(UPGRADES):
            rect = self.card_rect(index)
            if rect.colliderect(self.rect):
                self._draw_card(surface, rect, upgrade, economy, index == hovered)
        surface.set_clip(None)
        if self.max_scroll:
            track = pygame.Rect(self.rect.right - 6, self.rect.y, 4, self.rect.height)
            pygame.draw.rect(surface, settings.MUTED, track, border_radius=2)
            thumb_h = max(24, track.height * track.height // (track.height + self.max_scroll))
            thumb_y = track.y + (track.height - thumb_h) * self.scroll // self.max_scroll
            pygame.draw.rect(surface, settings.CARD, (track.x, thumb_y, track.width, thumb_h), border_radius=2)

    def _draw_card(self, surface, rect, upgrade, economy, hovered):
        level = economy.level(upgrade)
        maxed = economy.is_maxed(upgrade)
        affordable = economy.can_afford(upgrade)
        locked = not affordable and not maxed

        if locked:
            background, text = settings.CARD_LOCKED, settings.CARD_LOCKED_TEXT
        else:
            background = settings.CARD_HOVER if hovered else settings.CARD
            text = settings.TEXT
        pygame.draw.rect(surface, background, rect, border_radius=6)
        border, width = settings.CARD_BORDER, 1
        if hovered and affordable:
            border, width = settings.CARD_HOVER_BORDER, 2
        pygame.draw.rect(surface, border, rect, width, border_radius=6)

        icon_box = pygame.Rect(rect.x + 8, rect.y + (rect.height - settings.ICON_BOX[1]) // 2, *settings.ICON_BOX)
        icon = upgrade_icon(upgrade, level)
        surface.blit(icon, icon.get_rect(center=icon_box.center))
        if locked:
            surface.blit(self.icon_shade, icon_box)

        left = icon_box.right + 10
        draw_text(surface, upgrade.name, 22, text, topleft=(left, rect.y + 8))
        level_text = f"Lv {level}"
        level_w = assets.font(18).size(level_text)[0]
        draw_text(surface, level_text, 18, text, topleft=(rect.right - 10 - level_w, rect.y + 10))

        if maxed:
            draw_text(surface, "Price: MAXED", 18, settings.MAXED, topleft=(left, rect.y + 29))
        else:
            color = settings.PRICE_OK if affordable else settings.PRICE_TOO_HIGH
            draw_text(surface, f"Price: {fmt.money(economy.price(upgrade))}", 18, color, topleft=(left, rect.y + 29))

        if upgrade.key == BIGGER_BILLS:
            if maxed:
                gain = f"Gain: {fmt.money(economy.bill_value)} per click"
            else:
                gain = f"Gain: click {fmt.money(economy.bill_value)} -> {fmt.money(bill_value(level + 1))}"
        else:
            gain = f"Gain: +{fmt.rate(upgrade.income)} each"
        draw_text(surface, gain, 18, text, topleft=(left, rect.y + 45))
