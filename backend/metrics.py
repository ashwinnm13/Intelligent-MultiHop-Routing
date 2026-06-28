from rl_engine.topology import (
    latency_matrix,
    loss_matrix,
)


def telemetry_cost_matrices(telemetry=None):
    if telemetry is None:
        return latency_matrix, loss_matrix

    latency = float(
        telemetry.get(
            "latency",
            0
        )
    )
    loss = float(
        telemetry.get(
            "loss",
            0
        )
    )
    bandwidth = max(
        1.0,
        float(
            telemetry.get(
                "bandwidth",
                1
            )
        )
    )

    latency_pressure = max(
        1.0,
        latency / 20.0
    )
    bandwidth_pressure = max(
        1.0,
        50.0 / bandwidth
    )
    loss_pressure = max(
        1.0,
        loss / 3.0
    )

    adjusted_latency = (
        latency_matrix
        * latency_pressure
        * bandwidth_pressure
    ).round()

    adjusted_loss = (
        loss_matrix
        * loss_pressure
    ).round()

    return adjusted_latency, adjusted_loss


def route_metrics(route, telemetry=None):

    if telemetry is not None:
        latency = float(
            telemetry.get(
                "latency",
                0
            )
        )
        loss = float(
            telemetry.get(
                "loss",
                0
            )
        )
        hops = len(route) - 1
        estimated_reward = round(
            100
            -
            latency
            -
            (
                loss
                *
                2
            )
            -
            hops,
            2
        )

        return {
            "latency": latency,
            "loss": loss,
            "hops": hops,
            "reward": estimated_reward,
        }

    total_latency = 0
    total_loss = 0

    for i in range(len(route) - 1):

        start = route[i]
        end = route[i + 1]

        total_latency += int(latency_matrix[start][end])

        total_loss += int(loss_matrix[start][end])

    estimated_reward = (
        100
        -
        total_latency
        -
        (
            total_loss
            *
            2
        )
    )

    return {
        "latency": total_latency,
        "loss": total_loss,
        "hops": len(route) - 1,
        "reward": estimated_reward,
    }


if __name__ == "__main__":

    sample = [0, 2, 4, 5]

    print(
        route_metrics(
            sample
        )
    )
