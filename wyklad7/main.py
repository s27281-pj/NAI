"""
===============================================
Atari Pacman Reinforcement Learning Environment
===============================================
Autor: Roland i Cyprian (Poprawione)
Opis: Implementacja z widocznym oknem gry (render_mode="human")
"""

import gymnasium as gym
import ale_py
import cv2
import numpy as np
import time

# ===============================
# ======== PREPROCESSING ========
# ===============================
class AtariPreprocess(gym.ObservationWrapper):
    def observation(self, obs):
        # Konwersja na skalę szarości i zmiana rozmiaru (84x84)
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
        # Na razie wybiera losowe ruchy
        return self.action_space.sample()

    def learn(self, *args):
        pass

# =============================
# ======== ENVIRONMENT ========
# =============================
# Rejestracja środowisk Atari
gym.register_envs(ale_py)

# UWAGA: render_mode="human" otwiera okno gry.
# W tym trybie nie można używać RecordVideo!
env = gym.make(
    "ALE/Pacman-v5",
    render_mode="human",
    obs_type="rgb"
)

# Nakładamy preprocessing na środowisko
env = AtariPreprocess(env)

# Jeśli chcesz nagrywać wideo, musisz:
# 1. Zmienić render_mode powyżej na "rgb_array"
# 2. Odkomentować poniższy blok:
"""
from gymnasium.wrappers import RecordVideo
env = RecordVideo(
    env,
    episode_trigger=lambda num: num % 5 == 0,
    video_folder="recordings/",
    name_prefix="video",
)
"""

agent = Agent(env.action_space)
num_episodes = 5

# =================================
# ======== GŁÓWNA PĘTLA  ==========
# =================================
for episode in range(num_episodes):
    observation, info = env.reset(seed=42)
    episode_score = 0
    episode_over = False

    print(f"Rozpoczynam epizod {episode + 1}...")

    while not episode_over:
        # Agent podejmuje decyzję
        action = agent.act(observation)

        # Wykonanie ruchu w środowisku
        observation, reward, terminated, truncated, info = env.step(action)
        episode_score += reward

        # Opcjonalne: zwolnienie animacji, żeby dało się coś zauważyć
        # time.sleep(0.01)

        episode_over = terminated or truncated

    print(f"Epizod {episode + 1} zakończony | Wynik: {episode_score}")

# Zamknięcie środowiska i okna
env.close()
print("Koniec symulacji.")

#zmiana