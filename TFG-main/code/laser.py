import pygame as pg
from constants import *

class Laser(pg.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.image = pg.Surface((LASER_WIDTH, LASER_HEIGTH))
        self.image.fill('White')
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed


    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= -20 * REESCALADO or self.rect.y >= SCREEN_HEIGTH + 20 * REESCALADO:
            self.kill()
