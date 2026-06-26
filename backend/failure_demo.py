from backend.chaos_router import break_link

from rl_engine.topology import (
    adjacency_matrix
)

from rl_engine.train import train

from rl_engine.inference import (
    get_best_route
)


def run():

    print("\n=== ORIGINAL NETWORK ===")

    agent = train()

    original = get_best_route(
        agent
    )

    print(
        "Route:",
        original
    )

    print(
        "\n=== BREAKING LINK 2 ↔ 4 ==="
    )

    failed = break_link(
        adjacency_matrix,
        2,
        4
    )

    agent = train(
        failed
    )

    updated = get_best_route(
        agent
    )

    print(
        "New Route:",
        updated
    )


if __name__ == "__main__":
    run()