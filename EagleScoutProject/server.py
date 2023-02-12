import socket
import threading


HEADER = 64
PORT = 5050
SERVER = "192.168.1.22"
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCCONECT_MSG = "!Disconnect!"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = false
        print(f"[{addr}] {msg}") 
    conn.close()
    
def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print("[STARTING] server is starting...")
start()  