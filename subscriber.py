import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from ast import literal_eval as dict
import subprocess
import re

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)

MQTT_SERVER = "192.168.31.45"
MQTT_PATH = "/home/pi/180DA/"

MAC = subprocess.check_output(['hciconfig'], stdin=subprocess.PIPE)
MAC = re.search('BD Address:(.*)ACL', MAC)
MAC = MAC.group(1)
MAC = MAC.strip()

seat_num = 0

print(MAC)
# The callback for when the client receives a connect response from the server.
def on_connect(client, userdata, flags, rc):
    # on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
    print("Connected with result code "+str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = str(msg.payload)
    global seat_num 
    print(payload)
    print("I am here")
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

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
