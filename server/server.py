import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    #Reading data from the accepted message, see what type of emergency_type it is
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
            recieved_message = str(data.outb)
            print("Got message from client:", str(data.outb))

            if "Fire" in recieved_message:
                print("Alerting Public Safety there is a fire")
                # Make GUI Popup for verification
                # Once approved, call pyfirmata code on arduino to change lights
            if "Shooter" in recieved_message:
                print("Alerting Public Safety there is a shooter")
                # Make GUI Popup for verification
                # Once approved, call pyfirmata code on arduino to change lights

        else:
            print("closing connection to", data.addr)
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
    host = "127.0.0.1"
    port = 65432
    num_conns = 1

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    print("listening on", (host, port))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()

if __name__ == "__main__":
    main()
