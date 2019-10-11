import cv2 
pic=cv2.VideoCapture(0) 
rval, frame = pic.read() 
cv2.imwrite("image.png",frame)
