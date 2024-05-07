from socket import *
import threading
import chess

# This server file handles the handshake between the two clients ensuring the clients don't interact directly with
# one another directly as well as validate the moves each client makes.

board = chess.Board()


def get_line(conn):  # handy little function that just keeps trying to read
    msg = b''        # a byte from socket until it gets a \n or nothing
    while True:
        ch = conn.recv(1)
        msg += ch
        if ch == b'\n' or len(ch) == 0:
            break
        
    return msg.decode()


serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
try:  # This try/except section handles a miss-formatted config.txt file
    with open('config.txt', 'r') as f:
        ip = f.readline().split(':')[1].rstrip()
        port = int(f.readline().split(':')[1])
        f.close()
except ValueError:
    print('Invalid port or IP address')
    print('Make sure format of config.txt is formatted like the following:\nIP:127.0.0.1\nPort:8085\n')
    exit(1)

serverSock.bind((ip, port))
serverSock.listen(2)
SOCK_NAME = f'{serverSock.getsockname()[0]}:{serverSock.getsockname()[1]}'

print(f'Server running on: {SOCK_NAME}')

connectedUsers: list[tuple[socket, str]] = []


def handle_client(connInfo):  # Function called by each thread to handle communicating to each client on its own thread
    global connectedUsers, board
    clientConn, clientAddr = connInfo
    print(f'connection from {clientAddr}')
    white = True

    if not connectedUsers:
        clientConn.send('w\n'.encode())
    else:
        white = False
        clientConn.send('b\n'.encode())

    connectedUsers.append((clientConn, clientAddr))

    while True:  # This loop just keeps the hand off going until the end of the game or until one client disconnects
        message = clientConn.recv(5).decode().rstrip()
        print(f'{message=}')
        if 'exit' in message:
            if white:
                connectedUsers[1][0].send('disc\n'.encode())
                connectedUsers.pop(0)
            else:
                connectedUsers[0][0].send('disc\n'.encode())
                connectedUsers.pop(1)
            break

        move = chess.Move.from_uci(message)
        if move in board.legal_moves:
            board.push(move)
            print('-'*15)
            print(board)
            print('-'*15)
            if white:
                try:
                    clientConn.send('1\n'.encode())
                    connectedUsers[1][0].send(message.encode())
                except IndexError:
                    print('Only one user connected!')
            else:
                clientConn.send('1\n'.encode())
                connectedUsers[0][0].send(message.encode())
        else:
            clientConn.send('0\n'.encode())


running = True
while running:  # This while true keeps running waiting for users to connect and when they do it calls handle_client
    try:
        threading.Thread(target=handle_client,
                         args=(serverSock.accept(),),
                         daemon=True).start()
    except KeyboardInterrupt:
        print("\n[Shutting Down]")
        if connectedUsers:
            for user in connectedUsers:
                user[0].send('disc\n'.encode())
        running = False
