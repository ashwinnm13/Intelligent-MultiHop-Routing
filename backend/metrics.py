from rl_engine.topology import (
    latency_matrix,
    loss_matrix,
)


def route_metrics(route):

    total_latency = 0
    total_loss = 0

    for i in range(len(route) - 1):

        start = route[i]
        end = route[i + 1]

        total_latency += int(latency_matrix[start][end])

        total_loss += int(loss_matrix[start][end])

    return {
        "latency": total_latency,
        "loss": total_loss,
        "hops": len(route) - 1,
    }


if __name__ == "__main__":

    sample = [0, 2, 4, 5]

    print(
        route_metrics(
            sample
        )
    )