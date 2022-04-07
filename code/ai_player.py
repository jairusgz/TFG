import keras
import numpy as np
from keras.models import Model
from keras.optimizers import Adam
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Activation
import random


class DeepQNetwork:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self._batch_size = 32
        self._frame_per_action = 4
        self._frame_count = 0
        self.model = self._build_model()

    def _build_model(self):
        #Build a model that receives a pixel array in grey scale of size (210, 160, 3) and outputs a Q-value for each action
        model = keras.Sequential()
        model.add(keras.layers.Conv2D(32, (8, 8), strides=(4, 4), activation='relu', input_shape=self.state_size))
        model.add(keras.layers.Conv2D(64, (4, 4), strides=(2, 2), activation='relu'))
        model.add(keras.layers.Conv2D(64, (3, 3), strides=(1, 1), activation='relu'))
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(512, activation='relu'))
        model.add(keras.layers.Dense(self.action_size))
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self):
        minibatch = random.sample(self.memory, self._batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    """
    Trains the model by passing the game state and score to the model.
    The model will then train the model by using the experience replay.
    """
    def train(self, state, score):
        if self._frame_count % self._frame_per_action == 0:
            if len(self.memory) < self._batch_size:
                return
            self.replay()
            self.remember(state, score)
        self._frame_count += 1

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def get_weights(self):
        return self.model.get_weights()

    def set_weights(self, weights):
        self.model.set_weights(weights)

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model




