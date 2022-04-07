import pygame
import random
import time
import numpy as np

class PygameDisplay:
    def __init__(self, size_y, size_x, window_width=640):
        self.size_x = size_x
        self.size_y = size_y
        self.window_width = window_width
        self.blockSize = round(window_width / size_x)
        self.window_height = self.blockSize*size_y

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))

        self.range_x = list(map(lambda x: x + 1, range(0, self.window_width, self.blockSize)))
        self.range_y = list(map(lambda x: x + 1, range(0, self.window_height, self.blockSize)))

        self.blockSize = self.blockSize - 2

        for x_pos in self.range_x:
            for y_pos in self.range_y:
                rect = pygame.Rect(x_pos, y_pos, self.blockSize, self.blockSize)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 0)

        self.start_ticks = pygame.time.get_ticks()

    # 'data' is a 3 dimensional array where the first element represent the y position, the second the x position and
    # the third the RGB value (in that order)
    def update(self, data):
        for x, x_pos in enumerate(self.range_x):
            for y, y_pos in enumerate(self.range_y):
                rect = pygame.Rect(x_pos, y_pos, self.blockSize, self.blockSize)
                pygame.draw.rect(self.screen, data[y][x], rect, 0)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == "__main__":
    size_x = 20
    size_y = 15

    display = PygameDisplay(size_y, size_x)

    display_data = np.zeros((size_y, size_x, 3), dtype=np.uint8)

    x = 0
    y = 0
    while True:
        if display_data[y][x][0] == 0:
            display_data[y][x][0] = 255
        else:
            display_data[y][x][0] = 0
        print("Update")
        display.update(display_data)
        time.sleep(0.5)
        x += 1
        if x == size_x:
            x = 0
            y += 1
            if y == size_y:
                y = 0

