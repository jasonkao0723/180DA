import time
import paho.mqtt.publish as publish


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
        MAC_mapping[] = line[mac_idx:]
        
    file.close()
        
def buildSeatingMapFrom(filename, MAC_mapping, Seating): #From google form
    file = open(filename, 'r')
    #Seat Number, MAC address mapping
    for line in file:
        seat_num = search_num(line)
        indxOfMACIndx = str(line.find(',')+1)
        Seating[search_num] = MAC_mapping[indxOfMACIndx]
        
    file.close()
    

sequence1 = {Seating["1"]: "1", Seating["2"]: "0", Seating["3"]: "0"}
sequence2 = {Seating["1"]: "0", Seating["2"]: "1", Seating["3"]: "0"}
sequence3 = {Seating["1"]: "0", Seating["2"]: "0", Seating["3"]: "1"}

seq1 = str(sequence1)
seq2 = str(sequence2)
seq3 = str(sequence3)

pattern = [seq1, seq2, seq3]

while 1:
    for seq in pattern:
        publish.single(MQTT_PATH, seq, hostname=MQTT_SERVER)
        time.sleep(3)

