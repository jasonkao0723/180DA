import bluetooth

bd_addr = "B8:27:EB:B9:0A:F5"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send("hello!!")

sock.close()
