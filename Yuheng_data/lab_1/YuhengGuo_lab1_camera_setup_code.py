import cv2
vc = cv2.VideoCapture(0)
rval, fram = vc.read()
cv2,imwrite("ptest.png",fram)