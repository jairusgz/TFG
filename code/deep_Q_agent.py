import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.losses import *


class DeepQAgent:
    def __init__(self, state_size, action_size, model_file=None):
        self._episode_reward = 0
        self._state_size = state_size
        self._action_size = action_size
        self._new_episode = True
        self._optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)
        self._done = False

        # Experience replay buffers and training parameters
        self._action_history = []
        self._state_history = []
        self._state_next_history = []
        self._rewards_history = []
        self._done_history = []
        self._episode_reward_history = []
        self._running_reward = 0
        self._episode_count = 0
        self._frame_count = 0
        self._epsilon_random_frames = 50000
        self._epsilon_greedy_frames = 1000000.0
        self._max_memory_length = 100000
        self._update_after_actions = 4
        self._update_target_network = 10000
        self._loss_function = keras.losses.Huber()

        # Build the model
        self._gamma = 0.99
        self._epsilon = 1.0
        self._epsilon_min = 0.1
        self._epsilon_decay = 0.995
        self._learning_rate = 0.0002
        self._batch_size = 32
        self._max_steps_per_episode = 10000
        self._model = self.__build_model()
        self._target_model = self.__build_model()
        if model_file:
            self._model.load_weights(model_file)

    def __build_model(self):
        # Input layer of shape 80x80
        inputs = layers.Input(shape=self._state_size)

        # 3 convolutional layers
        layer1 = layers.Conv2D(32, 8, strides=4, activation='relu')(inputs)
        layer2 = layers.Conv2D(64, 4, strides=2, activation='relu')(layer1)
        layer3 = layers.Conv2D(64, 3, strides=1, activation='relu')(layer2)

        # Flatten the output of the convolutional layers
        flatten = layers.Flatten()(layer3)

        # Fully connected layer
        layer5 = layers.Dense(512, activation='relu')(flatten)

        # Output layer
        output = layers.Dense(self._action_size, activation='linear')(layer5)

        return keras.Model(inputs=inputs, outputs=output)

    def train(self, state, new_episode=False):
        if not self._done:
            self._frame_count += 1
            self._new_episode = new_episode
            if self._frame_count % 100 == 0:
                print("Frame count: {}".format(self._frame_count))

            if self._frame_count >= self._max_steps_per_episode:
                self._new_episode = True

            if self._new_episode:
                self._episode_count += 1
                self._new_episode = False
                self._frame_count = 0
                self._episode_reward = 0
                print('Episode: {}'.format(self._episode_count))

            if self._frame_count < self._epsilon_random_frames or self._epsilon > np.random.rand(1)[0]:
                # Take random action
                action = np.random.choice(self._action_size)
            else:
                # Predict the Q values for the next state
                state_tensor = tf.convert_to_tensor(state)
                state_tensor = tf.expand_dims(state_tensor, 0)
                action_probs = self._model(state_tensor, training=False)
                # Take best action
                action = tf.argmax(action_probs[0]).numpy()

            self._epsilon -= self._epsilon_decay / self._epsilon_greedy_frames
            self._epsilon = max(self._epsilon, self._epsilon_min)

            return action
        else:
            print("Solved at episode {}!".format(self._episode_count))

    def update(self, state, action, reward, state_next):
        if not self._done:

            self._episode_reward += reward

            # Save actions and states in replay buffer
            self._action_history.append(action)
            self._state_history.append(state)
            self._state_next_history.append(state_next)
            self._done_history.append(self._done)
            self._rewards_history.append(reward)

            if self._frame_count % self._update_after_actions == 0 and len(self._done_history) > self._batch_size:
                # Get indices of samples for replay buffers
                indices = np.random.choice(range(len(self._done_history)), size=self._batch_size)

                # Using list comprehension to sample from replay buffer
                state_sample = np.array([self._state_history[i] for i in indices])
                state_next_sample = np.array([self._state_next_history[i] for i in indices])
                rewards_sample = [self._rewards_history[i] for i in indices]
                action_sample = [self._action_history[i] for i in indices]
                done_sample = tf.convert_to_tensor(
                    [float(self._done_history[i]) for i in indices]
                )

                # Build the updated Q-values for the sampled future states
                # Use the target model for stability
                future_rewards = self._target_model.predict(state_next_sample)
                # Q value = reward + discount factor * expected future reward
                updated_q_values = rewards_sample + self._gamma * tf.reduce_max(
                    future_rewards, axis=1
                )

                # If final frame set the last value to -1
                updated_q_values = updated_q_values * (1 - done_sample) - done_sample

                # Create a mask so we only calculate loss on the updated Q-values
                masks = tf.one_hot(action_sample, self._action_size)

                with tf.GradientTape() as tape:
                    # Train the model on the states and updated Q-values
                    q_values = self._model(state_sample.astype(np.float32))

                    # Apply the masks to the Q-values to get the Q-value for action taken
                    q_action = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
                    # Calculate loss between new Q-value and old Q-value
                    loss = self._loss_function(updated_q_values, q_action)

                # Backpropagation
                grads = tape.gradient(loss, self._model.trainable_variables)
                self._optimizer.apply_gradients(zip(grads, self._model.trainable_variables))

            if self._frame_count % self._update_target_network == 0:
                # update the the target network with new weights
                self._target_model.set_weights(self._model.get_weights())
                # Log details
                template = "running reward: {:.2f} at episode {}, frame count {}"
                print(template.format(self._running_reward, self._episode_count, self._frame_count))

                # Limit the state and reward history
            if len(self._rewards_history) > self._max_memory_length:
                del self._rewards_history[:1]
                del self._state_history[:1]
                del self._state_next_history[:1]
                del self._action_history[:1]
                del self._done_history[:1]


                # Update running reward to check condition for solving
            self._episode_reward_history.append(self._episode_reward)
            if len(self._episode_reward_history) > 100:
                del self._episode_reward_history[:1]
            running_reward = np.mean(self._episode_reward_history)

            if running_reward > 2000:  # Condition to consider the task solved
                print("Solved at episode {}!".format(self._episode_count))
                self._done = True


    @property
    def new_episode(self):
        return self._new_episode

