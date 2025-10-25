import pygame
from random import randint
from math import sin, cos

# --- Inicjalizacja ---
pygame.init()
pygame.font.init()

# --- Stałe ---
SCREEN_SIZE = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 5
FONT_SIZE = SCREEN_SIZE // 32
FONT = pygame.font.SysFont('courier', FONT_SIZE)
CLOCK = pygame.time.Clock()
DISPLAY = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

# --- Parametry lądowiska ---
mountain_count = 40
mountain_height = SCREEN_SIZE // 20
altitude_mod = SCREEN_SIZE // 5
mountain_x = []
mountain_y = []
phase_shift = randint(0, SCREEN_SIZE)

for i in range(mountain_count + 1):
    mountain_x.append(i * 10)
    raw_height = randint(-mountain_height, 0)
    terrain_shape = altitude_mod * (4 - sin((i + phase_shift) / 5))
    height = int(raw_height + terrain_shape) - FONT_SIZE
    mountain_y.append(height)

# --- Platforma lądowania ---
platform_length = 14
platform_index = 20
mountain_x.append(SCREEN_SIZE)
mountain_y.append(randint(SCREEN_SIZE - mountain_height, SCREEN_SIZE))
mountain_x[platform_index] = mountain_x[platform_index - 1] + platform_length
mountain_y[platform_index] = mountain_y[platform_index - 1]

# --- Stan gry ---
x = randint(10, SCREEN_SIZE - 10)
y = 10
vx = vy = 0
fuel = SCREEN_SIZE
radius = 5
game_state = ''
color_left = color_right = BLACK
color_glow = WHITE
wing_intensity = 255
pygame.key.set_repeat(100, 100)

# --- Główna pętla gry ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset gry
                x = randint(10, SCREEN_SIZE - 10)
                y = 10
                vx = vy = 0
                fuel = SCREEN_SIZE
                radius = 5
                game_state = ''
                color_glow = WHITE
                wing_intensity = 255

            if fuel > 0:
                if event.key == pygame.K_SPACE:
                    vy -= 2
                    fuel -= 5
                    color_left = color_right = WHITE
                elif event.key == pygame.K_LEFT:
                    vx += 2
                    fuel -= 5
                    color_left = WHITE
                elif event.key == pygame.K_RIGHT:
                    vx -= 2
                    fuel -= 5
                    color_right = WHITE

    # --- Fizyka ---
    if game_state == '' and (x < 0 or x > SCREEN_SIZE):
        x -= (abs(x) / x) * SCREEN_SIZE

    if game_state == '':
        vy += 1
        x = (10 * x + vx) / 10
        y = (10 * y + vy) / 10

    # --- Lądowanie ---
    if (y + 8) >= mountain_y[platform_index] and mountain_x[platform_index - 1] < x < mountain_x[platform_index] and vy < 30:
        game_state = 'LANDING'

    # --- Kolizje ---
    for i in range(mountain_count):
        if game_state == '' and mountain_x[i] <= x <= mountain_x[i + 1] and (mountain_y[i] <= y or mountain_y[i + 1] <= y):
            color_right = 1
            color_glow = BLACK
            game_state = 'CRASH'

    # --- Rysowanie ---
    DISPLAY.fill(BLACK)
    pygame.draw.line(DISPLAY, WHITE, (mountain_x[platform_index - 1], mountain_y[platform_index - 1]),
                     (mountain_x[platform_index], mountain_y[platform_index]), 3)

    if wing_intensity > 10 and game_state == 'CRASH':
        radius += 10
        wing_intensity -= 10

    for i in range(50):
        ax = sin(i / 8.)
        ay = cos(i / 8.)
        pygame.draw.line(DISPLAY, (wing_intensity, wing_intensity, wing_intensity),
                         (int(x + radius * ax), int(y + radius * ay)),
                         (int(x + radius * ax), int(y + radius * ay)))

    pygame.draw.line(DISPLAY, color_glow, (int(x + 3), int(y + 3)), (int(x + 4), int(y + 6)))
    pygame.draw.line(DISPLAY, color_glow, (int(x - 3), int(y + 3)), (int(x - 4), int(y + 6)))
    pygame.draw.line(DISPLAY, color_left, (int(x + 2), int(y + 5)), (int(x), int(y + 9)))
    pygame.draw.line(DISPLAY, color_right, (int(x - 2), int(y + 5)), (int(x), int(y + 9)))

    # --- HUD ---
    status = f'FUEL {fuel:3d}     ALT {SCREEN_SIZE - int(y):3d}     VERT SPD {int(vy):3d}     HORZ SPD {int(vx):3d}'
    surface = FONT.render(status, False, WHITE)
    DISPLAY.blit(surface, (0, SCREEN_SIZE - 12))
    color_left = color_right = BLACK

    # --- Góry ---
    for i in range(mountain_count):
        pygame.draw.line(DISPLAY, WHITE,
                         (int(mountain_x[i]), int(mountain_y[i])),
                         (int(mountain_x[i + 1]), int(mountain_y[i + 1])))

    # --- Komunikat ---
    surface = FONT.render(game_state, False, WHITE)
    DISPLAY.blit(surface, (SCREEN_SIZE // 3, SCREEN_SIZE // 2))

    pygame.display.flip()
    CLOCK.tick(FPS)

# --- Zakończenie ---
pygame.quit()