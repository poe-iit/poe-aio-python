import sys
import socket
import selectors
import types
import threading
from queue import Queue

sel = selectors.DefaultSelector()

client_1_address = "127.0.0.1:65431"
client_2_ip = "127.0.0.1"
client_2_port = "65432"
client_2_sending_address = "('127.0.0.1', 65432)"

class Server:

    def __init__(self, host, port, argv):
        self.host = host
        self.port = port
        self.argv = argv


    # Registers and binds the sockets. Sets the socket to listen on the host and port to act as a server
    def init_sockets_and_listen(self):

        try:
            num_conns = 1
            lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            lsock.bind((self.host, self.port))
            lsock.listen()
            print("listening on", (self.host, self.port))
            lsock.setblocking(False)
            sel.register(lsock, selectors.EVENT_READ, data=None)
        except:
            print("could not init socket, retrying")
            self.init_sockets_and_listen()


    # Connects to a client with specified host and port with and sends custom message
    def start_connections(self, host, port, num_conns, message):
        try:
            # starts a new connection to client 2
            server_addr = (host, port)
            connid = 1
            print("starting connection", connid, "to", server_addr)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.connect_ex(server_addr)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(
                connid=connid,
                msg_total=1,
                recv_total=0,
                messages=message,
                outb=b"",
            )
            sel.register(sock, events, data=data)
            sock.send(data.messages)


        except BlockingIOError:
            #print("travis sucks at socket programming, caught blocking error, retrying")
            sock.close()
            self.start_connections(host, port, num_conns, message)


    # Sends emergency message to the ceiling device
    def alert_client_2(self, message):
        host = client_2_ip
        port  = client_2_port
        num_conns = 1
        self.start_connections(host, int(port), int(num_conns), message)


    # registers the new client with the socket
    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print("accepted connection from", addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)


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
                        self.alert_client_2(message)
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

    def main(argv):

        host = "127.0.0.1"
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

