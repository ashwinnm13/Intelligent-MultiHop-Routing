import numpy as np


def generate_latency():

    base = np.array([

        [0,5,3,0,0,0],
        [5,0,0,4,6,0],
        [3,0,0,0,5,0],
        [0,4,0,0,0,2],
        [0,6,5,0,0,3],
        [0,0,0,2,3,0]

    ])

    noise = np.random.randint(
        -2,
        3,
        (6,6)
    )

    result = base + noise

    result[result < 0] = 0

    return result


def generate_loss():

    base = np.array([

        [0,1,2,0,0,0],
        [1,0,0,1,3,0],
        [2,0,0,0,2,0],
        [0,1,0,0,0,1],
        [0,3,2,0,0,1],
        [0,0,0,1,1,0]

    ])

    noise = np.random.randint(
        0,
        3,
        (6,6)
    )

    return base + noise