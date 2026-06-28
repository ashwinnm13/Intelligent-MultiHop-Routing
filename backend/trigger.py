def should_retrain(
    telemetry
):

    latency = (
        telemetry[
            "latency"
        ]
    )

    loss = (
        telemetry[
            "loss"
        ]
    )

    return (

        latency > 18

        or

        loss > 6

    )
