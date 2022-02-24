import os

import pygame as pg
import math

filenames = {'red': os.path.join('../Resources', 'red.png'),
             'yellow': os.path.join('../Resources', 'yellow.png'),
             'green': os.path.join('../Resources', 'green.png')}


class Alien(pg.sprite.Sprite):
    def __init__(self, dimensions, color, initial_pos, value):


        super().__init__()
        img_path = filenames[color]
        self.image = pg.image.load(img_path).convert_alpha()
        self.image = pg.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect(topleft=initial_pos)
        self.absolute_x = self.rect.x
        self.value = value

    def update(self, direction):
        self.absolute_x += direction
        self.rect.x = math.trunc(self.absolute_x)

    def get_value(self):
        return self.value


class Mothership(pg.sprite.Sprite):
    def __init__(self, y, dimensions, side, speed, screen_size):
        super().__init__()
        self.image = pg.image.load('../Resources/extra.png').convert_alpha()
        self.image = pg.transform.scale(self.image, dimensions)

        if side == 'right':
            x = screen_size[0] + 50
            self.speed = -speed
        else:
            x = -50
            self.speed = speed

        self.rect = self.image.get_rect(topleft=(x, y))
        self.absolute_x = self.rect.x

    def update(self):
        self.absolute_x += self.speed
        self.rect.x = math.trunc(self.absolute_x)
