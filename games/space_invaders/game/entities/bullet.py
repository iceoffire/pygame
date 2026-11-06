from game import assets

PLAYER_BULLET = "images/projectiles/bullet_player.png"
ENEMY_BULLET = "images/projectiles/bullet_enemy.png"


class Bullet:
    def __init__(self, image_name, topleft, speed):
        self.image = assets.image(image_name)
        self.rect = self.image.get_frect(topleft=topleft)
        self.speed = speed  # pixels per second; negative goes up
        self.alive = True

    def update(self, dt, screen_height):
        self.rect.y += self.speed * dt
        # Remove bullets leaving through either edge (enemy bullets travel down).
        if self.rect.bottom < 0 or self.rect.top > screen_height:
            self.alive = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
