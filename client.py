import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.156"
ADDR = (SERVER,PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

print(f"Connected succesfully to [{SERVER}]")
print("Type !DISCONNECT to disconnect ...")

send("Hello from macbook :)")

while True:
    client_message = input("Input: ")
    send(client_message)

    if client_message == "!DISCONNECT":
        break
