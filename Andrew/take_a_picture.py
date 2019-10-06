import cv2
vc=cv2.VideoCapture(0)
rval, frame=vc.read()
cv2.imwrite("test1.png",frame)
