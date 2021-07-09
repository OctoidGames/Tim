import socket
import threading
import requests
import wikipedia


HEADER = 64
PORT = 14677
SERVER = ''
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "UwU I'm sowwy, buwt I gowtta go now~~"

Alts = {}

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def extract_alts():
    f=open('Alts.txt','r')
    for x in f:
        wrd = ""
        msgList = []
        for a in range(len(x)):
            chr = x[a]
            if not chr == "\n":
                if not chr == " ":
                    wrd += chr
                else:
                    msgList.append(wrd)
                    wrd = ""
        msgList.append(wrd)
        Alts.update({msgList[0]:msgList})


def handle_message(msg):
    msgList = []
    wrd = ""
    for a in range(len(msg)):
        chr = msg[a]
        if not chr == " ":
            wrd+=chr
        else:
            msgList.append(wrd)
            wrd = ""
    msgList.append(wrd)
    print("thinking. . . ")

    command = msgList[0]
    cmd=""
    for cmd in Alts:
        if command in Alts[cmd]:
            command = cmd

    if cmd == "x":
        pass

    if cmd == "Find":
        pass

    if cmd == "Search":
        term = ""
        for a in msgList:
            if not a == msgList[0]:
                term += a+" "
        results = wikipedia.search(term)
        if results == []:
            return "No results found"
        #print(results)
        try:
            page = wikipedia.page(results[0])
            sum = wikipedia.summary(results[0], sentences=2)

            try:
                extra = f"did you mean: {results[1]}, {results[2]}, or {results[3]}"
            except:
                extra = ""

            result = page.title + "\n" + sum + "\n" + page.url + "\n" + extra
            return result
        except:
            return "something went wrong, maybe your serch term was an initialism"


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
                connected = False
                break               # Closes loop
            else:
                print(f"[MESSAGE] from @{addr}: '{msg}'")
                REPLY = handle_message(msg)
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


extract_alts()
print("[STARTING] setting up personal tweaks")
print("[STARTING] server is starting at",ADDR)
start()
