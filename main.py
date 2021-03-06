from flask import Flask, render_template, redirect, url_for, request
from functions import text_to_rgb, blit
from text_classes import ShowTime
from WS2812_matrix import WS2812_matrix
from text_classes import MovingText, ShowTime, StartGame, FireEffect
import board
import neopixel
import numpy as np
import mediapipe as mp
import cv2
from PIL import Image
import requests
import time
from picamera import PiCamera

## Camera Width x Height ##
WIDTH = 640
HEIGHT = 480

## Initial widget,cap and Koos(x) ##
Xinit = 0
widget = 0
cap = 0

swipe_cnt = 0
## Initial Flags to set different Modes ##
CaptureFlag = False
CameraRenderFlag = False
TempFlag = False
ShowImageFlag = False
LightModeFlag = False
def cleanUp():
    '''
    This function sets all global Variables to initial State
    To prevent hickups and chrash errors
    :return: None
    '''
    
    global LightModeFlag
    LightModeFlag = False
    
    global CaptureFlag
    CaptureFlag = False
    
    global CameraRenderFlag
    CameraRenderFlag = False
    
    global TempFlag
    TempFlag = False
    
    global ShowImageFlag
    ShowImageFlag = False

    global cap
    if cap != 0:
        cap.release()

    cv2.destroyAllWindows()
    out = np.zeros((15, 20, 3), dtype=np.uint8)
    display.update(out)
    

def switchPage(widget):
    """
    This function change the widget im CameraMode, when a certain swipe is recognized
    :param widget: Current Widget
    :return: None
    """
    global CaptureFlag
    
    if widget == 1:  # Time widget
                   
        
        ### Code to display current Mode on LEDWALL ###
           
        show_time = ShowTime((255, 255, 255))
        out = np.zeros((15, 20, 3), dtype=np.uint8)
        
        while (CaptureFlag):  # a mueste eine Timer Var sein
            
           
            out_time = show_time.update()
            if out_time is not None:
                out = np.full((15, 20, 3), (51, 102, 255), dtype=np.uint8)
                blit(out, out_time, (2, 4),True)

            display.update(out)

    elif widget == 2:  #Current Temperature widget
        cleanUp()
        
        CaptureFlag = True

        show_temp = MovingText( "??C", 20, 150, 500, (255, 0, 255))  # (Text, Pixellaenge, Durchlauf in ms, sleep time after text, Farbe)

        while CaptureFlag:
        
            # Enter your API Key here (xxx)
            #BASE_URL = "https://api.openweathermap.org/data/2.5/weather?lat=50.04937&lon=10.22175&appid=xxxxxxxxx&units=metric"
            # Schweinfurt lat=50.04937&lon=10.22175

            #final_url = BASE_URL
            #weather_data = requests.get(final_url).json()

            #icon = weather_data.get("weather")[0].get("icon")
            #iconChopped = str(icon)[0] + str(icon)[1]
            image = Image.open(f"weather_icons/01.png") #Hier Icon setzen
            image.thumbnail((35, 25))
            background = Image.new("RGB", image.size, (0, 0, 0))
            background.paste(image, mask=image.split()[3])  # 3 is the alpha channel 
            #currentTemp = str(weather_data.get("main").get("temp"))
            out = np.zeros((15, 20, 3), dtype=np.uint8)

            if show_temp.done:
                blit(out, np.array(background, dtype=np.uint8), (-6, -3))
                display.update(out)
                time.sleep(8)
                show_temp.restart()
            else:
                show_temp.update_text("22" + "??C") #Hartcodiert
                out_text = show_temp.update()
                if out_text is not None:
                    out = np.zeros((15, 20, 3), dtype=np.uint8)
                    blit(out, out_text, (1, 0), transparent=True)
                    display.update(out)
              
    elif widget == 0: #ImgRender
        
   
   
        out = np.zeros((15, 20, 3), dtype=np.uint8)
        while CaptureFlag:
            image = Image.open("Mario.png")
            image.thumbnail((25, 20))
            background = Image.new("RGB", image.size, (0, 0, 0))
            background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
            blit(out, np.array(background, dtype=np.uint8), (-2, 2))
            display.update(out)
            

    #### Add new widgets here with elif(widget == ...) ####

def SwipeReco(Xcoo):
    """
    Function to detect swipe gesture
    :param Xcoo: Current Xcoo of Hand
    :return: Xvalue on depend of Initial X
    """
    global Xinit
    result = Xcoo - Xinit
    Xinit = Xcoo

    return result

####### Flask App for Webserver #######

app = Flask(__name__) #Inital Flask App

### Root Endpoint ###
@app.route("/")
def home():
    return render_template("index.html")
display = WS2812_matrix(15, 20)

### Capture Endpoint (Recognize Swipe) ###
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
        outSwipeStatus = np.zeros((15,20,3), dtype= np.uint8)
        
        with mp_hands.Hands(
                max_num_hands=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                cnt = cnt + 1
                success, image = cap.read()
                image = cv2.flip(image, 0)
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
                    outSwipeStatus[0][0] = (0,255,0)
                    
                    print("Swipe m??glich")
                try:
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            lmx = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                            lmy = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                            cx, cy = int(lmx * WIDTH), int(lmy * HEIGHT)

                    SwipeResult = SwipeReco(cx)
                    if (SwipeResult > 90) & (cnt > 20):
                        outSwipeStatus[0][0] = (255,0,0)
                        global swipe_cnt
                        
                        ### Swipe to right detected ###

                        if(swipe_cnt != 2):
                            swipe_cnt = swipe_cnt + 1
                        else:
                            swipe_cnt = 0
                            
                        print("Rechts")
                        cnt = 0

                    elif (SwipeResult < -90) & (cnt > 20):
                        outSwipeStatus[0][0] = (255,0,0)

                        if(swipe_cnt != 0):
                            swipe_cnt = swipe_cnt - 1
                        else:
                            swipe_cnt = 2
                            
                        ### Swipe to left detected ###

                        print("Links")
                        cnt = 0
                    detected = True
                except:
                    detected = False
                    
                out = np.zeros((15, 20, 3), dtype=np.uint8)
                
                if(swipe_cnt ==1):
                    mode = text_to_rgb("Time",(255,255,255))
                    blit(out, mode,(0,0),True)
                    
                    
                elif(swipe_cnt ==2):
                    mode = text_to_rgb("Temp",(255,255,0))
                    blit(out, mode,(0,0),True)
                    
                    
                elif(swipe_cnt ==0):
                    mode = text_to_rgb("Img",(0,255,255))
                    blit(out, mode,(0,0),True)
                    
                blit(out,outSwipeStatus,(0,0),True)
                display.update(out)
                if((cnt == 70) & detected):
                    print("lock", " " , swipe_cnt)
                    switchPage(swipe_cnt)
                
                cv2.imshow('MediaPipe Hands', cv2.flip(image,0))
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.waitKey()
        cv2.destroyAllWindows()
    return render_template("index.html")

### Shutdown Endpoint to stop all Leds ###
@app.route("/Shutdown")
def Shutdown():
    
    global CaptureFlag
    CaptureFlag = False
    
    global CameraRenderFlag
    CameraRenderFlag = False
    
    global TempFlag
    TempFlag = False
    
    global ShowImageFlag
    ShowImageFlag = False
    
    global LightModeFlag
    LightModeFlag = False

    global cap
    if cap:
        cap.release()
        cv2.destroyAllWindows()
   
    out = np.zeros((15, 20, 3), dtype=np.uint8)
    display.update(out)
    return render_template("index.html")

### Camera LiveRenderMode ###
@app.route("/LiveRenderMode")
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
             image = cv2.flip(image, 0)
             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
             image = Image.fromarray(image)
             image.thumbnail((20, 15))
             display.update(np.array(image, dtype=np.uint8))
         cv2.destroyAllWindows()

     return render_template("index.html")



@app.route("/LightMode")
def LightMode():
    cleanUp()
    global LightModeFlag
    LightModeFlag = True

    
    while LightModeFlag:
        global WIDTH
        global HEIGHT
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands
        outSwipeStatus = np.zeros((15,20,3), dtype= np.uint8)
        cnt = 0
        global cap
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        fire = FireEffect("orange")
        with mp_hands.Hands(
                max_num_hands=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                cnt = cnt + 1
                success, image = cap.read()
                image = cv2.flip(image, 0)
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
                    outSwipeStatus[0][0] = (0,255,0)
                    print("Swipe m??glich")
                try:
                    
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            lmx = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                            lmy = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                            cx, cy = int(lmx * WIDTH), int(lmy * HEIGHT)
        
                    SwipeResult = SwipeReco(cx)
                    
                    if (SwipeResult > 60) & (cnt > 20):
                        global swipe_cnt
                        
                        ### Swipe to right detected ###
                        
                        if(swipe_cnt != 2):
                            swipe_cnt = swipe_cnt + 1
                        else:
                            swipe_cnt = 0
                        outSwipeStatus[0][0] = (255,0,0)    
                        print("Rechts")
                        cnt = 0

                    elif (SwipeResult < -60) & (cnt > 20):
                       
                        if(swipe_cnt != 0):
                            swipe_cnt = swipe_cnt - 1
                        else:
                            swipe_cnt = 2
                            
                        ### Swipe to left detected ###
                        outSwipeStatus[0][0] = (255,0,0)
                        print("Links")
                        cnt = 0
                    detected = True
                except:
                    
                    detected = False
                    
                out = np.zeros((15, 20, 3), dtype=np.uint8)
                if(swipe_cnt ==1):
                    out = np.full((15,20,3),(255,255,255),dtype=np.uint8)
                        
                    
                elif(swipe_cnt ==2):
                    
                    out = np.full((15,20,3),(0,255,255),dtype=np.uint8)
                    
                    
                elif(swipe_cnt ==0):
                    #out = np.full((15,20,3),(0,0,0),dtype=np.uint8)
                    
    
                    out = fire.update()
                    
                blit(out,outSwipeStatus,(0,0),True)
                display.update(out)     
                if((cnt == 70) & detected):
                    if(swipe_cnt ==1):
                        out = np.full((15,20,3),(255,255,255),dtype=np.uint8)
                        
                    
                    elif(swipe_cnt ==2):
                    
                        out = np.full((15,20,3),(0,255,255),dtype=np.uint8)
                    
                    
                    
                     
                    while LightModeFlag:
                        if(swipe_cnt ==0):
                           out = fire.update()
                        display.update(out) 
                      
                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.waitKey()
        cv2.destroyAllWindows()
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(host="192.168.178.37", port=80, debug=True) #Run Server

