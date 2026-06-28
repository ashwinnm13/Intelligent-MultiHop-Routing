from rl_engine.topology import (
    adjacency_matrix,
)

from backend.dynamic_network import (
    generate_latency,
    generate_loss,
)

from rl_engine.rewards import (
    calculate_reward,
)

DESTINATION = 5


class NetworkEnv:

    def __init__(
        self,
        topology=None
    ):

        self.current_node = 0

        self.adjacency = (
            topology
            if topology is not None
            else adjacency_matrix
        )

        self.latency = (
            generate_latency()
        )

        self.loss = (
            generate_loss()
        )

    def reset(self):

        self.current_node = 0

        return self.current_node

    def get_valid_actions(
        self,
        state
    ):

        actions = []

        for node, connected in enumerate(
            self.adjacency[state]
        ):

            if connected == 1:
                actions.append(
                    node
                )

        return actions

    def step(
        self,
        action
    ):

        if action not in self.get_valid_actions(
            self.current_node
        ):

            raise ValueError(
                "Invalid move"
            )

        latency = self.latency[
            self.current_node
        ][action]

        loss = self.loss[
            self.current_node
        ][action]

        self.current_node = action

        done = (
            self.current_node
            == DESTINATION
        )

        reward = calculate_reward(
            latency,
            loss,
            done
        )

        info = {
            "latency": latency,
            "loss": loss,
        }

        return (
            self.current_node,
            reward,
            done,
            info,
        )
