from flask import Flask, render_template, redirect, url_for, request
import os

import board
import neopixel
import numpy as np
import time

app = Flask(__name__)
run_flag = False                        
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/on")
def on():
    global run_flag
    run_flag = True
    
    
    return render_template("index.html")

@app.route("/Shutdown")
def Shutdown():
    global run_flag
    run_flag = False
    print("Wall shutdown")
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
    app.run(host="0.0.0.0", port=80, debug=True)

