import pygame as pg
from laser import Laser
from game_parameters import *


class Player(pg.sprite.Sprite):

    def __init__(self, start_pos, dimensions, player_speed, laser_speed, laser_dimensions, screen_dimensions):
        super().__init__()
        self._image = pg.image.load('tfg/Resources/player.png').convert_alpha()
        self._image = pg.transform.scale(self._image, dimensions)
        self._rect = self._image.get_rect(midbottom=start_pos)
        self._dimensions = dimensions
        self._speed = player_speed
        self._max_x = screen_dimensions[0]
        self._max_y = screen_dimensions[1]

        self._lasers = pg.sprite.Group()
        self._laser_ready = True
        self._laser_time = 0
        self._laser_cd = PLAYER_LASER_CD
        self._laser_count = 0
        self._laser_speed = laser_speed
        self._laser_dimensions = laser_dimensions

    def move(self, dir):
        if self._rect.x + self._dimensions[0] + dir * self._speed < self._max_x and \
                self._rect.x + dir * self._speed > 0:

            self._rect.x += dir * self._speed

    def update(self):
        self.__laser_reload()
        self._lasers.update()

    def shoot_laser(self):
        if self._laser_ready:
            self._lasers.add(Laser(self._rect.center, - self._laser_speed, self._laser_dimensions, self._max_y))
            self._laser_ready = False
            self._laser_time = pg.time.get_ticks()
            self._laser_count += 1

    def __laser_reload(self):
        if not self._laser_ready:
            if pg.time.get_ticks() - self._laser_time >= self._laser_cd:
                self._laser_ready = True


    @property
    def laser_count(self):
        return self._laser_count

    @property
    def lasers(self):
        return self._lasers

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    @property
    def laser_ready(self):
        return self._laser_ready

    @property
    def get_pos(self):
        return self._rect.center

    def count_shots(self):
        self._laser_count += 1
