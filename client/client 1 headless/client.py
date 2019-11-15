import sys
import socket
import selectors
import types
#from button_read import Button




class Client:

    def __init__(self,server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.server = None
        self.client_socket = None
        self.sel = selectors.DefaultSelector()



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
                sock.close()


    # Whenever someone tries to connect, we can use the conn and addr to check who it is
    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print("Accepted a connection from", addr)



    def main():

        server_address = "192.168.2.50"
        server_port = "65433"

        client = Client(server_address, server_port)

        # connect to the server so it knows we exist
        client.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.client_socket.connect_ex((client.server_address, int(client.server_port)))
        client.client_socket.send(b"hey")

        # wait for response from server
        response = client.client_socket.recv(1024)

        if response:
            print(str(response))

            print ("Headless client has started, waiting for button press")
            #emergency_type = Button.listen_for_press()
            emergency_type = 1

            print("Button Pressed")
            time.sleep(100)

            if emergency_type == 1:
                message = b"Fire from headless client1"
                #send message to server
                client.client_socket.sendall(message)
                print("Sent message to server")

        try:
            while True:
                events = client.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        client.accept_wrapper(key.fileobj)
                    else:
                        print("serviced connection")
                        client.service_connection(key, mask)
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")


if __name__ == "__main__":
    Client.main()
