import cv2
frame = cv2.VideoCapture(0)
val, img = frame.read()
cv2.imwrite('Img.png', img)
frame.release()

