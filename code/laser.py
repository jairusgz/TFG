import pygame as pg

class Laser(pg.sprite.Sprite):
    def __init__(self, pos, speed=-5, screen_height = 210):
        super().__init__()
        self.image = pg.Surface((2, 10))
        self.image.fill('White')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.max_y = screen_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= -20 or self.rect.y >= self.max_y + 20:
            self.kill()
