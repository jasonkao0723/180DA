import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)

def localization(loc)
	for i in range(loc):
		GPIO.output(21,GPIO.HIGH)
		time.sleep(1)
		GPIO.output(21,GPIO.LOW)
		time.sleep(1)
