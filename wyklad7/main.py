"""
===============================================
Atari Pacman Reinforcement Learning Environment
===============================================

Autor: Roland i Cyprian
Data: 2026-01-23
Opis:
    Przykładowa implementacja agenta RL (Random) dla gry Atari Pacman
    przy użyciu bibliotek Gymnasium i ALE (Arcade Learning Environment).
"""

import gymnasium as gym
import ale_py
import cv2
import numpy as np
from gymnasium.wrappers import RecordVideo


# ===============================
# ======== PREPROCESSING ========
# ===============================
class AtariPreprocess(gym.ObservationWrapper):
    def observation(self, obs):
        obs = cv2.cvtColor(obs, cv2.COLOR_RGB2GRAY)
        obs = cv2.resize(obs, (84, 84))
        obs = obs.astype(np.float32) / 255.0
        return obs



# =======================
# ======== AGENT ========
# =======================
class Agent:
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation):
        # Losowa akcja - ZASTĄPIC
        return self.action_space.sample()

    def learn(self, *args):
        # PLACEHOLDER
        pass



# =============================
# ======== ENVIRONMENT ========
# =============================
# Rejestruje środowisko Atari (ALE) w Gymnasium
gym.register_envs(ale_py)
# Ładuje:
# - Emulator Atari (Arcade Learning Environment),
# - ROM Pacman jako obiekt pythonowy,
# - human - otwiera okno 60 klatek/s
# OPTYMALIZACJA UCZENIA - Zmien render_mode na None
# - rgb_array - do nagrywania, brak okna LIVE
# - obs_type - domyślnie RGB
# OPTYMALIZACJA UCZENIA - Zmien obs_type na grayscale
env = gym.make(
    "ALE/Pacman-v5",
    render_mode="rgb_array",
    obs_type="rgb"
)
# Wyświetla możliwe i przykładowe akcje
# print(f"Action space: {env.action_space}")  # Discrete(2) - left or right
# print(f"Sample action: {env.action_space.sample()}")  # 0 or 1

# Box observation space (continuous values)
# print(f"Observation space: {env.observation_space}")  # Box with 4 values
# Box([-4.8, -inf, -0.418, -inf], [4.8, inf, 0.418, inf])
# print(f"Sample observation: {env.observation_space.sample()}")  # Random valid observation



# =================================
# ======== VIDEO RECORDING ========
# =================================
# Wrapper nagrywa wideo z rozgrywki, episode_trigger - określa które rozgrywki nagrywać
env = RecordVideo(
    AtariPreprocess(env),
    episode_trigger=lambda num: num % 2 == 0,
    video_folder="recordings/",
    name_prefix="video",
)
# env.reset() - resetuje grę, ustawia pacmana na start, zwraca pierwszą klatkę
# env.step() - zwraca 1 klatkę RGB

print(f"Videos will be saved to: recordings/")

# Reset the environment to generate the first observation
agent = Agent(env.action_space)


# =================================
# ======== SINGLE EPISODE =========
# =================================
num_episodes = 100


for episode in range(num_episodes):
    # Resetuje środowisko dla nowego epizodu
    observation, info = env.reset(seed=42)
    episode_score = 0
    episode_over = False

    while not episode_over:
        # Wybiera akcję na podstawie agenta
        action = agent.act(observation)
        # Wykonuje akcje i sprawdza co się zadzieje
        observation, reward, terminated, truncated, info = env.step(action)
        episode_score += reward
        agent.learn(observation, action, reward, terminated)

        episode_over = terminated or truncated

    print(f"Episode {episode + 1} finished | Score: {episode_score}")

env.close()
