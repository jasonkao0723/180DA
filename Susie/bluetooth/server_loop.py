import RPi.GPIO as GPIO
import time
import keyboard
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)

bd_addr = "B8:27:EB:B9:0A:F5"

port = 1
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.bind(("",port))
sock.listen(1)

client_sock,address = sock.accept()
print ("Accepted connection from ",address)

data = client_sock.recv(1024)
print ("received [%s]" % data)

client_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
client_sock.connect((bd_addr, port))

client_sock.send("light")

if data.decode("utf-8")  == "light":
    GPIO.output(21,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(21,GPIO.LOW)
    time.sleep(1)

client_sock.close()
