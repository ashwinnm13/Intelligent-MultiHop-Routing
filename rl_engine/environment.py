from rl_engine.topology import (
    adjacency_matrix,
    latency_matrix,
    loss_matrix,
)

DESTINATION = 5


class NetworkEnv:

    def __init__(self):

        self.current_node = 0

    def reset(self):

        self.current_node = 0
        return self.current_node

    def get_valid_actions(self, state):

        actions = []

        for node, connected in enumerate(adjacency_matrix[state] ):

            if connected == 1:
                actions.append(node)

        return actions

    def step(self, action):

        if action not in self.get_valid_actions( self.current_node):
            raise ValueError("Invalid move")

        latency = latency_matrix[self.current_node][action]

        loss = loss_matrix[self.current_node][action]

        reward = -(latency + loss)

        self.current_node = action

        done = ( self.current_node == DESTINATION)

        if done:
            reward += 100

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