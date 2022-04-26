'''checkout requirements textfile for same versions'''
import board
import neopixel
from time import sleep
from functions import text_to_rgb, blit
import sys
import cv2
import mediapipe as mp
import numpy as np
from text_classes import ShowTime
from WS2812_matrix import WS2812_matrix


display = WS2812_matrix(15, 20)
WIDTH = 640
HEIGHT = 480
Xinit = 0
widget = 0
def switchPage(widget):
    
    if widget == 1 : #Time
        
        show_time = ShowTime((0, 127, 255))
        out = np.zeros((15, 20, 3), dtype=np.uint8)
        
        out_time = show_time.update()
        if out_time is not None:
            out = np.full((15, 20, 3),(255,0,0), dtype=np.uint8)
            blit(out, out_time, (2, 4))
              
        display.update(out)
        
    
    elif widget == -1: #LED MODE
        ORDER = neopixel.RGB
        pixels = neopixel.NeoPixel(board.D18, 300, brightness = 0.2, pixel_order=ORDER) #boardD18 = Pin 18, 50=Anzahl LED

        pixels.fill((255,255,255)) #pixel blue g,r,b

        pixels.show() #sudo python3 rgb_test.py

  
        
        
        
        
def SwipeReco(Xcoo):
    global Xinit
    result = Xcoo - Xinit
    Xinit = Xcoo

    return result 


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

if __name__ == "__main__":
    
    cnt = 0
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
                    #display.write(0, 5 ,(255,0,0))
                    cnt = 0
                    
                elif (SwipeResult < -80) & (cnt > 30):
                    
                    widget = -1
                    print("Links")
                    #display.write(0, 5 ,(255,255,0))
                    cnt = 0
            
            except:
                pass
            
            switchPage(widget) 
                

              # Flip the image horizontally for a selfie-view display.
              #cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    cap.release()

    cv2.waitKey()
    cv2.destroyAllWindows()   


