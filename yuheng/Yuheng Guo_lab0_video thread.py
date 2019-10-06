import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret,thresh1 = cv2.threshold(hsv,127,255,cv2.THRESH_BINARY)
    ret,thresh2 = cv2.threshold(hsv,127,255,cv2.THRESH_BINARY_INV)
    ret,thresh3 = cv2.threshold(hsv,127,255,cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(hsv,127,255,cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(hsv,127,255,cv2.THRESH_TOZERO_INV)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',thresh2)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
