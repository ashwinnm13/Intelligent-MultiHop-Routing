from rl_engine.environment import NetworkEnv


def test_move():

    env = NetworkEnv()

    env.reset()

    state, reward, done, info = (env.step(1))

    assert state == 1