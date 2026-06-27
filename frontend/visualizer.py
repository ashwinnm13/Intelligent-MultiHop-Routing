import networkx as nx
import matplotlib.pyplot as plt


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

    graph.add_edges_from(
        edges
    )

    positions = nx.spring_layout(
        graph,
        seed=42
    )

    figure = plt.figure(
        figsize=(4, 3)
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
        with_labels=True,
        node_size=1200,
    )

    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=route_edges,
        width=3,
    )

    plt.title(
        "Learned Route"
    )

    return figure