import pygame as pg
from player import Player
from pygame.locals import *
from constants_general import *


class Controller:
    def __init__(self, player=None, ai_player=False):
        self._player = player
        self._ai_player = ai_player

    def get_input(self):

        if not self.AI:
            keys = pg.key.get_pressed()

            if keys[pg.K_RIGHT]:
                self._player.move(1)
            elif keys[pg.K_LEFT]:
                self._player.move(-1)
            if keys[pg.K_SPACE]:
                self._player.shoot_laser()

    def set_ai_player(self, ai_player):
        self._ai_player = ai_player

    def set_player(self, player):
        self._player = player