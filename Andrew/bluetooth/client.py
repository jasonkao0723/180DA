import bluetooth

#bd_addr = "01:23:45:67:89:AB"
bd_addr = "6C:4D:73:A3:66:54"
port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send("hello!!")

sock.close()
