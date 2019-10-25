import RPi.GPIO as GPIO
import RPi.GPIO as GPIO
import time
import keyboard
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)
def led():
  while(1):
    print ("LED on")
    GPIO.output(21,GPIO.HIGH)
    time.sleep(1)
    print ("LED off")
    GPIO.output(21,GPIO.LOW)
    time.sleep(1)
