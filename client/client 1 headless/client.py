#!/usr/bin/env python3

import sys
import socket
import selectors
import types
#from button_read import Button

sel = selectors.DefaultSelector()



def start_connections(host, port, num_conns, message):
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
        sel.register(sock, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    # Got message from server
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print("received", repr(recv_data), "from connection", data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print("closing connection", data.connid)
            sel.unregister(sock)
            sock.close()
    # Writing message back to server
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print("sending", repr(data.outb), "to connection", data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

    else:
        print("closing connection to")
        sel.unregister(sock)
        sock.close()

def keep_connection_open():
    try:
        while True:
            events = sel.select(timeout=1)
            if events:
                for key, mask in events:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()



def main ():
    host = "127.0.0.1"
    port = 65433
    num_conns = 1
    print ("Headless client has started, waiting for button press")
    #emergency_type = Button.listen_for_press()
    emergency_type = 1

    print("Button Pressed")

    if emergency_type == 1:
        message = [b"Fire from headless client1"]
        #send message to server
        start_connections(host, int(port), int(num_conns), message)
        keep_connection_open()
    if emergency_type == 2:
        message = [b"Shooter from headless client1"]
        start_connections(host, int(port), int(num_conns), message)
        keep_connection_open()


if __name__ == "__main__":
    main()
