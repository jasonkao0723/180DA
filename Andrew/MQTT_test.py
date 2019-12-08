import paho.mqtt.client as mqtt
import RPi.GPIO
import led_test
import RPi.GPIO as GPIO
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)

MQTT_SERVER = "192.168.31.45"
MQTT_PATH = "/home/pi/180DA/"

# The callback for when the client receives a connect response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if str(msg.payload) == "light":
	# more callbacks, etc
      print ("LED on")
      GPIO.output(21,GPIO.HIGH)
      time.sleep(1)
      print ("LED off")
      GPIO.output(21,GPIO.LOW)
      time.sleep(1)	# more callbacks, etc

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
