import pygame as pg


class Block(pg.sprite.Sprite):
    def __init__(self, size, color, x, y):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
