import os
import pygame as pg
import math


class Alien(pg.sprite.Sprite):
    def __init__(self, dimensions, color, initial_pos, value):
        super().__init__()
        self._image_paths = {'red': os.path.join('../Resources', 'red.png'),
                             'yellow': os.path.join('../Resources', 'yellow.png'),
                             'green': os.path.join('../Resources', 'green.png')}

        img_path = self._image_paths[color]
        self._image = pg.image.load(img_path).convert_alpha()
        self._image = pg.transform.scale(self._image, dimensions)
        self._rect = self._image.get_rect(topleft=initial_pos)
        self._absolute_x = self._rect.x
        self._value = value

    def update(self, direction):
        self._absolute_x += direction
        self._rect.x = math.trunc(self._absolute_x)

    @property
    def value(self):
        return self._value

    @property
    def rect(self):
        return self._rect

    @property
    def image(self):
        return self._image


class Mothership(pg.sprite.Sprite):
    def __init__(self, y, dimensions, side, speed, screen_size):
        super().__init__()

        self._image = pg.image.load('../Resources/extra.png').convert_alpha()
        self._image = pg.transform.scale(self._image, dimensions)

        if side == 'right':
            x = screen_size[0] + 50
            self._speed = -speed
        else:
            x = -50
            self._speed = speed

        self._rect = self._image.get_rect(topleft=(x, y))
        self._absolute_x = self._rect.x

    def update(self):
        self._absolute_x += self._speed
        self._rect.x = math.trunc(self._absolute_x)

    @property
    def rect(self):
        return self._rect

    @property
    def image(self):
        return self._image
