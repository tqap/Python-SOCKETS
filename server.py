import socket
import threading

HEADER = 64
PORT = 5050
# SERVER = "192.168.1.165" # To manually specify ip of server
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
    print(f"[New Connection] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        #disconnect the user or next time he tries connecting, it might look like he already has connection with server
        if msg == DISCONNECT_MESSAGE:
            connected = False
        
        print(f"[{addr}] {msg}")
        
    conn.close()



def start():
    server.listen()
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[Active Connections] {threading.activeCount() - 1}") #We do -1 because server is always listening which will count as a thread


print("Server is starting ...")
start()