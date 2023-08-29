import socket
import threading


IP = "localhost"
PORT = 4455 # socket IN
PORT2 = 4444 #socket OUT
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"



def handle_client(conn, addr):
    def sendIN(msg):
        print(type(msg))
        conn.send(msg)


    def sendOUT(msg):
        print(type(msg))
        tunel.sendall(msg.encode(FORMAT)) # msg.encode(FORMAT)

    def listenIN():
        msg = conn.recv(SIZE).decode(FORMAT)
        print(f"[ IN => OUT ] [{addr}] {msg}\n")
        sendOUT(msg)

    def listenOUT():
        msg = tunel.recv(1024)
        print(f"[ IN <= OUT ] [{addr}] {msg}\n")
        sendIN(msg)


    print(f"[NEW CONNECTION] {addr} connected.")

    print("[STARTING] TUNNEL is starting...")
    tunel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tunel.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tunel.connect((IP,PORT2))
    #tunel.sendall(msg)
    #data = tunel.recv(1024)
    connected = True
    thIN = threading.Thread(target=listenIN, args=())
    thOUT = threading.Thread(target=listenOUT, args=())
    thIN.start()
    thOUT.start()
    while connected:
        thIN = threading.Thread(target=listenIN, args=())
        thOUT = threading.Thread(target=listenOUT, args=())
        thIN.start()
        thOUT.start()
        #msg = conn.recv(SIZE).decode(FORMAT) # wait for message of client
        #msg = tunel.recv(1024)
        #print(f"[{addr}] {msg}") # print to proxy server the message from client
        #msg = f"Msg received: {msg}" # msg to client
        #conn.send(msg.encode(FORMAT)) # send to client from server

        #tunel.sendall(f"[CLIENT] {msg}".encode(FORMAT)) # send to final target
    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()


