import time
import paho.mqtt.publish as publish
from ast import literal_eval as dict
import RPi.GPIO as GPIO
import subprocess
import re
import threading
from parse import buildMappingFrom
from parse import buildSeatingMapFrom

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)


MAC = subprocess.check_output(['hciconfig'], stdin=subprocess.PIPE)
MAC = re.search('BD Address:(.*)ACL', MAC)
MAC = MAC.group(1)
MAC = MAC.strip()


MQTT_SERVER = "192.168.31.45"
MQTT_PATH = "/home/pi/180DA/"


MAC_info = "MAC_info.txt"
seating_info = "Seating_info.txt"
MAC_mapping = {}
Seating = {}



def sendSequence(sequence):
    publish.single(MQTT_PATH, sequence, hostname=MQTT_SERVER)
    time.sleep(1)

def LED(sequence):
    payload = str(msg.payload)
    global seat_num
    global MAC
    print(payload)
    if payload[0] == "{":
        print("I am in the { loop")
        seat_assignment = dict(payload)
        seat_num = int(seat_assignment[MAC])-1
        print("Seat Number: "+str(seat_num))
    else:
        sequence = payload
        print("Sequence Received : "+sequence)
        print("LED: "+sequence[seat_num])
        if sequence[seat_num] == "1":
            GPIO.output(21,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(21, GPIO.LOW)

def main():
    buildMappingFrom("MAC_info.txt", MAC_mapping)
    buildSeatingMapFrom("Seating_info.txt", MAC_mapping, Seating)
    seat_assignment = str(Seating)
    start = 1
    pattern = ["1000", "0100", "0010", "0001", "0000", "1111"]
    while True:
        if start == 1:
            sendSequence(seat_assignment)
            start = 0
        for seq in pattern:
            sendSequence(seq)


if __name__ == "__main__":
    cmd = ["python", "subscriber.py"]
    t1 = threading.Thread(target=subprocess.call, args=(cmd,))
    t2 = threading.Thread(target=main)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
