import paho.mqtt.publish as publish
#MQTT communication
MQTT_SERVER = "192.168.31.243" # same mosquitto server ip. 
MQTT_PATH = "hello/world" # same topic
publish.single(MQTT_PATH, "Hello World!", hostname=MQTT_SERVER)
print("Done")