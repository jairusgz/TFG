import os
import pygame as pg
import math


class Alien(pg.sprite.Sprite):
    def __init__(self, dimensions, initial_pos, img_path):
        super().__init__()
        self._image = pg.image.load(img_path).convert_alpha()
        self._image = pg.transform.scale(self._image, dimensions)
        self._rect = self._image.get_rect(topleft=initial_pos)
        self._absolute_x = self._rect.x
        self._value = 0

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


class Alien_red(Alien):
    def __init__(self, dimensions, initial_pos):
        img_path = os.path.join('tfg/Resources', 'red.png')
        super().__init__(dimensions, initial_pos, img_path)
        self._value = 10


class Alien_green(Alien):
    def __init__(self, dimensions, initial_pos):
        img_path = os.path.join('tfg/Resources', 'green.png')
        super().__init__(dimensions, initial_pos, img_path)
        self._value = 20


class Alien_yellow(Alien):
    def __init__(self, dimensions, initial_pos):
        img_path = os.path.join('tfg/Resources', 'yellow.png')
        super().__init__(dimensions, initial_pos, img_path)
        self._value = 30


class Mothership(pg.sprite.Sprite):
    def __init__(self, y, dimensions, side, speed, screen_size):
        super().__init__()

        self._image = pg.image.load('tfg/Resources/extra.png').convert_alpha()
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
