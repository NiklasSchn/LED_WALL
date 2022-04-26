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


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def calculateCoo(XPose, YPose, height, width):
    '''calculate coordinates based on your webcam format'''
    XCoo, YCoo = int(XPose * width), int(YPose * height)
    return XCoo, YCoo

if __name__ == "__main__":
    
        
    oldXCoo = 0
    oldYCoo = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    display = WS2812_matrix(15, 20)
    
    global NXcoog 
    global NYcoog
    NXcoog = 0
    NYcoog = 0
    
    with mp_pose.Pose(
        
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
           
        while cap.isOpened():
            
            success, image = cap.read()
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            #mask = np.zeros_like(image)

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            #image.flags.writeable = True
            #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try: 
                landmarks = results.pose_landmarks.landmark
           
                nose_x, nose_y = landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y
                
                NXcoo, NYcoo = calculateCoo(nose_x, nose_y, 640, 480)
                
                NXcoog = int(NXcoo/32)
                NYcoog = int(NYcoo/32)
                
#                 newNXcoo = int(NXcoo/32)*32
#                 newNYcoo = int(NYcoo/32)*32
#                 
#                 oldXCoo = newNXcoo
#                 oldYCoo = newNYcoo
                
                print("X: " , NXcoog)
                print("Y: " , NYcoog)
                display.clear()
                display.write(NXcoog, NYcoog ,(255,0,0))
                
            except(AttributeError):
                pass
            
            except(IndexError):
                pass
            
      
#              mp_drawing.draw_landmarks(
#                  image,
#                  results.hand_landmarks,
#                  mp_pose.POSE_CONNECTIONS,
#                  landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            
            #cv2.imshow('MediaPipe Pose', image)
            
            if cv2.waitKey(5) & 0xFF == ord('q'):
                cap.release()
                cv2.waitKey()
                cv2.destroyAllWindows()
                
                sys.exit()
            
            
            
            