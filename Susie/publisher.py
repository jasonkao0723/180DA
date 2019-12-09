import paho.mqtt.publish as publish
import time
MQTT_SERVER = "192.168.31.45"
MQTT_PATH = "/home/pi/180DA/"
while(1):
	publish.single(MQTT_PATH, "light", hostname=MQTT_SERVER)
	time.sleep(5)
	publish.single(MQTT_PATH, "sleep", hostname=MQTT_SERVER)
	time.sleep(5)
