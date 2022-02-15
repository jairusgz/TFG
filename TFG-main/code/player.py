import pygame as pg
from pygame.locals import *
from laser import Laser
from constants import *


class Player(pg.sprite.Sprite):

    def __init__(self, pos, dimensions):

        # Crea un Sprite, carga la imagen del jugador, la reescala a 15x12px y la asigna una posicion inicial,
        # por defecto la parte central inferior de la pantalla

        super().__init__()
        self.image = pg.image.load('../Resources/player.png').convert_alpha()
        self.image = pg.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect(midbottom=pos)
        self.dimensions = dimensions
        self.speed = PLAYER_SPEED
        self.max_x = SCREEN_WIDTH

        self.lasers = pg.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_cd = PLAYER_LASER_CD

    def move(self, dir):
        if self.rect.x + self.dimensions[0] + dir * self.speed < self.max_x and self.rect.x + dir * self.speed > 0:
            self.rect.x += dir * self.speed

    def update(self):
        self.laser_reload()
        self.lasers.update()

    def shoot_laser(self):
        if self.laser_ready:
            self.lasers.add(Laser(self.rect.center, -LASER_SPEED))
            self.laser_ready = False
            self.laser_time = pg.time.get_ticks()

    def laser_reload(self):
        if not self.laser_ready:
            if pg.time.get_ticks() - self.laser_time >= self.laser_cd:
                self.laser_ready = True
