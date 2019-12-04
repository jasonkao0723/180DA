import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('131.179.34.72', 3947))
text = "I am CLIENT\n"
client.send(text.encode())
from_server = client.recv(4096)
client.close()
print(from_server.decode())
