#client use decode
from socket import gethostname, socket

serSocket = socket()
server = "192.168.2.50"
port = 12345
serSocket.connect((server, port))

data = serSocket.recv(1024)
msg = data.decode('utf-8')
print("Returned Msg from server:  <{}>".format(msg))
serSocket.send(b"HAHAH")

serSocket.close()



