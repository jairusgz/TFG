import pygame as pg
from os import path

class Alien(pg.sprite.Sprite):
    def __init__(self, color):
        super().__init__():
        path = os.path.join('..', 'Resources', color + '.png')
        self.image = pg.image.load(path).convert_alpha()
