def evaluate_health(
    latency,
    loss
):

    score = (
        latency
        +
        loss
    )

    if score < 15:

        return (
            "🟢 Healthy"
        )

    elif score < 25:

        return (
            "🟡 Congested"
        )

    return (
        "🔴 Critical"
    )
