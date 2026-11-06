import settings
from game import assets
from game.animation import Animation

THRUSTER_FRAMES = "images/effects/thruster_{:02d}.png"
TILTS = ("left", "mid", "right")


def ship_path(hp, tilt):
    return f"images/player/ship_hp{hp}_{tilt}.png"


class Player:
    def __init__(self):
        self.images = {
            (hp, tilt): assets.image(ship_path(hp, tilt))
            for hp in range(1, settings.PLAYER_MAX_HP + 1)
            for tilt in TILTS
        }
        self.hp = settings.PLAYER_MAX_HP
        self.tilt = "mid"
        self.rect = self.image.get_frect(topleft=settings.PLAYER_START)
        self.velocity = 0.0
        self.cooldown = 0.0
        self.invulnerable = 0.0
        self.thruster = Animation(assets.frames(THRUSTER_FRAMES, 4), settings.THRUSTER_FRAME_TIME)

    @property
    def alive(self):
        return self.hp > 0

    @property
    def image(self):
        # Clamp so a dead ship (hp 0) can never look up a missing sprite.
        hp = max(1, min(self.hp, settings.PLAYER_MAX_HP))
        return self.images[(hp, self.tilt)]

    @property
    def hitbox(self):
        return self.rect.inflate(-settings.PLAYER_HITBOX_SHRINK[0], -settings.PLAYER_HITBOX_SHRINK[1])

    @property
    def visible(self):
        if not self.alive:
            return False
        if self.invulnerable <= 0:
            return True
        return int(self.invulnerable / settings.PLAYER_BLINK_INTERVAL) % 2 == 0

    @property
    def can_fire(self):
        return self.alive and self.cooldown <= 0

    def update(self, dt, direction, screen_width):
        """direction: -1 left, 0 none, 1 right."""
        self.cooldown = max(0.0, self.cooldown - dt)
        self.invulnerable = max(0.0, self.invulnerable - dt)
        self.thruster.update(dt)

        if direction:
            self.velocity += direction * settings.PLAYER_ACCELERATION * dt
            self.tilt = "right" if direction > 0 else "left"
        else:
            self.velocity *= settings.PLAYER_FRICTION ** (dt * 60)
            self.tilt = "mid"
        limit = settings.PLAYER_MAX_SPEED
        self.velocity = max(-limit, min(limit, self.velocity))

        self.rect.x += self.velocity * dt
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity = 0.0
            self.tilt = "mid"
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
            self.velocity = 0.0
            self.tilt = "mid"

    def hit(self):
        """Lose one HP unless invulnerable. Returns True when damage was taken."""
        if not self.alive or self.invulnerable > 0:
            return False
        self.hp -= 1
        self.invulnerable = settings.PLAYER_INVULNERABLE_TIME
        return True

    def draw(self, surface):
        if not self.visible:
            return
        surface.blit(self.image, self.rect.topleft)
        # Two engine flames under the ship; they sit closer together when the ship tilts.
        y = self.rect.y + self.rect.height - 5
        if self.tilt == "mid":
            x, gap = self.rect.x + 2, 25
        else:
            x, gap = self.rect.x + 4, 18
        flame = self.thruster.image
        surface.blit(flame, (x, y))
        surface.blit(flame, (x + gap, y))
