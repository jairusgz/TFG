import pygame as pg
from player import Player
from pygame.locals import *

class Controller:
    def __init__(self, player, AI=False):
        self.player = player
        self.AI = AI

    def get_input(self):

        if not self.AI:
            keys = pg.key.get_pressed()

            if keys[pg.K_RIGHT]:
                self.player.move(1)
            elif keys[pg.K_LEFT]:
                self.player.move(-1)

