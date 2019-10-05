import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

while(True):

    ret, frame = cap.read()
    og = frame;
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    
    lower_red = np.array([30,150,50])
    upper_red = np.array([255,255,180])
    
    mask = cv2.inRange(frame, lower_red, upper_red)
    output = cv2.bitwise_and(frame, frame, mask=mask)
    edge = cv2.Canny(output, 100, 200)




    cv2.imshow('frame2', og)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows();
