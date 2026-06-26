import numpy as np

from rl_engine.topology import NUM_NODES


class QLearningAgent:

    def __init__(
        self,
        learning_rate=0.1,
        discount_factor=0.9,
        epsilon=0.2
    ):

        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon

        self.q_table = np.zeros(
            (NUM_NODES, NUM_NODES)
        )

    def choose_action(
        self,
        state,
        valid_actions
    ):

        if np.random.random() < self.epsilon:
            return np.random.choice(
                valid_actions
            )

        scores = [
            self.q_table[state][a]
            for a in valid_actions
        ]

        best = np.argmax(scores)

        return valid_actions[best]

    def update(
        self,
        state,
        action,
        reward,
        next_state
    ):

        current = self.q_table[
            state
        ][action]

        future = np.max(
            self.q_table[
                next_state
            ]
        )

        updated = (
            current
            +
            self.alpha
            *
            (
                reward
                +
                self.gamma
                * future
                -
                current
            )
        )

        self.q_table[
            state
        ][action] = updated