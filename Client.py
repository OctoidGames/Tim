import socket
import threading


HEADER = 64
PORT = 14677
SERVER = "45.76.62.81"
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "UwU I'm sowwy, buwt I gowtta go now~~"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message=msg.encode(FORMAT) # encodes message to bytes
    msg_length = len(message) # finds length
    send_length = str(msg_length).encode(FORMAT) # encodes length
    send_length += b" " * (HEADER-len(send_length)) # pads length to fill HEADER
    client.send(send_length) #sends length
    client.send(message) # sends message
    print(f"[MESSAGE SENT] {msg}")
    #print("[LISTENING] client listening")
    msg_length = client.recv(HEADER).decode(
        FORMAT)  # Waits for message from client telling how long the next message will be (must be length 64 bytes)
    if msg_length:
        msg_length = int(msg_length)  # Converts received message length to usable format
        msg = client.recv(msg_length).decode(FORMAT)  # Waits for message
        print(f"[MESSAGE] '{msg}'")

#send("Hello World")

#send(DISCONNECT_MESSAGE)

while(1==1):
    msg=input("Tell Tim:")
    if not msg == "x":
        send(msg)
    else:
        send(DISCONNECT_MESSAGE)

