
import cv2
import mediapipe as mp
import time

HEIGHT = 480
WIDTH = 640

Xinit = 0

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

      # if results.multi_hand_landmarks:
      #   for hand_landmarks in results.multi_hand_landmarks:
      #     mp_drawing.draw_landmarks(
      #         image,
      #         hand_landmarks,
      #         mp_hands.HAND_CONNECTIONS,
      #         mp_drawing_styles.get_default_hand_landmarks_style(),
      #         mp_drawing_styles.get_default_hand_connections_style())

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
          print("Rechts")
          cnt = 0
        elif (SwipeResult < -80) & (cnt > 30):
          print("Links")
          cnt = 0
      except:
        pass
          


      # Flip the image horizontally for a selfie-view display.
      #cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
      cv2.imshow('MediaPipe Hands', image)
      if cv2.waitKey(5) & 0xFF == ord('q'):
        break
  cap.release()

  cv2.waitKey()
  cv2.destroyAllWindows()