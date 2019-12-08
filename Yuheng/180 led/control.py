import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)

def light():
		pat_1 = [[1,0],[0,0]]
		pat_2 = [[0,1],[0,0]]
		pat_3 = [[0,0],[1,0]]
		pat_4 = [[0,0],[0,1]]

def light_1():
		pat_1 = [[1,1],[1,1]]
		pat_2 = [[1,1],[1,1]]
		pat_3 = [[1,1],[1,1]]
		pat_4 = [[1,1],[1,1]]

def light_2():
		pat_1 = [[0,0],[0,0]]
		pat_2 = [[0,0],[0,0]]
		pat_3 = [[0,0],[0,0]]
		pat_4 = [[0,0],[0,0]]



