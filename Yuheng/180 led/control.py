import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)

def light():
	while(True):
		print("LED on")
		as = [[0 0],[0 1]]
		time.sleep(0.1)
		time.sleep(0.1)



