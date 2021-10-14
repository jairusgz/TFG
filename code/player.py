import pygame as pg
from pygame.locals import *

class Player(pg.sprite.Sprite):

    def __init__(self, pos, screen_width, dimensions):
        #Crea un Sprite, carga la imagen del jugador, la reescala a 15x12px y la asigna una posicion inicial, por defecto la parte central inferior de la pantalla
        super().__init__()
        self.image = pg.image.load(r'..\Resources\player.png').convert_alpha()
        self.image = pg.transform.scale(self.image, dimensions)
        self.rect = self.image.get_rect(midbottom=pos)
        self.dimensions = dimensions
        self.speed = 3
        self.max_x = screen_width

        self.laser_ready = True
        self.laser_time = 0
        self.laser_cd = 800

    def move(self, dir):
        if self.rect.x + self.dimensions[0] + dir * self.speed < self.max_x and self.rect.x + dir * self.speed > 0:
            self.rect.x += dir * self.speed

    def update(self):
        self.laser_reload()

    def shoot_laser(self):
        if self.laser_ready:
            print('Shoot Laser')
            self.laser_ready = False
            self.laser_time = pg.time.get_ticks()


    def laser_reload(self):
        if not self.laser_ready:
            if pg.time.get_ticks() - self.laser_time >= self.laser_cd:
                self.laser_ready = True

