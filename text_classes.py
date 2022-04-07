from functions import text_to_rgb, blit
import time
import numpy as np
from datetime import datetime
#from WS2812_matrix import WS2812_matrix
from PIL import Image
from pygame_matrix import PygameDisplay


class MovingText:
    def __init__(self, text, size_x, speed, wait, fill):
        self.size_x = size_x
        self.pos = size_x - 1
        self.speed = speed/1000
        self.wait = wait/1000
        self.last_update = time.time()
        self.done = False

        self.rgb_text = text_to_rgb(text, fill=fill)
        self.out = np.zeros((9, self.size_x, 3), dtype=np.uint8)

    def restart(self):
        self.pos = self.size_x - 1
        self.last_update = time.time()
        self.done = False

    def update(self):
        if self.pos > -self.rgb_text.shape[1]:
            if time.time() - self.last_update > self.speed:
                self.last_update = time.time()
                self.out = np.zeros((9, self.size_x, 3), dtype=np.uint8)
                self.out = blit(self.out, self.rgb_text, (0, self.pos))
                self.pos -= 1

                return self.out
            else:
                return None
        else:
            self.done = True
            if time.time() - self.last_update > self.wait:
                self.pos = self.size_x - 1
                self.done = False
            return None


class ShowTime:
    def __init__(self, fill):
        self.fill = fill
        self.time_now = datetime.now()
        self.last_second = self.time_now.second
        self.rst = True
        self.out = np.zeros((11, 13, 3), dtype=np.uint8)
        self.two_points = np.zeros((3, 1, 3), dtype=np.uint8)
        self.two_points[0][0] = fill
        self.two_points[2][0] = fill
        self.two_points_active = False
        pass

    def restart(self):
        self.rst = True

    def update(self):
        self.time_now = datetime.now()
        if self.time_now.second != self.last_second:
            self.last_second = self.time_now.second

            if self.time_now.second == 0 or self.rst:
                self.rst = False
                arr_hour = text_to_rgb(str(self.time_now.hour).zfill(2), fill=self.fill)
                arr_min = text_to_rgb(str(self.time_now.minute).zfill(2), fill=self.fill)
                self.out = blit(self.out, arr_min, (2, 2))
                self.out = blit(self.out, arr_hour, (-4, 2))

            if not self.two_points_active:
                self.two_points_active = True
                self.out = blit(self.out, self.two_points, (7, 0))
            else:
                self.two_points_active = False
                self.out = blit(self.out, np.zeros((3, 1, 3), dtype=np.uint8), (7, 0))

            return self.out
        else:
            return None


if __name__ == "__main__":
    #display = WS2812_matrix(15, 20)
    display = PygameDisplay(15, 20)

    # mov_text = MovingText("FH-WS", 20, 200, 1000, "Orange")
    # out = np.zeros((15, 20, 3), dtype=np.uint8)
    # while True:
    #     out_text = mov_text.update()
    #     # if mov_text.done:
    #     #     print("Done")
    #     if out_text is not None:
    #         out = np.zeros((15, 20, 3), dtype=np.uint8)
    #         blit(out, out_text, (1, 0))
    #         # img = Image.fromarray(out, "RGB")
    #         # img.show()
    #         # img.save("test.png")
    #         # input()
    #     display.update(out)

    show_time = ShowTime((0, 127, 255))
    out = np.zeros((15, 20, 3), dtype=np.uint8)
    while True:
        out_time = show_time.update()
        if out_time is not None:
            out = np.zeros((15, 20, 3), dtype=np.uint8)
            blit(out, out_time, (2, 4))
            # img = Image.fromarray(out, "RGB")
            # img.show()
            # img.save("test.png")
        display.update(out)
