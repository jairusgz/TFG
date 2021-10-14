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

    def move(self, dir):
        if self.rect.x + self.dimensions[0] + dir * self.speed < self.max_x and self.rect.x + dir * self.speed > 0:
            self.rect.x += dir * self.speed

    def update(self):
        pass
