import gymnasium as gym
import ale_py
import time
import random
import pygame

# =====================================================
# Rejestracja ALE
# =====================================================
gym.register_envs(ale_py)

# =====================================================
# Wrapper ograniczający akcje Pac-Mana
# =====================================================
class PacmanActionWrapper(gym.ActionWrapper):
    """
    Ogranicza akcje Pac-Mana do 5 podstawowych:
    0 - NOOP
    1 - UP
    2 - RIGHT
    3 - LEFT
    4 - DOWN
    """
    def __init__(self, env):
        super().__init__(env)
        self.valid_actions = [0, 1, 2, 3, 4]
        self.action_space = gym.spaces.Discrete(len(self.valid_actions))

    def action(self, act):
        return self.valid_actions[act]


# =====================================================
# Sterowanie MANUALNE (klawiatura)
# =====================================================
def manual_controller():
    pygame.init()
    pygame.display.set_mode((1, 1))

    current_action = 0  # NOOP na start
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    current_action = 1
                elif event.key == pygame.K_RIGHT:
                    current_action = 2
                elif event.key == pygame.K_LEFT:
                    current_action = 3
                elif event.key == pygame.K_DOWN:
                    current_action = 4

        yield current_action

    pygame.quit()
    yield None


# =====================================================
# Sterowanie AUTOMATYCZNE (BOT / RL placeholder)
# =====================================================
def bot_controller():
    while True:
        yield random.randint(0, 3)

# =====================================================
# GŁÓWNA PĘTLA GRY
# =====================================================
def run_game(controller):
    env = gym.make("ALE/Pacman-v5", render_mode="human")
    env = PacmanActionWrapper(env)

    obs, info = env.reset()

    for action in controller:
        if action is None:
            break

        obs, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            time.sleep(1)
            obs, info = env.reset()

        time.sleep(0.03)

    env.close()

# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    print("Wybierz tryb sterowania:")
    print("1 - Sterowanie manualne (klawiatura)")
    print("2 - Sterowanie automatyczne (bot / RL)")

    choice = input("Twój wybór (1/2): ").strip()

    if choice == "1":
        print("Tryb MANUALNY: użyj strzałek, ESC aby wyjść")
        controller = manual_controller()
    elif choice == "2":
        print("Tryb AUTOMATYCZNY: bot steruje Pac-Manem")
        controller = bot_controller()
    else:
        print("Niepoprawny wybór")
        exit(0)

    run_game(controller)
