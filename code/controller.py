from abc import abstractmethod, ABC

import pygame as pg
from player import Player
from pygame.locals import *
from constants_general import *


class Controller(ABC):
    def __init__(self, player):
        self._player = player
        self._pixel_array = None
        self._score = 0

    @abstractmethod
    def action(self):
        pass

    def set_game_info(self, score, pixel_array):
        self._pixel_array = pixel_array
        self._score = score

    @property
    def player(self):
        return self._player

    def set_player(self, player):
        self._player = player


class Controller_AI(Controller, ABC):
    def __init__(self, player=None):
        super().__init__(player)

    def action(self):
        pass


class Controller_Human(Controller, ABC):
    def __init__(self, player=None):
        super().__init__(player)

    def action(self):

        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT]:
            self._player.move(1)
        elif keys[pg.K_LEFT]:
            self._player.move(-1)
        if keys[pg.K_SPACE]:
            self._player.shoot_laser()