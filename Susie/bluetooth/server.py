import bluetooth
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
bd_addr = "B8:27:EB:B9:0A:F5"

port = 1
sock.bind(("",port))
sock.listen(1)

client_sock,address = sock.accept()

data = client_sock.recv(1024)

client_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
client_sock.connect((bd_addr, port))

client_sock.send("light")

if data.decode("utf-8")  == "light":
    GPIO.output(21,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(21,GPIO.LOW)
    time.sleep(1)

