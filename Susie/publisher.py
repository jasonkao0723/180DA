import paho.mqtt.publish as publish
MQTT_SERVER = "2605:e000:1703:634e:8883:94c6:3328:b5f5"
MQTT_PATH = "topic/state"
publish.single(MQTT_PATH, "light", hostname=MQTT_SERVER)
