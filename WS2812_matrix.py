import board
import neopixel
import numpy as np
import time


class WS2812_matrix:
    def __init__(self, size_y, size_x):
        self.size_x = size_x
        self.size_y = size_y

        if self.size_x % 2 == 0:
            self.range_x = range(1, self.size_x, 2)[::-1]
        else:
            self.range_x = range(0, self.size_x, 2)[::-1]
        self.range_y = range(0, self.size_y)
        self.range_y_inv = range(0, self.size_y)[::-1]
        ORDER = neopixel.RGB
        self.pixels = neopixel.NeoPixel(board.D18, self.size_x*self.size_y, auto_write=False, pixel_order=ORDER)

    # 'data' is a 3 dimensional array where the first element represent the y position, the second the x position and
    # the third the RGB value (in that order)
    def update(self, data):
        # WS2812 data enters from the upper right corner and continues to the vertical line
        i = 0
        for x in self.range_x:
            for y in self.range_y:
                self.pixels[i] = (data[y][x][0], data[y][x][1], data[y][x][2])
                i += 1
            if x >= 0:
                x = x - 1
                for y in self.range_y_inv:
                    self.pixels[i] = (data[y][x][0], data[y][x][1], data[y][x][2])
                    i += 1

        self.pixels.show()


if __name__ == "__main__":
    size_x = 20
    size_y = 15

    display = WS2812_matrix(size_y, size_x)

    display_data = np.zeros((size_y, size_x, 3), dtype=np.uint8)

    x = 0
    y = 0
    while True:
        if display_data[y][x][0] == 0:
            display_data[y][x] = (255,255,255) #g,r,b
        else:
            display_data[y][x] = (0,0,0)
        print("Update")
        display.update(display_data)
        #time.sleep(0.1)
        x += 1
        if x == size_x:
            x = 0
            y += 1
            if y == size_y:
                y = 0
