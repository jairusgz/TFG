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
        self._model = DeepQAgent((84, 84, 4,), 6)
        self._frame_count = 0
        self._frame_memory = []
        self._state = None
        self._next_state = None
        self._score_0 = 0
        self._score_1 = 0
        self._done = 0
        self._action = 0
        self._new_episode = False
        self._action_mapping = {0: lambda: self._player.move(0),
                                1: lambda: self._player.move(-1),
                                2: lambda: self._player.move(1),
                                3: lambda: self._player.shoot_laser(),
                                4: lambda: self._player.move(-1) and self._player.shoot_laser(),
                                5: lambda: self._player.move(1) and self._player.shoot_laser()}

    def stack_frame(self, frame, score):
        """
        Processes every 4th frame and stacks last 4 processed frames. Then trains the model with the stacked frames.
        """

        if self._new_episode:
            self._frame_memory = []
            self._score_0 = 0
            self._score_1 = 0
            self._new_episode = False

        self._score_1 += score

        if self._frame_count % 4 == 0:
            self._score_0 = score

            self._frame_memory.append((self.__process_frame(frame), score))
            if len(self._frame_memory) > 4:
                self._frame_memory.pop(0)

            if len(self._frame_memory) == 4:
                pass
                # TODO Train model

        self._frame_count += 1
        self._action = self._model.action

    def __process_frame(self, state):
        arr = np.array(state)
        # First, we crop the image to remove the top and bottom of the screen
        arr = arr[:480, 81:561]

        #Then, we downscale the image to 84x84
        img = pg.image.frombuffer(arr, (480, 480), 'RGB')
        img = pg.transform.scale(img, (84, 84))

        #We get the pixel array from the new image
        arr = pg.surfarray.array3d(img)

        # Then, we convert the array to grayscale
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        gray_scale_arr = 0.2989 * r + 0.5870 * g + 0.1140 * b

        return gray_scale_arr

    def action(self):
        self._action_mapping[self._action]()

    def set_new_episode(self):
        self._new_episode = True

    @property
    def new_episode(self):
        return self._new_episode

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
