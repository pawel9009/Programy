import pygame
import random
import time

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (233, 237, 5)
AQUA = (5, 237, 156)
PURPLE = (133, 5, 237)
COLORS = [RED, GREEN, BLUE, YELLOW, AQUA, PURPLE]

blockSize = 10
size = 100
WINDOW_HEIGHT = 350
WINDOW_WIDTH = 500

pygame.init()
pygame.display.set_caption('Mrówki Langtona')
font = pygame.font.SysFont("FFF Forward", 44)


def draw_text(text, font, color, surface, x, y):
    oobj = font.render(text, 1, color)
    text_rect = oobj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(oobj, text_rect)


class Cell:
    value: int = 0
    color = WHITE


class Menu:
    SCREEN = pygame.display.set_mode((500, 350))

    run_button = pygame.image.load('run.png')
    run_button_rect = run_button.get_rect(topleft=(WINDOW_WIDTH // 2 - 50, 300))

    left_button_ant = pygame.image.load('left.png')
    left_rect_ant = left_button_ant.get_rect(topleft=(WINDOW_WIDTH // 2 - 120, 100))

    right_button_ant = pygame.image.load('right.png')
    right_rect_ant = right_button_ant.get_rect(topleft=(WINDOW_WIDTH // 2 + 90, 100))

    left_button_step = left_button_ant.copy()
    left_rect_step = left_button_step.get_rect(topleft=(WINDOW_WIDTH // 2 - 120, 230))

    right_button_step = right_button_ant.copy()
    right_rect_step = right_button_step.get_rect(topleft=(WINDOW_WIDTH // 2 + 90, 230))

    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    def run_menu(self, n_ants=6, steps=13000, click=None):
        while True:
            self.SCREEN.fill((0, 0, 0))
            draw_text('Opcje', font, (255, 255, 255), self.SCREEN, WINDOW_WIDTH // 2 -50, 10)

            draw_text('Ilosc mrówek', font, (255, 255, 255), self.SCREEN, WINDOW_WIDTH // 3, 60)
            draw_text(f'{n_ants}', font, (255, 255, 255), self.SCREEN, WINDOW_WIDTH // 2, 110)

            draw_text('Ilosc kroków', font, (255, 255, 255), self.SCREEN, WINDOW_WIDTH // 3, 170)
            draw_text(f'{steps}', font, (255, 255, 255), self.SCREEN, WINDOW_WIDTH // 2 - 20, 240)

            mx, my = pygame.mouse.get_pos()

            if self.left_rect_ant.collidepoint((mx, my)):
                if click and n_ants > 1:
                    n_ants -= 1
            if self.right_rect_ant.collidepoint((mx, my)):
                if click and n_ants < 6:
                    n_ants += 1

            if self.left_rect_step.collidepoint((mx, my)):
                if click and steps > 1000:
                    steps -= 1000
            if self.right_rect_step.collidepoint((mx, my)):
                if click and steps < 20000:
                    steps += 1000

            if self.run_button_rect.collidepoint((mx, my)):
                if click:
                    board = Board(self.SCREEN, n_ants, steps)
                    board.run()

            self.SCREEN.blit(self.left_button_ant, [WINDOW_WIDTH // 2 - 120, 100])
            self.SCREEN.blit(self.right_button_ant, [WINDOW_WIDTH // 2 + 90, 100])

            self.SCREEN.blit(self.left_button_step, [WINDOW_WIDTH // 2 - 120, 230])
            self.SCREEN.blit(self.right_button_step, [WINDOW_WIDTH // 2 + 90, 230])

            self.SCREEN.blit(self.run_button, [WINDOW_WIDTH // 2 - 50, 300])

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                pygame.display.update()
                self.CLOCK.tick(60)


class Ant:
    def __init__(self, a, b, direction, color):
        self.a = a
        self.b = b
        self.dir = direction
        self.color = color

    def __str__(self):
        return f'{self.a} {self.b} {self.dir} {self.color}'


class Board:

    def __init__(self, Screan, ants, steps):
        self.ants = ants
        self.steps = steps
        self.SCREEN = Screan
        self.SCREEN = pygame.display.set_mode((blockSize * size, blockSize * size))

    grid = []
    mrowisko = []
    CLOCK = pygame.time.Clock()

    def create(self):
        for x in range(size):
            pom = []
            for y in range(size):
                pom.append(Cell())
            self.grid.append(pom)

        for color in range(self.ants):
            self.mrowisko.append(
                Ant(random.randint(10, size - 10), random.randint(10, size - 10), random.randint(0, 3), COLORS[color]))

    def run(self):
        self.create()
        for krok in range(self.steps + 1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            for ant in self.mrowisko:

                if ant.dir == 0:
                    if self.grid[ant.a][ant.b].value == 0:
                        self.grid[ant.a][ant.b].value = 1
                        self.grid[ant.a][ant.b].color = ant.color
                        ant.dir = 1
                        if ant.a > 0:
                            ant.a -= 1
                        else:
                            ant.a = size - 1
                    else:
                        self.grid[ant.a][ant.b].value = 0
                        self.grid[ant.a][ant.b].color = WHITE
                        ant.dir = 3
                        if ant.a < size - 1:
                            ant.a += 1
                        else:
                            ant.a = 0


                elif ant.dir == 1:
                    if self.grid[ant.a][ant.b].value == 0:
                        self.grid[ant.a][ant.b].color = ant.color
                        self.grid[ant.a][ant.b].value = 1
                        ant.dir = 2
                        if ant.b < size - 1:
                            ant.b += 1
                        else:
                            ant.b = 0
                    else:
                        self.grid[ant.a][ant.b].value = 0
                        self.grid[ant.a][ant.b].color = WHITE
                        ant.dir = 0
                        if ant.b > 0:
                            ant.b -= 1
                        else:
                            ant.b = size - 1


                elif ant.dir == 2:
                    if self.grid[ant.a][ant.b].value == 0:
                        self.grid[ant.a][ant.b].color = ant.color
                        self.grid[ant.a][ant.b].value = 1
                        ant.dir = 3
                        if ant.a < size - 1:
                            ant.a += 1
                        else:
                            ant.a = 0
                    else:
                        self.grid[ant.a][ant.b].value = 0
                        self.grid[ant.a][ant.b].color = WHITE
                        ant.dir = 1
                        if ant.a > 0:
                            ant.a -= 1
                        else:
                            ant.a = size - 1

                elif ant.dir == 3:
                    if self.grid[ant.a][ant.b].value == 0:
                        self.grid[ant.a][ant.b].color = ant.color
                        self.grid[ant.a][ant.b].value = 1
                        ant.dir = 0
                        if ant.b > 0:
                            ant.b -= 1
                        else:
                            ant.b = size - 1
                    else:
                        self.grid[ant.a][ant.b].value = 0
                        self.grid[ant.a][ant.b].color = WHITE
                        ant.dir = 2
                        if ant.b < size - 1:
                            ant.b += 1
                        else:
                            ant.b = 0

            self.draw()
            draw_text(f'Krok - {krok}', font, BLACK, self.SCREEN, 0, 10)
            pygame.display.update()
        time.sleep(10)
        pygame.quit()
        exit()

    def draw(self):
        for x in range(size):
            for y in range(size):
                if self.grid[x][y].value == 0:
                    rect = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
                    pygame.draw.rect(self.SCREEN, WHITE, rect)
                elif self.grid[x][y].value == 1:
                    rect = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
                    pygame.draw.rect(self.SCREEN, self.grid[x][y].color, rect)


if __name__ == '__main__':
    zad1 = Menu()
    zad1.run_menu()
