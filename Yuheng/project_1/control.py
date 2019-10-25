import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)

def light():
	while(True):
		print("LED on")
		GPIO.output(21,GPIO.HIGH)
		time.sleep(0.1)
		print("LED off")
		GPIO.output(21,GPIO.LOW)
		time.sleep(0.1)



