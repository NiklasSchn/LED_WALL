import board
import neopixel
import numpy as np
import time


class WS2812_matrix:
    def __init__(self, size_y, size_x):
        self.size_x = size_x
        self.size_y = size_y

        # Calculate ranges beforehand so function update is faster
        if self.size_x % 2 == 0:
            self.range_x = range(1, self.size_x, 2)[::-1]
        else:
            self.range_x = range(0, self.size_x, 2)[::-1]
        self.range_y = range(0, self.size_y)
        self.range_y_inv = range(0, self.size_y)[::-1]

        # Initialize NeoPixel class
        self.pixels = neopixel.NeoPixel(board.D18, self.size_x * self.size_y, auto_write=False,
                                        pixel_order=neopixel.RGB)

    # Writes (0, 0, 0) an all LEDs
    def clear(self):
        for i in range(self.size_x * self.size_y):
            self.pixels[i] = (0, 0, 0)

        self.pixels.show()

    # 'data' is a 3 dimensional array where the first element represent the y position, the second the x position and
    # the third the RGB value (in that order)
    def update(self, data):
        # WS2812 data enters from the upper right corner and continues to the vertical line
        i = 0  # Points to the LEDs position

        # Loops through the columns of the matrix. It starts from the back
        for x in self.range_x:
            # Writes data (from top to bottom) of the column to the LEDs
            for y in self.range_y:
                self.pixels[i] = (data[y][x][0], data[y][x][1], data[y][x][2])
                i += 1
            if x >= 0:
                # Writes data (bottom up) of the next column to the LEDs
                x = x - 1
                for y in self.range_y_inv:
                    self.pixels[i] = (data[y][x][0], data[y][x][1], data[y][x][2])
                    i += 1

        # Writes the values on the LEDs
        self.pixels.show()

    # Writes single LED
    def write_single(self, y_pos, x_pos, color):
        y_pos = self.size_y - y_pos - 1
        x_pos = self.size_x - x_pos - 1
        print(y_pos, " , ", x_pos)
        i = x_pos * self.size_y
        if x_pos % 2 == 0:
            i += self.size_y - y_pos - 1
        else:
            i += y_pos

        print(i)

        self.pixels[i] = color
        self.pixels.show()


if __name__ == "__main__":
    # Dimensions of the display
    size_x = 20
    size_y = 15

    display = WS2812_matrix(size_y, size_x)  # Declares class
    display_data = np.zeros((size_y, size_x, 3), dtype=np.uint8)  # Declares class

    x = 0
    y = 0
    while True:
        # Sequence for testing
        if display_data[y][x][0] == 0:
            display_data[y][x] = (255, 255, 255)  # R,G,B
        else:
            display_data[y][x] = (0, 0, 0)
        print("Update")
        # display.update(display_data)  # Updates teh data to the LEDs
        display.write_single(0, 0, (255, 0, 0))
        time.sleep(0.1)

        # Sequence for testing
        x += 1
        if x == size_x:
            x = 0
            y += 1
            if y == size_y:
                y = 0
