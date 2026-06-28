from collections import deque

import numpy as np

from rl_engine.topology import (
    adjacency_matrix,
)

from rl_engine.train import train


def _valid_actions(topology, state, visited):
    return [
        node
        for node, connected in enumerate(topology[state])
        if connected == 1 and node not in visited
    ]


def _fallback_route(topology, source=0, destination=5):
    queue = deque([(source, [source])])
    visited = {source}

    while queue:
        state, route = queue.popleft()

        if state == destination:
            return route

        for node, connected in enumerate(topology[state]):
            if connected == 1 and node not in visited:
                visited.add(node)
                queue.append((node, route + [node]))

    return [source]

## get the best route from trained agent
def get_best_route(agent, topology=None):

    if topology is None:
        topology = adjacency_matrix

    state = 0

    route = [state]

    visited = {state}

    while state != 5:

        valid_actions = _valid_actions(
            topology,
            state,
            visited,
        )

        if not valid_actions:

            return _fallback_route(
                topology
            )

        q_values = agent.q_table[
            state,
            valid_actions
        ]

        action = int(
            valid_actions[
                int(
                    np.argmax(
                        q_values
                    )
                )
            ]
        )

        route.append(
            action
        )

        visited.add(action)

        state = action

    return route


if __name__ == "__main__":

    agent, _ = train()

    route = (
        get_best_route(
            agent
        )
    )

    print(
        "\nBest Route:"
    )

    print(route)
