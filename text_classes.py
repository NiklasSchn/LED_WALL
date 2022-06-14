from functions import text_to_rgb, blit
import time
import numpy as np
from numpy import random
from datetime import datetime
#from WS2812_matrix import WS2812_matrix
from PIL import Image
from pygame_matrix import PygameDisplay
import cv2


class MovingText:
    def __init__(self, text, size_x, speed, wait, fill):
        self.size_x = size_x
        self.pos = size_x - 1
        self.speed = speed/1000
        self.wait = wait/1000
        self.last_update = time.time()
        self.done = False
        self.fill = fill

        self.rgb_text = text_to_rgb(text, fill=self.fill)
        self.out = np.zeros((9, self.size_x, 3), dtype=np.uint8)

    def update_text(self, text):
        self.rgb_text = text_to_rgb(text, fill=self.fill)

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


class StartGame:
    def __init__(self, fill):
        self.fill = fill
        self.three = text_to_rgb("3", fill=self.fill)
        self.two = text_to_rgb("2", fill=self.fill)
        self.one = text_to_rgb("1", fill=self.fill)
        self.go = text_to_rgb("GO!", fill=self.fill)
        self.time_start = time.time()
        self.out = np.zeros((9, 17, 3), dtype=np.uint8)
        self.done = False

    def restart(self):
        self.out = np.zeros((9, 17, 3), dtype=np.uint8)
        self.time_start = time.time()
        self.done = False

    def update(self):
        time_delay = time.time() - self.time_start
        if time_delay < 1:
            self.out = blit(self.out, self.three, (0, 4))
        elif time_delay < 2:
            self.out = blit(self.out, self.two, (0, 4))
        elif time_delay < 3:
            self.out = np.zeros((9, 17, 3), dtype=np.uint8)
            self.out = blit(self.out, self.one, (0, 4))
        elif time_delay < 4:
            self.out = blit(self.out, self.go, (0, 0))
        elif time_delay < 5:
            self.done = True

        return self.out

class FireEffect:
    def __init__(self, color):
        self.last_time = time.time()
        if color == "orange":
            self.fire_colors = [(250, 192, 0), (255, 117, 0), (252, 100, 0), (215, 53, 2), (182, 34, 3), (128, 17, 0), (0, 0, 0)]
        elif color == "blue":
            self.fire_colors = [(48, 154, 241), (102, 190, 249), (183, 232, 235), (156, 222, 235), (17, 101, 193), (4, 63, 152), (0, 0, 0)]
        elif color == "violette":
            self.fire_colors = [(97, 189, 172), (94, 138, 181), (86, 82, 171), (45, 39, 102), (13, 9, 40), (0, 0, 0)]
        if len(self.fire_colors) == 7:
            self.random_max_value = 3
        else:
            self.random_max_value = 2
        self.mask = np.full((16, 20), len(self.fire_colors)-1, dtype=np.uint8)
        self.mask[15] = 0
        self.out = np.zeros((15, 20, 3), dtype=np.uint8)

    def restart(self):
        pass

    def update(self):
        if time.time() - self.last_time > 0.2:
            self.last_time = time.time()
            for x in range(20):
                 for y in range(15):
                     random_value = self.mask[y+1][x] + random.randint(0, self.random_max_value)
                     if random_value > len(self.fire_colors)-1:
                         random_value = len(self.fire_colors)-1
                     self.mask[y][x] = random_value


            for y in range(15):
                for x in range(20):
                    self.out[y][x] = self.fire_colors[self.mask[y][x]]

        return self.out



if __name__ == "__main__":
    # display = WS2812_matrix(15, 20)
    display = PygameDisplay(15, 20)

    # Moving text example: FH-WS

    # mov_text = MovingText("FH-WS", 20, 200, 1000, (255,0,255)) #(Text, Pixellaenge, Durchlauf in ms, sleep time after text, Farbe)
    # out = np.zeros((15, 20, 3), dtype=np.uint8)
    # while True:
    #     out_text = mov_text.update()
    #     if mov_text.done: #Wenn text durchgelaufen ist
    #         print("Done")
    #     if out_text is not None:
    #         out = np.zeros((15, 20, 3), dtype=np.uint8)
    #         blit(out, out_text, (1, 0))
    #          # img = Image.fromarray(out, "RGB")
    #          # img.show()
    #          # img.save("test.png")
    #          # input()
    #     display.update(out)

    # Show actual time example

    # show_time = ShowTime((0, 127, 255))
    # out = np.zeros((15, 20, 3), dtype=np.uint8)
    # while True:
    #     out_time = show_time.update()
    #     if out_time is not None:
    #         out = np.full((15, 20, 3), (255, 0, 0), dtype=np.uint8)
    #         blit(out, out_time, (2, 4), transparent=True)
    #         # img = Image.fromarray(out, "RGB")
    #         # img.show()
    #         # img.save("test.png")
    #     display.update(out)

    # Start game sequence

    # start_game = StartGame((255, 0, 255))
    # out = np.zeros((15, 20, 3), dtype=np.uint8)
    # while True:
    #     out_text = start_game.update()
    #     if start_game.done:
    #         print("Done")
    #         start_game.restart()
    #     if out_text is not None:
    #         out = np.zeros((15, 20, 3), dtype=np.uint8)
    #         blit(out, out_text, (1, 4))
    #         # img = Image.fromarray(out, "RGB")
    #         # img.show()
    #         # img.save("test.png")
    #         # input()
    #     display.update(out)

    # Show temperature example

    # temperature = 20.0
    # show_temp = MovingText(str(round(temperature, 1)) + "°C", 20, 150, 500, (255, 0, 255))  # (Text, Pixellaenge, Durchlauf in ms, sleep time after text, Farbe)
    # out = np.zeros((15, 20, 3), dtype=np.uint8)
    # while True:
    #     if show_temp.done:
    #         if temperature < 25.0:
    #             temperature += 0.3
    #         else:
    #             temperature = 19
    #         show_temp.update_text(str(round(temperature, 1)) + "°C")
    #     out_text = show_temp.update()
    #     if out_text is not None:
    #         out = np.zeros((15, 20, 3), dtype=np.uint8)
    #         blit(out, out_text, (1, 0), transparent=True)
    #     display.update(out)

    # Show capture from camera

    # cap = cv2.VideoCapture(0)
    # while cap.isOpened():
    #     success, image = cap.read()
    #     image = cv2.flip(image, 1)
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     image = Image.fromarray(image)
    #     image.thumbnail((20, 15))
    #     display.update(np.array(image, dtype=np.uint8))
    # cv2.destroyAllWindows()

    # Show image

    # out = np.zeros((15, 20, 3), dtype=np.uint8)
    # while True:
    #     image = Image.open("color_icon.png")
    #     image.thumbnail((20, 15))
    #     background = Image.new("RGB", image.size, (255, 255, 255))
    #     background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
    #     blit(out, np.array(background, dtype=np.uint8), (0, 0))
    #     display.update(out)

    # Fire effect

    fire = FireEffect("orange")
    while True:
        display.update(fire.update())



