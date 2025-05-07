import pygame
import random
import sys

# Configuración
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 21, 21  
CELL_SIZE = WIDTH // COLS

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
DARK_GREY = (100, 100, 100)
BLUE = (50, 150, 255)
GREEN = (0, 255, 0) 
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))
pygame.display.set_caption("Laberinto con Backtracking Animado")
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

# Variables globales
maze = []
visited = []
solution_path = []
wrong_path = []
restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT + 10, 100, 30)


def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (y, x) in solution_path:
                color = BLUE
            elif (y, x) in wrong_path:
                color = DARK_GREY
            elif visited[y][x]:
                color = YELLOW
            else:
                color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GREY, rect, 1)

    # Inicio y fin
    pygame.draw.rect(screen, GREEN, (0, 0, CELL_SIZE, CELL_SIZE))  # Inicio
    pygame.draw.rect(screen, RED, ((COLS - 1) * CELL_SIZE, (ROWS - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Fin

    # Botón
    pygame.draw.rect(screen, GREY, restart_button)
    text = font.render("Reiniciar", True, BLACK)
    screen.blit(text, (restart_button.x + 10, restart_button.y + 5))

    pygame.display.flip()


def generate_maze(x=0, y=0, animate=False):
    maze[y][x] = 0
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
            maze[y + dy // 2][x + dx // 2] = 0  # Eliminar la pared intermedia
            maze[ny][nx] = 0  # Marcar la celda destino como pasillo
            if animate:
                draw_maze()
                pygame.time.wait(10)
            generate_maze(nx, ny, animate)


def solve_maze(x=0, y=0):
    pygame.event.pump()
    if not (0 <= x < COLS and 0 <= y < ROWS):
        return False
    if visited[y][x] or maze[y][x] == 1:
        return False

    visited[y][x] = True
    solution_path.append((y, x))
    draw_maze()
    pygame.time.wait(20)

    if (x, y) == (COLS - 1, ROWS - 1):
        return True

    if (solve_maze(x + 1, y) or solve_maze(x - 1, y) or
        solve_maze(x, y + 1) or solve_maze(x, y - 1)):
        return True

    solution_path.pop()
    wrong_path.append((y, x))
    draw_maze()
    pygame.time.wait(20)
    return False


def reset_maze():
    global maze, visited, solution_path, wrong_path
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    solution_path = []
    wrong_path = []

    generate_maze(0, 0, animate=True)
    maze[ROWS - 1][COLS - 1] = 0  # Asegura que la salida sea posible

    if not solve_maze():
        print("No se encontró solución al laberinto generado.")


def main():
    reset_maze()
    running = True
    while running:
        clock.tick(60)
        draw_maze()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    reset_maze()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
