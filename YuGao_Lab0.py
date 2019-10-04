#2019fall, ece180DALab 0
#OpenCV, video edge detection
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    edge = cv2.Canny(gray,100,200)

    cv2.imshow('frame',frame)
    cv2.imshow('edge',edge)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
