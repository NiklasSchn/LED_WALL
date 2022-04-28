from flask import Flask, render_template, redirect, url_for, request
import os
from functions import text_to_rgb, blit
from text_classes import ShowTime
from WS2812_matrix import WS2812_matrix
import board
import neopixel
import numpy as np
import time

app = Flask(__name__)
run_flag = False

@app.route("/")
def home():
    return render_template("index.html")
display = WS2812_matrix(15, 20)
@app.route("/on")
def on():
    global run_flag
    run_flag = True
    
    show_time = ShowTime((0, 127, 255))
    out = np.zeros((15, 20, 3), dtype=np.uint8)
    while run_flag:
        out_time = show_time.update()
        if out_time is not None:
            out = np.full((15, 20, 3),(255,0,0), dtype=np.uint8)
            blit(out, out_time, (2, 4))
            # img = Image.fromarray(out, "RGB")
            # img.show()
            # img.save("test.png")
        display.update(out)
    
    return render_template("index.html")

@app.route("/Shutdown")
def Shutdown():
    global run_flag
    run_flag = False
    out = np.zeros((15, 20, 3), dtype=np.uint8)
    display.update(out)
    return render_template("index.html")

@app.route("/LEDTest")
def LEDTest():
    global run_flag
    run_flag = True
    while run_flag:
        print("Wall is LED Mode !")

    return render_template("index.html")

@app.route("/Gamemode1")
def Gamemode1():
    global run_flag
    run_flag = True
    while run_flag:
        print("Wall is Gamemode1 !")

    return render_template("index.html")

@app.route("/Gamemode2")
def Gamemode2():
    global run_flag
    run_flag = True
    while run_flag:
        print("Wall is in Gamemode2 !")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="192.168.178.37", port=80, debug=True)

