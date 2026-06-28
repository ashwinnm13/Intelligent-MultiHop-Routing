import networkx as nx
import matplotlib.pyplot as plt

from rl_engine.topology import (
    adjacency_matrix,
)


def _topology_edges(topology):
    edges = []

    for start in range(len(topology)):
        for end in range(start + 1, len(topology[start])):
            if topology[start][end] == 1:
                edges.append((start, end))

    return edges


def draw_route(
    route,
    topology=None,
    title="Learned Route",
):

    graph = nx.Graph()

    if topology is None:
        topology = adjacency_matrix

    edges = _topology_edges(topology)

    graph.add_edges_from(
        edges
    )
    graph.add_nodes_from(range(len(topology)))

    positions = nx.spring_layout(
        graph,
        seed=7,
        k=0.8,
    )

    figure = plt.figure(
        figsize=(4.8, 3.2),
        dpi=120,
    )

    route_edges = list(
        zip(
            route[:-1],
            route[1:]
        )
    )

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=650,
        node_color="#dbeafe",
        edgecolors="#2563eb",
        linewidths=1.5,
    )

    nx.draw_networkx_labels(
        graph,
        positions,
        font_color="#111827",
        font_size=10,
        font_weight="bold",
    )

    nx.draw_networkx_edges(
        graph,
        positions,
        width=1.2,
        edge_color="#cbd5e1",
    )

    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=route_edges,
        width=3,
        edge_color="#0f172a",
    )

    plt.title(
        title
    )
    plt.axis(
        "off"
    )
    figure.tight_layout()

    return figure
