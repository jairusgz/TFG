import pygame as pg


class Laser(pg.sprite.Sprite):
    def __init__(self, pos, speed, dimensions, screen_height):

        super().__init__()
        self.max_y = screen_height
        self.dimensions = dimensions
        self.image = pg.Surface(dimensions)
        self.image.fill('White')
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= self.dimensions[1] or self.rect.y >= self.max_y + self.dimensions[1]:
            self.kill()
