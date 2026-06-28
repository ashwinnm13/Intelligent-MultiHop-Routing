from rl_engine.topology import (
    adjacency_matrix,
)

from backend.metrics import (
    telemetry_cost_matrices,
)


DESTINATION = 5


class NetworkEnv:

    def __init__(
        self,
        topology=None,
        telemetry=None,
    ):

        self.current_node = 0

        self.adjacency = (
            topology
            if topology is not None
            else adjacency_matrix
        )

        self.latency, self.loss = (
            telemetry_cost_matrices(
                telemetry
            )
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

        latency = int(
            self.latency[
                self.current_node
            ][
                action
            ]
        )

        loss = int(
            self.loss[
                self.current_node
            ][
                action
            ]
        )

        self.current_node = action

        done = (
            self.current_node
            == DESTINATION
        )

        reward = (

            100

            -

            latency

            -

            (

                loss
                *
                2

            )

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
