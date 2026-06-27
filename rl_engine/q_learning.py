import numpy as np


class QLearning:

    def __init__(

        self,

        states=6,

        actions=6,

        alpha=0.1,

        gamma=0.9,

        epsilon=0.2

    ):

        self.alpha = alpha

        self.gamma = gamma

        self.epsilon = epsilon

        self.q_table = np.zeros(
            (
                states,
                actions
            )
        )

    def choose_action(

        self,

        state,

        valid_actions

    ):

        if np.random.rand() < self.epsilon:

            return np.random.choice(
                valid_actions
            )

        values = self.q_table[
            state,
            valid_actions
        ]

        return valid_actions[
            np.argmax(
                values
            )
        ]

    def update(

        self,

        state,

        action,

        reward,

        next_state

    ):

        best_next = np.max(
            self.q_table[
                next_state
            ]
        )

        current = self.q_table[
            state,
            action
        ]

        self.q_table[
            state,
            action
        ] = (

            current

            +

            self.alpha

            *

            (

                reward

                +

                self.gamma

                *

                best_next

                -

                current

            )
        )