import time
import paho.mqtt.publish as publish
from ast import literal_eval as dict
import RPi.GPIO as GPIO
import subprocess
import re
import threading

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


def search_num(num):
    if num[0].isdigit():
        return num[0]+search_num(num[1:])
    else:
        return ""


def buildMappingFrom(filename, MAC_mapping): #Predetermined MAC Addresses and assigned index
    file = open(filename, 'r')
        
    for line in file:
        assignedIndx = search_num(line)
        mac_idx = line.find(',') + 1
        MAC_mapping[assignedIndx] = line[mac_idx:mac_idx+17]
        
    file.close()
        
        
def buildSeatingMapFrom(filename, MAC_mapping, Seating): #From google form
    file = open(filename, 'r')
    #Seat Number, MAC address mapping
    for line in file:
        seat_num = search_num(line)
        indxOfMACIndx = (line.find(',')+1)
        Seating[seat_num] = MAC_mapping[line[indxOfMACIndx]]
        
    file.close()
    


def sendSequence(sequence):
    publish.single(MQTT_PATH, sequence, hostname=MQTT_SERVER)
    time.sleep(1)

def LED(sequence):
    seq = dict(sequence)
    if seq[MAC] == "1":
        GPIO.output(21, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(21, GPIO.LOW)

def main():
    buildMappingFrom("MAC_info.txt", MAC_mapping)
    buildSeatingMapFrom("Seating_info.txt", MAC_mapping, Seating)
    sequence1 = {Seating["1"]: "1", Seating["2"]: "0", Seating["3"]: "0", Seating["4"]: "0"}
    sequence2 = {Seating["1"]: "0", Seating["2"]: "1", Seating["3"]: "0", Seating["4"]: "0"}
    sequence3 = {Seating["1"]: "0", Seating["2"]: "0", Seating["3"]: "1", Seating["4"]: "0"}
    sequence4 = {Seating["1"]: "0", Seating["2"]: "0", Seating["3"]: "0", Seating["4"]: "1"}
    seq1 = str(sequence1)
    seq2 = str(sequence2)
    seq3 = str(sequence3)
    seq4 = str(sequence4)
    pattern = [seq1, seq2, seq3, seq4]
    while 1:
        for seq in pattern:
            t1 = threading.Thread(target=sendSequence, args=(seq,))
            t2 = threading.Thread(target=LED, args=(seq,))
            
            t1.start()
            t2.start()
            
            t1.join()
            t2.join()
            



    


if __name__ == "__main__":

    main()
