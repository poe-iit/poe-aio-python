import sys
import socket
import selectors
import types
import threading
from queue import Queue

sel = selectors.DefaultSelector()

client_1_address = "127.0.0.1"
client_1_port = 65431
client_2_ip = "127.0.0.1"
client_2_port = "65432"
client_2_sending_address = "('127.0.0.1', 65432)"

class Server:

    def __init__(self, host, port, argv):
        self.host = host
        self.port = port
        self.argv = argv
        self.server_socket = None

        self.client1_address = "127.0.0.1"
        self.client1_port = 65431
        self.client2_address = "127.0.0.1"
        self.client2_port = "65432"

        self.client1 = None
        self.client2 = None

        self.data = types.SimpleNamespace(
            connid=1,
            msg_total=1,
            recv_total=0,
            messages=None,
            outb=b"",
        )

        self.client1_connected = False

    # Registers and binds the sockets. Sets the socket to listen on the host and port to act as a server
    def init_sockets_and_listen(self):

        try:
            num_conns = 1
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print("listening on", (self.host, self.port))
            self.server_socket.setblocking(False)
            sel.register(self.server_socket, selectors.EVENT_READ, data=None)
        except:
            print("could not init socket, retrying")
            self.init_sockets_and_listen()

    # Sends emergency message to the ceiling device
    def alert_client_2(self, message):

        self.data.messages = b"jeff"
        self.client1.send(self.data.messages)


    # determines which client is connecting to the server
    # saves those connections to Server object to easily communicate with them
    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(addr[0])
        print(addr[1])

        # distinguish client 1 from 2 while testing locally
        if addr[0] == "192.168.2.51":
            self.client1 = conn
            self.client_1_port = addr[1]
            print("accepted connection from client 1")
            self.client1.setblocking(False)
            data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")


            self.client1.send(b"Server got your message")
            self.client1_connected = True

        if addr[1] == "192.168.2.52":
            self.client2 = conn
            print("accepted connection from client 2")
            self.client2.setblocking(False)
            data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")



    # Handles every incoming connection to the server, determines if the message is meant to be read for contents or if the message is telling the server to shut down
    def service_connection(self,key, mask):
        sock = key.fileobj
        data = key.data
        #Reading data from the accepted message, see what type of emergency_type it is
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
                recieved_message = str(data.outb)
                print("Got message from client:", str(data.outb))

                if "client1" in recieved_message:
                    if "Fire" in recieved_message:
                        print("Alerting Public Safety there is a fire")
                        message =  b"FORWARDING EMERGENCY FROM HEADLESS CLIENT, Fire"
                        self.alert_client_2(message)
                        # Make GUI Popup for verification
                        self.argv.put(0)
                        # Once approved, call pyfirmata code on arduino to change lights
                    if "Shooter" in recieved_message:
                        print("Alerting Public Safety there is a shooter")
                        message =  b"FORWARDING EMERGENCY FROM HEADLESS CLIENT, Shooter"
                        # Make GUI Popup for verification
                        # Once approved, call pyfirmata code on arduino to change lights
                        self.argv.put(2)
                        #self.alert_client_2(message)
            else:
                print("closing connection to")
                sel.unregister(sock)
                sock.close()
        # Writing data back to the client that sent the message
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                custom_message = "I got your message - love server"
                data.outb = custom_message.encode()
                #print("echoing", repr(data.outb), "to client", data.addr)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

    def main():

        argv = Queue()

        host = "192.168.2.50"
        port = 65433
        server = Server(host, port, argv)
        server.init_sockets_and_listen()
        try:
            while True:
                events = sel.select(timeout=None) # blocks until sockets are ready for I/O, then populates list of events for each socket
                for key, mask in events:
                    if key.data is None: # data is from a listening socket, we need to accept the connection and register it with the socket
                        server.accept_wrapper(key.fileobj)
                    else: # client has already been registered with the socket, we can service the connection and see what it contains
                        server.service_connection(key, mask)
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            sel.close()

if __name__ == '__main__':
    Server.main()
