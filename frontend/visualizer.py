import networkx as nx
import matplotlib.pyplot as plt

from rl_engine.inference import (
    train,
    get_best_route,
)


def draw_route(route):

    graph = nx.Graph()

    edges = [
        (0, 1),
        (0, 2),
        (1, 3),
        (1, 4),
        (2, 4),
        (3, 5),
        (4, 5),
    ]

    graph.add_edges_from(edges)

    positions = nx.spring_layout(
        graph,
        seed=42
    )

    route_edges = list(
        zip(
            route[:-1],
            route[1:]
        )
    )

    nx.draw(
        graph,
        positions,
        with_labels=True
    )

    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=route_edges,
        width=4
    )

    plt.title(
        "Learned Route"
    )

    plt.show()


if __name__ == "__main__":

    agent = train()

    route = (
        get_best_route(
            agent
        )
    )

    draw_route(route)