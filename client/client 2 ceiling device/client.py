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
from gpio_pins import CeilingDeviceGPIO
from threading import Thread






class Client:

    def __init__(self,server_address, sel):
        self.server_address = server_address
        self.sel = sel

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
                msg_total=sum(len(m) for m in message),
                recv_total=0,
                messages=list(message),
                outb=b"",
            )
            self.sel.register(sock, events, data=data)


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
        # Writing message back to server
        #if mask & selectors.EVENT_WRITE:
            #if not data.outb and data.messages:
                #data.outb = data.messages.pop(0)
            #if data.outb:
                #print("sending", repr(data.outb), "to connection", data.connid)
                #sent = sock.send(data.outb)  # Should be ready to write
                #data.outb = data.outb[sent:]



    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print("accepted connection from", addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)



    def main():

        server_address = "127.0.0.1:65433"
        sel = selectors.DefaultSelector()
        client = Client(server_address, sel)

        ceiling_client = CeilingDeviceGPIO.init() # init GPIO pins on device

        # listen for the smoke detector in another thread
        process = Thread(target=ceiling_client.listen_for_smoke)
        process.start()

        print("Listening for smoke")

        host = "127.0.0.1"
        port = 65432
        num_conns = 1

        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        print("Ceiling device started")
        print("listening for messages from server on", (host, port))
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = sel.select(timeout=None)
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
