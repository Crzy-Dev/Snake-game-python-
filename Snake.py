import pygame
import random
import sys

pygame.init()

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
LIGHT_GREEN = (0, 255, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
BLUE = (80, 160, 255)

def draw_text(text, size, color, x, y, center=False):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

def select_level():
    options = ["Easy", "Medium", "Hard"]
    selected = 0

    while True:
        screen.fill(BLACK)
        draw_text("SELECT LEVEL", 48, WHITE, WIDTH//2, HEIGHT//4, True)

        for i, opt in enumerate(options):
            color = BLUE if i == selected else WHITE
            draw_text(opt, 36, color, WIDTH//2, HEIGHT//2 + i*50, True)

        draw_text("UP / DOWN  -  ENTER", 20, GRAY, WIDTH//2, HEIGHT-40, True)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % 3
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                elif e.key == pygame.K_RETURN:
                    return selected + 1  # 1,2,3

def spawn_food(snake, obstacles):
    while True:
        pos = [random.randint(0, GRID_WIDTH-1),
               random.randint(0, GRID_HEIGHT-1)]
        if pos not in snake and pos not in obstacles:
            return pos

def generate_obstacles(level, snake):
    if level == 1:
        return []

    count = level * 6
    obs = []
    while len(obs) < count:
        p = [random.randint(0, GRID_WIDTH-1),
             random.randint(0, GRID_HEIGHT-1)]
        if p not in obs and p not in snake:
            obs.append(p)
    return obs

def draw_snake(snake, direction):
    for i, s in enumerate(snake):
        color = GREEN if i % 2 == 0 else LIGHT_GREEN
        pygame.draw.rect(
            screen,
            color,
            (s[0]*CELL_SIZE, s[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

    head = snake[0]
    cx = head[0]*CELL_SIZE
    cy = head[1]*CELL_SIZE
    r = CELL_SIZE//4

    if direction == "RIGHT":
        eyes = [(cx+15, cy+6), (cx+15, cy+14)]
    elif direction == "LEFT":
        eyes = [(cx+5, cy+6), (cx+5, cy+14)]
    elif direction == "UP":
        eyes = [(cx+6, cy+5), (cx+14, cy+5)]
    else:
        eyes = [(cx+6, cy+15), (cx+14, cy+15)]

    for ex, ey in eyes:
        pygame.draw.circle(screen, WHITE, (ex, ey), r)
        pygame.draw.circle(screen, BLACK, (ex, ey), r//2)

def main():
    level = select_level()

    snake = [[10, 10], [9, 10], [8, 10]]
    direction = "RIGHT"
    change = direction

    obstacles = generate_obstacles(level, snake)
    food = spawn_food(snake, obstacles)
    score = 0

    speed = 8 + level*2

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: change = "UP"
                if e.key == pygame.K_DOWN: change = "DOWN"
                if e.key == pygame.K_LEFT: change = "LEFT"
                if e.key == pygame.K_RIGHT: change = "RIGHT"

        if change == "UP" and direction != "DOWN": direction = "UP"
        if change == "DOWN" and direction != "UP": direction = "DOWN"
        if change == "LEFT" and direction != "RIGHT": direction = "LEFT"
        if change == "RIGHT" and direction != "LEFT": direction = "RIGHT"

        head = snake[0].copy()
        if direction == "UP": head[1] -= 1
        if direction == "DOWN": head[1] += 1
        if direction == "LEFT": head[0] -= 1
        if direction == "RIGHT": head[0] += 1

        if (head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT or
            head in snake or
            head in obstacles):
            break

        snake.insert(0, head)

        if head == food:
            score += 1
            food = spawn_food(snake, obstacles)
        else:
            snake.pop()

        screen.fill(BLACK)
        draw_snake(snake, direction)

        pygame.draw.rect(
            screen, RED,
            (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

        for o in obstacles:
            pygame.draw.rect(
                screen, GRAY,
                (o[0]*CELL_SIZE, o[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

        draw_text(f"Score: {score}", 24, WHITE, 10, 10)

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()
    sys.exit()

main()