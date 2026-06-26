from copy import deepcopy

from rl_engine.topology import (
    adjacency_matrix
)


def break_link(
    matrix,
    node_a,
    node_b
):

    updated = deepcopy(
        matrix
    )

    updated[
        node_a
    ][
        node_b
    ] = 0

    updated[
        node_b
    ][
        node_a
    ] = 0

    return updated


if __name__ == "__main__":

    failed = break_link(
        adjacency_matrix,
        2,
        4
    )

    print(
        failed
    )