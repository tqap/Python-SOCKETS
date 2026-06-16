import socket
import threading

HEADER = 64
PORT = 5050
# SERVER = "192.168.1.165" # If you want to manually specify ip of server
SERVER = socket.gethostbyname(socket.gethostname()) # Automatically sets IP with your machine local IP
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# socket.socket makes a new socket
# First argument is the family (category): socket.AF_INET means we are using IPv4 addresses.
# Second argument is the type (protocol): socket.SOCK_STREAM means we are using TCP for a reliable data stream.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    # conn = the specific socket object for this client
    # addr = the IP address and port of this specific client
    print(f"[New Connection] {addr} connected.")

    connected = True
    while connected:
        # We first receive a fixed-length header that tells us how long the incoming message is.
        # Data comes in as bytes, so we .decode() it into a readable string.
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            
            # If the client actually sent a message (so msg_length isn't blank)
            if msg_length: 
                msg_length = int(msg_length)

                # Now we know exactly how many bytes to receive, so we don't grab too much or too little.
                msg = conn.recv(msg_length).decode(FORMAT)
                

                print(f"[{addr}] {msg}")
                # Disconnect the client, if we don't do this, the server might crash or keep a "ghost" connection open.
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                
        except ConnectionResetError:
            print(f"[-] {addr} lost connection")
            break

    # Always close the connection once the loop ends to free up network resources
    conn.close()
    print(f"Client [{addr}] has disconnected")
    print(f"[Active Connections] {threading.active_count() - 2}")



def start():
    server.listen()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[Active Connections] {threading.active_count() - 1}") #We do -1 because server is always listening which will count as a thread


print("Server is starting ...")
start()