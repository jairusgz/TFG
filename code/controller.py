from abc import abstractmethod, ABC
from skimage.measure import block_reduce
import numpy as np
import pygame as pg
from player import Player
from pygame.locals import *
from constants_general import *
from deep_Q_agent import DeepQAgent


class Controller(ABC):
    def __init__(self, player):
        self._player = player
        self._state = None
        self._next_state = None
        self._score = 0

    @abstractmethod
    def action(self):
        pass

    @property
    def player(self):
        return self._player

    def set_player(self, player):
        self._player = player


class Controller_AI(Controller, ABC):
    def __init__(self, player=None):
        super().__init__(player)
        self._model = DeepQAgent((80, 80, 1,), 6)
        self._state = None
        self._next_state = None
        self._reward = 0
        self._done = 0
        self._action = 0
        self._new_episode = False
        self._action_mapping = {0: lambda: self._player.move(0),
                                1: lambda: self._player.move(-1),
                                2: lambda: self._player.move(1),
                                3: lambda: self._player.shoot_laser(),
                                4: lambda: self._player.move(-1) and self._player.shoot_laser(),
                                5: lambda: self._player.move(1) and self._player.shoot_laser()}

    def __preprocess_state(self, state):
        arr = np.array(state)
        # First, we crop the image to remove the top and bottom of the screen
        arr = arr[:160, 27:187]

        # Then, we convert the array to grayscale
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        gray_scale_arr = 0.2989 * r + 0.5870 * g + 0.1140 * b

        # We normalize the array
        gray_scale_arr /= 255

        # Finally, we downsample the array to a 80x80 shape
        return block_reduce(gray_scale_arr, block_size=(2, 2), func=np.mean)

    def train_model(self, state):
        self._state = self.__preprocess_state(state)
        self._action = self._model.train(self._state, new_episode=self._new_episode)
        self._new_episode = False

    def update_model(self, next_state, reward):
        self._model.update(self._state, self._action, reward, self.__preprocess_state(next_state))

    def action(self):
        self._action_mapping[self._action]()

    def new_episode(self):
        self._new_episode = True

    def model_trained(self):
        return self._model.done


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
