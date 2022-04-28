import board
import neopixel
from time import sleep
import sys
import cv2
import mediapipe as mp
import random
import numpy as np
from text_classes import ShowTime
from WS2812_matrix import WS2812_matrix
import time

cap = cv2.VideoCapture(0) # 0 Represents the camera of the computer
#（2） Create a method to detect hand keys
mpHands = mp.solutions.hands # Receiving method
hands = mpHands.Hands(static_image_mode=False, # Static tracking , lower than 0.5 Confidence will track again
max_num_hands=2, # At most 2 One hand
min_detection_confidence=0.5, # Minimum detection confidence
min_tracking_confidence=0.5) # Minimum tracking confidence

mpDraw = mp.solutions.drawing_utils
# Check the time
pTime = 0 # Time before processing an image
cTime = 0 # The time when a picture is processed
# Store coordinate information
lmList = []
#（3） Process video images
# The file is set to True, For each frame of video image processing
while True:
    # Returns whether the read is successful and the read image
    success, img = cap.read()
    # Send... In a loop rgb Image to hands in ,opencv The default image is BGR Format
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Pass the image into the detection model , Extract information
    results = hands.process(imgRGB)
    # Check whether there are more than one hand in each frame , Extract them one by one
    if results.multi_hand_landmarks: # If there is no hand, it is None
        for handlms in results.multi_hand_landmarks:
            # Get the index and coordinates of each key point
            for index, lm in enumerate(handlms.landmark):
# The index for 0 Represents the middle part of the bottom of the hand , by 4 Represents a finger key or fingertip
# print(index, lm) # Output 21 A key point of the hand xyz coordinate (0-1 Between ), Is the aspect ratio relative to the image
# Just use x and y Find location information
# take xy Convert the scale coordinates of to pixel coordinates
                h, w, c = img.shape # Store images separately \ wide \ The channel number
# Central coordinates ( decimal ), Must be converted to an integer ( Pixel coordinates )
                cx ,cy = int(lm.x * w), int(lm.y * h) # Scale coordinates x The pixel coordinates multiplied by the width
# Print display 21 Pixel coordinates of key points
                print(index, cx, cy)
# Store coordinate informationlambdalmList.append([index, cx, cy])
# stay 21 Change the key point ,img Drawing board , coordinate (cx,cy), radius 5, Blue fill
                cv2.circle(img, (cx,cy), 12, (0,0,255), cv2.FILLED)
# Draw keys for each hand
                mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS) # Pass in the drawing board you want to draw img, One handed information handlms
# mpHands.HAND_CONNECTIONS Draw a line between hand keys
# Record the execution time
    cTime = time.time()
# Calculation fps
    fps = 1/(cTime-pTime)
    # Reset start time
    pTime = cTime
    # hold fps On the window ;img Drawing board ; Rounded fps value ; Displays the coordinates of the location ; Set the font ; Font scale ; Color ; The thickness of the
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    # Display images
    cv2.imshow('Image', img) # Window name , Image variables
    if cv2.waitKey(1) & 0xFF==27: # Every frame 1 Disappear in milliseconds
        break
# Release video resources
cap.release()
cv2.destroyAllWindows()