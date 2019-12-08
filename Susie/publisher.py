import paho.mqtt.publish as publish
MQTT_SERVER = "192.168.31.45"
MQTT_PATH = "/home/pi/180DA/"
publish.single(MQTT_PATH, "light", hostname=MQTT_SERVER)
