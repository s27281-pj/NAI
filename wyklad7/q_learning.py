"""
Demo of the Q-learning algorithm using the Frozen Lake environment from OpenAI Gym.
To be verified if reaches the goal.
"""

import gymnasium as gym
import numpy as np

# Initialize the Frozen Lake environment
env = gym.make('FrozenLake-v1', is_slippery=True, render_mode="human")

# Parameters
num_states = env.observation_space.n
num_actions = env.action_space.n
q_table = np.zeros((num_states, num_actions))
learning_rate = 0.8
discount_factor = 0.95
epsilon = 1.0
epsilon_decay = 0.995
min_epsilon = 0.01
max_steps = 100

# Q-learning algorithm
for episode in range(1000):
    state, _ = env.reset()  # Gymnasium returns a tuple (state, info)
    done = False
    step = 0

    while not done and step < max_steps:
        # Choose action using epsilon-greedy policy
        if np.random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(q_table[state, :])

        # Take action and observe the result
        next_state, reward, done, _, _ = env.step(action)

        # Update Q-value
        q_table[state, action] = q_table[state, action] + learning_rate * (
            reward + discount_factor * np.max(q_table[next_state, :]) - q_table[state, action]
        )

        state = next_state
        step += 1
        print("current reward", reward)

    # Decay epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

# Test the trained agent
state, _ = env.reset()
done = False
steps = 0
print("Trained agent's performance:")
while not done and steps < max_steps:
    action = np.argmax(q_table[state, :])
    state, _, done, _, _ = env.step(action)
    env.render()
    steps += 1

env.close()