from rl_engine.train import train

## get the best route from trained agent
def get_best_route(agent):

    state = 0

    route = [state]

    while state != 5:

        action = int(
            agent.q_table[state]
            .argmax()
        )

        route.append(
            action
        )

        state = action

    return route


if __name__ == "__main__":

    agent = train()

    route = (
        get_best_route(
            agent
        )
    )

    print(
        "\nBest Route:"
    )

    print(route)