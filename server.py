import socket
import threading
import requests


PublicIP = (requests.get('http://ip.42.pl/raw').text)
HEADER = 64
PORT = 14677
SERVER = PublicIP
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "UwU I'm sowwy, buwt I gowtta go now~~"


server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send(conn, addr, msg):
    message=msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER-len(send_length))
    conn.send(send_length)
    conn.send(message)
    print(f"[MESSAGE SENT] to {addr}: '{msg}'")


def handle_client(conn, addr):
    print("[CONNECTION STARTED] connection with",addr,"started successfully")
    connected=True
    while(connected): # Loops while connected to server
        msg_length = conn.recv(HEADER).decode(FORMAT) # Waits for message from client telling how long the next message will be (must be length 64 bytes)
        if msg_length:
            msg_length = int(msg_length) # Converts received message length to usable format
            msg = conn.recv(msg_length).decode(FORMAT) # Waits for message
            if msg == DISCONNECT_MESSAGE: # Checks for disconnect message
                connected = False # Closes loop
            print(f"[MESSAGE] from @{addr}: '{msg}'")
            REPLY = "message recieved"
            send(conn, addr, REPLY ) # sends conformation
    conn.close() # closes connection
    print("[INFO] Active conncetions:", threading.activeCount() - 2)


def start(): # handles new connections
    server.listen() # sets the sever to listen for new connections
    while(True):
        conn, addr = server.accept() # waits for new connection and sets conn to socket object of connection
        print("[NEW CONNECTION] @", addr)
        thread = threading.Thread(target=handle_client, args=(conn, addr))  # Creates new thread for connection
        thread.start()                                                      # Starts new thread
        print("[INFO] Active conncetions:", threading.activeCount()-1)


print("[STARTING] server is starting at",ADDR)
start()
