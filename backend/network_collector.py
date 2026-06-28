from ping3 import ping


def collect_network():

    latency = ping(
        "8.8.8.8",
        timeout=2
    )

    if latency is None:

        latency = 100

    else:

        latency = round(
            latency * 1000,
            2
        )

    download = max(
        1,
        round(
            100 - latency,
            2
        )
    )

    loss = max(

        0,

        round(
            latency / 20
        )
    )

    return {

        "latency":
        latency,

        "loss":
        loss,

        "bandwidth":
        download

    }
