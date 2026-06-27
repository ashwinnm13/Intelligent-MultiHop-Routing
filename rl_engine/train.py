from rl_engine.environment import NetworkEnv
from rl_engine.q_learning import QLearning


def train(
    topology=None,
    episodes=300
):

    env = NetworkEnv(
        topology
    )

    agent = QLearning()

    rewards = []

    for _ in range(
        episodes
    ):

        state = env.reset()

        done = False

        total_reward = 0

        while not done:

            action = (
                agent.choose_action(
                    state,
                    env.get_valid_actions(
                        state
                    )
                )
            )

            (
                next_state,
                reward,
                done,
                _
            ) = env.step(
                action
            )

            agent.update(
                state,
                action,
                reward,
                next_state
            )

            state = (
                next_state
            )

            total_reward += (
                reward
            )

        rewards.append(
            total_reward
        )

    return (
        agent,
        rewards
    )