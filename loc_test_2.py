import parse
import subprocess
import re
import threading
import bluetooth

row_num = 2
col_num = 2
num_client = row_num

mac = subprocess.run(['hciconfig'], stdout=subprocess.PIPE)
mac = str (mac.stdout)
mac = re.search('BD Address:(.*)ACL', mac)
mac = mac.group(1)
mac = mac.strip()

def connectToServer(server):
	bd_addr = server
	port = 1
	sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((bd_addr, port))
	sock.send("hello!!")
	sock.close()
	
def acceptClient():
	client_cnt = 0
	while client_cnt <= num_client: 
		server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		port = 1
		server_sock.bind(("",port))
		server_sock.listen(1)
		client_sock,address = server_sock.accept()
		print ("Accepted connection from ",address)
		data = client_sock.recv(1024)
		print ("received [%s]" % data)
		client_sock.close()
		server_sock.close()
		client_cnt += 1



#Get seating arrangement
seat = {}
parse.parse_seating("bluetooth-info.txt", "pi-info.txt", seat)

#Parse arrangement result
location = int(seat[mac])
master_seat = location % row_num
if master_seat == 0:
	master_seat = col_num

if location > col_num:
	connectToServer(seat[str(master_seat)])
elif location == 1:
	acceptClient()
else:
	#Start threads for client and server codes
	client = threading.Thread(target=connectToServer, args=(seat[str(master_seat)],))
	server = threading.Thread(target=acceptClient)
	
	client.start()
	server.start()

	client.join()
	server.join()
