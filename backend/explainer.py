def explain_route(
    metrics
):

    latency = metrics[
        "latency"
    ]

    loss = metrics[
        "loss"
    ]

    if latency < 15:

        return (
            "Selected for lower latency"
        )

    if loss < 5:

        return (
            "Selected to reduce packet loss"
        )

    return (
        "Selected for balanced routing"
    )
