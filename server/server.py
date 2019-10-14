import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()


client_1_address = "127.0.0.1:65431"
client_2_ip = "127.0.0.1"
client_2_port = "65432"
client_2_sending_address = "('127.0.0.1', 65432)"


def start_connections(host, port, num_conns, message):
    try:
        # starts a new connection to client 2
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
                msg_total=1,
                recv_total=0,
                messages=message,
                outb=b"",
            )
            sel.register(sock, events, data=data)
            sock.send(data.messages)

    except BlockingIOError:
        print("travis sucks at socket programming, caught blocking error, retrying")
        start_connections(host, port, num_conns, message)


def alert_client_2(emergency_type, sock , data):
    host = client_2_ip
    port  = client_2_port
    num_conns = 1
    message = b"FORWARDING EMERGENCY FROM HEADLESS CLIENT, Fire"
    start_connections(host, int(port), int(num_conns), message)


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(True)
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

            if "client1" in recieved_message:
                if "Fire" in recieved_message:
                    print("Alerting Public Safety there is a fire")
                    emergency_type = "fire"
                    alert_client_2(emergency_type, sock, data)
                    # Make GUI Popup for verification
                    # Once approved, call pyfirmata code on arduino to change lights
                if "Shooter" in recieved_message:
                    print("Alerting Public Safety there is a shooter")
                    emergency_type = "fire"
                    alert_client_2(emergency_type)
                    # Make GUI Popup for verification
                    # Once approved, call pyfirmata code on arduino to change lights


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
    host = "127.0.0.1"
    port = 65433
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
