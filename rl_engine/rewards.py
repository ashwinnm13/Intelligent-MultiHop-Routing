def calculate_reward(
    latency,
    packet_loss,
    reached_destination=False
):

    reward = -(latency + packet_loss)

    if reached_destination:
        reward += 100

    return reward