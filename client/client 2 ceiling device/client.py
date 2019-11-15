# client for ceiling device
# recieve authorized emergency_type from server
# send emergency_type to arduino by writing to arduino pins

# monitor smoke detector
# listen to arduino

#!/usr/bin/env python3

#Any message from this client sent to server is trusted, no confirm needed

import sys
import socket
import selectors
import types
#from gpio_pins import CeilingDeviceGPIO
from threading import Thread
from queue import Queue



class Client:

    def __init__(self,server_address, server_port, sel):
        self.server_address = server_address
        self.server_port = server_port
        self.sel = sel
        self.server = None
        self.client_socket = None

    def start_connections(self, host, port, num_conns, message):
        server_addr = (host, port)
        for i in range(0, num_conns):
            connid = i + 1
            print("starting connection", connid, "to", server_addr)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.connect_ex(server_addr)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(
                connid=connid,
                msg_total= 1,
                recv_total=0,
                messages=message,
                outb=b"",
            )
            self.sel.register(sock, events, data=data)
            sock.send(data.messages)


    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data

        # Got message from server
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
                recieved_message = str(data.outb)
                print("Got message from server:", str(data.outb))

                if "Fire" in recieved_message:
                    print("Fire alert recieved from server")
                    # write to arduino saying fire
                if "Shooter" in recieved_message:
                    print("Shooter alert recieved from server")
                    # write to arduino saying shooter

            if not recv_data:
                print("closing connection")
                self.sel.unregister(sock)
                sock.close()



    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read

        if addr[0] == self.server_addr:
            print("accepted connection from", addr)
            self.server = conn
            self.server.setblocking(False)



    def checkQueue(self,queue):
        print("starting queue check")
        while True:
            check = queue.get() # halts until something is in the queue
            if check == -1:
                break
            else:
                # Whenever something is added to the queue
                # communicate with server
                if check == 0:
                    print("Sending fire alert to server")
                    message = b"Fire alert recieved from ceiling device"
                    num_conns = 1
                    #self.start_connections("127.0.0.1", int(65433), int(num_conns), message)
                    self.server.send(message)


    def main():

        server_address = "192.168.2.52"
        server_port = "65433"
        sel = selectors.DefaultSelector()

        client = Client(server_address, server_port, sel)

        # connect to the server so it knows we exist
        client.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.client_socket.connect_ex((client.server_address, int(client.server_port)))

        # wait for response from server
        response = client.client_socket.recv(1024)

        if response:
            print(str(response))

        # setup a queue to communicate between the listening for smoke thread and this main thread
        queue = Queue()
        #gpio_object = CeilingDeviceGPIO(queue)

        # listen for the smoke detector in another thread
        #process = Thread(target=gpio_object.listen_for_smoke)
        #process.start()

        print("Listening for smoke")

        # start thread that checks for updates to the queue
        #check = Thread(target = client.checkQueue, args = (queue,))
        #check.daemon = True
        #check.start()


        host = "127.0.0.1"
        port = 65432
        num_conns = 1

        client.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.client_socket.bind((host, port))
        client.client_socket.listen()
        print("Ceiling device started")
        print("listening for messages from server on", (host, port))
        client.client_socket.setblocking(False)

        try:
            while True:
                events = client.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        client.accept_wrapper(key.fileobj)
                    else:
                        client.service_connection(key, mask)
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            sel.close()


if __name__ == "__main__":
    Client.main()
