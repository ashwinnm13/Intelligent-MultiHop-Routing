import numpy as np

from rl_engine.topology import NUM_NODES


class QLearningAgent:

    def __init__(self,learning_rate=0.1,discount_factor=0.9,epsilon=0.2):

        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon

        # Q[state][action]
        self.q_table = np.zeros((NUM_NODES, NUM_NODES))

    def choose_action(self,state,valid_actions):

        # Exploration
        if np.random.rand() < self.epsilon:
            return np.random.choice(valid_actions)

        # Exploitation
        scores = [self.q_table[state][a] for a in valid_actions]

        return valid_actions[np.argmax(scores)]

    def update(
        self,
        state,
        action,
        reward,
        next_state
    ):

        old_value = (
            self.q_table[state][action]
        )

        next_best = np.max(
            self.q_table[next_state]
        )

        new_value = (old_value + self.alpha*(reward + self.gamma*next_best -old_value))

        self.q_table[
            state
        ][action] = new_value