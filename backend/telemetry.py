import random


def generate_metrics():

    return {

        "latency":
        random.randint(
            5,
            25
        ),

        "loss":
        random.randint(
            1,
            10
        ),

        "traffic":
        random.randint(
            20,
            90
        )
    }
