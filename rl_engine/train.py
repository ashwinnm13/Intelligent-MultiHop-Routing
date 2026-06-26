from rl_engine.environment import NetworkEnv
from rl_engine.q_learning import QLearningAgent


EPISODES = 100


def train(topology=None):

    env = NetworkEnv(topology)

    agent = QLearningAgent()

    for episode in range(EPISODES):

        state = env.reset()

        done = False

        while not done:

            valid_actions = (
                env.get_valid_actions(
                    state
                )
            )

            action = (
                agent.choose_action(
                    state,
                    valid_actions
                )
            )

            (
                next_state,
                reward,
                done,
                info,
            ) = env.step(action)

            agent.update(
                state,
                action,
                reward,
                next_state,
            )

            state = next_state

    return agent


if __name__ == "__main__":

    trained_agent = train()

    print("\nQ Table:\n")

    print(
        trained_agent.q_table
    )