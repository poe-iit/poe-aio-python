#Server use decode
import socket


s = socket.socket()
host = "192.168.2.50"
port = 12345
s.bind((host,port))

s.listen(5)

while True:

    c,addr = s.accept()
    print("Got connection from " + str(addr))
    ret_val = c.send("Thank you".encode('utf-8'))
    print ("ret_val={}".format(ret_val))
    c.close()