from backend.metrics import (
    route_metrics,
)


def test_route_metrics_use_live_telemetry_values():
    telemetry = {
        "latency": 15.75,
        "loss": 1,
        "bandwidth": 84.25,
    }

    metrics = route_metrics(
        [
            0,
            2,
            4,
            5,
        ],
        telemetry,
    )

    assert metrics["latency"] == 15.75
    assert metrics["loss"] == 1
    assert metrics["hops"] == 3
    assert metrics["reward"] == 79.25
