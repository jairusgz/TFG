from abc import abstractmethod, ABC
import numpy as np
import pygame as pg
from player import *
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
        self._score_memory = []
        self._action_memory = []
        self._cumulative_score = 0
        self._done = 0
        self._action = 0
        self._prev_action = 0
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
        self._action = self._model.action

        if self._new_episode:
            self._frame_memory = []
            self._score_memory = []
            self._action_memory = []
            self._cumulative_score = 0
            self._score = 0
            self._new_episode = False
            self._model.new_episode()

        if self._frame_count % 4 == 0:
            self._cumulative_score = 0
            self._frame_memory.append(self.__process_frame(frame))
            self._score_memory.append(score)
            self._action_memory.append(self._action)

            if len(self._frame_memory) > 5:
                self._frame_memory.pop(0)
                self._score_memory.pop(0)
                self._action_memory.pop(0)

            if len(self._frame_memory) == 5:
                reward = self._score_memory[-1] - self._score_memory[-2]
                self._model.train(np.array(self._frame_memory[1:]).transpose(2, 1, 0))

                state = np.array(self._frame_memory[:-1]).transpose(2, 1, 0)
                next_state = np.array(self._frame_memory[1:]).transpose(2, 1, 0)
                action = self._action_memory[0]

                self._model.update(state, action, reward, next_state)

        self._frame_count += 1

    def __process_frame(self, state):
        arr = np.array(state)
        # First, we crop the image to remove the top and bottom of the screen, leaving a 480x480 image.
        arr = arr[:480, 81:561].copy(order='C')

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
