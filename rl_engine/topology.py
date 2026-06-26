import numpy as np

NUM_NODES = 6


adjacency_matrix = np.array([
    [0,1,1,0,0,0],
    [1,0,0,1,1,0],
    [1,0,0,0,1,0],
    [0,1,0,0,0,1],
    [0,1,1,0,0,1],
    [0,0,0,1,1,0]
])


latency_matrix = np.array([
    [0,5,3,0,0,0],
    [5,0,0,4,6,0],
    [3,0,0,0,5,0],
    [0,4,0,0,0,2],
    [0,6,5,0,0,3],
    [0,0,0,2,3,0]
])


loss_matrix = np.array([
    [0,1,2,0,0,0],
    [1,0,0,1,3,0],
    [2,0,0,0,2,0],
    [0,1,0,0,0,1],
    [0,3,2,0,0,1],
    [0,0,0,1,1,0]
])


def print_topology():

    print("\nAdjacency Matrix")
    print(adjacency_matrix)

    print("\nLatency Matrix (ms)")
    print(latency_matrix)

    print("\nPacket Loss Matrix (%)")
    print(loss_matrix)


if __name__ == "__main__":
    print_topology()