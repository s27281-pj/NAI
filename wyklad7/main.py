import gymnasium as gym
import ale_py


# =======================
# ======== AGENT ========
# =======================
class Agent:
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation):
        return self.action_space.sample()

    def learn(self, *args):
        pass


# Rejestruje środowisko Atari (ALE) w Gymnasium
gym.register_envs(ale_py)


# Ładuje:
# - Emulator Atari (Arcade Learning Environment),
# - ROM Pacman jako obiekt pythonowy,
# - human - otwiera okno 60 klatek/s
# OPTYMALIZACJA UCZENIA - Zmien render_mode na None
# - rgb_array - do nagrywania, brak okna LIVE
env = gym.make("ALE/Pacman-v5", render_mode="rgb_array")


# Wrapper nagrywa wideo z rozgrywki, episode_trigger - określa które rozgrywki nagrywać
env = gym.wrappers.RecordVideo(
    env,
    episode_trigger=lambda num: num % 2 == 0,
    video_folder="recordings/",
    name_prefix="video",
)
# env.reset() - resetuje grę, ustawia pacmana na start, zwraca pierwszą klatkę
# env.step() - zwraca 1 klatkę RGB


# Reset the environment to generate the first observation
agent = Agent(env.action_space)

observation, info = env.reset(seed=42)

for _ in range(1000):
    action = agent.act(observation)
    observation, reward, terminated, truncated, info = env.step(action)

    agent.learn(observation, action, reward, terminated)

    if terminated or truncated:
        observation, info = env.reset()

env.close()
