import pygame
import sys
import open_cv_eyes
import random
import time
from threading import Thread
import os


class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = (0, 0)
        self.color = (255, 0, 0)
        # Special thanks to YouTubers Mini - Cafetos and Knivens Beast for raising this issue!
        # Code adjustment courtesy of YouTuber Elija de Hoog
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self, surface):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * gridsize)) % screen_width), (cur[1] + (y * gridsize)) % screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        elif self.positions[0][0] == 0.0 and x == -1:
            self.reset()
        elif self.positions[0][0] == 460.0 and x == 1:
            self.reset()
        elif self.positions[0][1] == 0.0 and y == -1:
            self.reset()
        elif self.positions[0][1] == 460.0 and y == 1:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = (0, 0)
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((int(p[0]), int(p[1])), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (0, 0, 0), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if open_cv_eyes.direction == "DOWN":
                    print("Oh yeah")
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)


class Food():
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (223, 163, 49), r, 1)


def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (255, 255, 255), r)
            else:
                rr = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (255, 255, 255), rr)


def exec_file():
    os.system('pythonw open_cv_eyes.py')


screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width / gridsize
grid_height = screen_height / gridsize

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace", 16)

    while (True):
        clock.tick(1)
        snake.handle_keys()
        drawGrid(surface)
        snake.move(surface)
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = myfont.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update()
        time.sleep(1)


Thread(target=main(), args=("2",)).start()
