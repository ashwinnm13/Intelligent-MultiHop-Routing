from rl_engine.q_learning import (
    QLearningAgent
)


def test_update():

    agent = QLearningAgent()

    agent.update(
        state=0,
        action=1,
        reward=10,
        next_state=1
    )

    assert (
        agent.q_table[0][1]
        > 0
    )