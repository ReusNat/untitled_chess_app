from socket import *
import threading
import chess

board = chess.Board


def get_line(conn):
    msg = b''
    while True:
        ch = conn.recv(1)
        msg += ch
        if ch == b'\n' or len(ch) == 0:
            break
        
    return msg.decode()


serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSock.bind(('', 0))
serverSock.listen(2)
SOCKNAME = f'{serverSock.getsockname()[0]}:{serverSock.getsockname()[1]}'

print(f'Server running on: {SOCKNAME}')

connectedUsers = [("", 0000), ("", 0000)]


def handle_client(connInfo):
    global connectedUsers
    if connectedUsers[0][0] == "":
        connectedUsers[0] = connInfo
        serverSock.send()
    else:
        connectedUsers[1] = connInfo
    connected = True
    while connected:
        message = get_line(connInfo[0]).rstrip()
        if 'exit' in message:
            connected = False
        print(message)


running = True
while running:
    try:
        threading.Thread(target=handle_client,
                         args=(serverSock.accept(),),
                         daemon=True).start()
    except KeyboardInterrupt:
        print("\n[Shutting Down]")
        running = False
