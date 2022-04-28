from flask import Flask, render_template, redirect, url_for, request
import os
from functions import text_to_rgb, blit
from text_classes import ShowTime
from WS2812_matrix import WS2812_matrix
from text_classes import MovingText, ShowTime, StartGame
import board
import neopixel
import numpy as np
import mediapipe as mp
import cv2
import time
from PIL import Image

WIDTH = 640
HEIGHT = 480
Xinit = 0
widget = 0


cap = 0
CaptureFlag = False
CameraRenderFlag = False
TempFlag = False

def cleanUp():
    global CaptureFlag
    CaptureFlag = False
    
    global CameraRenderFlag
    CameraRenderFlag = False
    
    global TempFlag
    TempFlag = False
    global cap
    if cap != 0:
        cap.release()
    cv2.destroyAllWindows()
    out = np.zeros((15, 20, 3), dtype=np.uint8)
    display.update(out)
    

def switchPage(widget):
    if widget == 1:  # Time
        a = False
        
        pixels = neopixel.NeoPixel(board.D18, 300, brightness=0.2)  # boardD18 = Pin 18, 50=Anzahl LED LED AUS

        pixels.fill((0, 0, 0))
        show_time = ShowTime((0, 127, 255))
        out = np.zeros((15, 20, 3), dtype=np.uint8)
        out_time = show_time.update()
        if out_time is not None:
            out = np.full((15, 20, 3), (255, 0, 0), dtype=np.uint8)
            blit(out, out_time, (2, 4))

            display.update(out)
        global CaptureFlag
        while (CaptureFlag) & (a):  # a mueste eine Timer Var sein
            out_time = show_time.update()
            if out_time is not None:
                out = np.full((15, 20, 3), (255, 0, 0), dtype=np.uint8)
                blit(out, out_time, (2, 4))

            display.update(out)


    elif widget == -1:  # LED MODE
        temperature = 20.0
        show_temp = MovingText(str(round(temperature, 1)) + "°C", 20, 150, 500, (255, 0, 255))  # (Text, Pixellaenge, Durchlauf in ms, sleep time after text, Farbe)
        out = np.zeros((15, 20, 3), dtype=np.uint8)
     
        
        while CaptureFlag:
             if show_temp.done:
                 if temperature < 25.0:
                     temperature += 0.3
                 else:
                     temperature = 19
                 show_temp.update_text(str(round(temperature, 1)) + "°C")
             out_text = show_temp.update()
             if out_text is not None:
                 out = np.zeros((15, 20, 3), dtype=np.uint8)
                 blit(out, out_text, (1, 0), transparent=True)
             display.update(out)
        


#### Weiter Widgets hier mit elif

def SwipeReco(Xcoo):
    global Xinit
    result = Xcoo - Xinit
    Xinit = Xcoo

    return result



app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")
display = WS2812_matrix(15, 20)

@app.route("/Capture")
def Capture():
    cleanUp()
    global CaptureFlag
    global CameraRenderFlag
    global TempFlag
    TempFlag = False
    CameraRenderFlag = False
    CaptureFlag = True
    
    while CaptureFlag:
        
        global WIDTH
        global HEIGHT
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands
        widget = 0

        cnt = 0
        global cap
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        with mp_hands.Hands(
                max_num_hands=1,

                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:

            while cap.isOpened():

                cnt = cnt + 1
                success, image = cap.read()
                image = cv2.flip(image, 1)

                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if cnt == 30:
                    print("Swipe möglich")

                try:
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            lmx = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                            lmy = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                            cx, cy = int(lmx * WIDTH), int(lmy * HEIGHT)

                    SwipeResult = SwipeReco(cx)

                    if (SwipeResult > 80) & (cnt > 30):

                        widget = 1
                        print("Rechts")

                        cnt = 0

                    elif (SwipeResult < -80) & (cnt > 30):

                        widget = -1
                        print("Links")

                        cnt = 0

                except:
                    pass
                switchPage(widget)
                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break
        cap.release()

        cv2.waitKey()
        cv2.destroyAllWindows()
    return render_template("index.html")

@app.route("/Shutdown")
def Shutdown():
    global CaptureFlag
    CaptureFlag = False
    
    global CameraRenderFlag
    CameraRenderFlag = False
    
    global TempFlag
    TempFlag = False
    global cap
    cap.release()
    cv2.destroyAllWindows()
    print("Shutdown")
    out = np.zeros((15, 20, 3), dtype=np.uint8)
    display.update(out)
    return render_template("index.html")

@app.route("/LEDTest")
def ShowTemp():
    cleanUp()
    global TempFlag
    TempFlag = True
    
    
    temperature = 20.0
    show_temp = MovingText(str(round(temperature, 1)) + "°C", 20, 150, 500, (255, 0, 255))  # (Text, Pixellaenge, Durchlauf in ms, sleep time after text, Farbe)
    out = np.zeros((15, 20, 3), dtype=np.uint8)
    while TempFlag:
         if show_temp.done:
             if temperature < 25.0:
                 temperature += 0.3
             else:
                 temperature = 19
             show_temp.update_text(str(round(temperature, 1)) + "°C")
         out_text = show_temp.update()
         if out_text is not None:
             out = np.zeros((15, 20, 3), dtype=np.uint8)
             blit(out, out_text, (1, 0), transparent=True)
         display.update(out)

    return render_template("index.html")

@app.route("/Gamemode1")
def RenderCameraCapture():
     cleanUp()
     global CaptureFlag
     CaptureFlag = False
     global CameraRenderFlag
    
     CameraRenderFlag = True
     global TempFlag
     TempFlag = False

   
     
     while CameraRenderFlag:
         global cap
         cap = cv2.VideoCapture(0)
         while cap.isOpened():
             success, image = cap.read()
             image = cv2.flip(image, 1)
             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
             image = Image.fromarray(image)
             image.thumbnail((20, 15))
             display.update(np.array(image, dtype=np.uint8))
         cv2.destroyAllWindows()

     return render_template("index.html")

@app.route("/Gamemode2")
def ShowImage():
    global run_flag
    run_flag = True
    out = np.zeros((15, 20, 3), dtype=np.uint8)
    while run_flag:
        image = Image.open("color_icon.png") #Hier noch das Bild wechseln !!
        image.thumbnail((20, 15))
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
        blit(out, np.array(background, dtype=np.uint8), (0, 0))
        display.update(out)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="192.168.178.37", port=80, debug=True)

