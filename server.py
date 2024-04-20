from socket import *
import threading
import chess

board = chess.Board()


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
serverSock.bind(('', 8086))
serverSock.listen(2)
SOCK_NAME = f'{serverSock.getsockname()[0]}:{serverSock.getsockname()[1]}'

print(f'Server running on: {SOCK_NAME}')

connectedUsers = []


def handle_client(connInfo):
    global connectedUsers, board
    clientConn, clientAddr = connInfo
    print(f'connection from {clientAddr}')
    white = True

    if not connectedUsers:
        connectedUsers.append((clientConn, clientAddr))
        clientConn.send('w\n'.encode())
    else:
        white = False
        connectedUsers.append((clientConn, clientAddr))
        clientConn.send('b\n'.encode())

    connected = True
    while connected:
        message = get_line(connInfo[0]).rstrip()
        print(f'{message=}')
        if 'exit' in message:
            if white:
                connectedUsers.pop(0)
            else:
                connectedUsers.pop(1)
            connected = False
            break
        move = chess.Move.from_uci(message)
        if move in board.legal_moves:
            board.push(move)
            print('-'*15)
            print(board)
            print('-'*15)
            if white:
                try:
                    clientConn.send('0001'.encode())
                    connectedUsers[1][0].send(message.encode())
                except IndexError:
                    print('Only one user connected!')
            else:
                clientConn.send('0001'.encode())
                connectedUsers[0][0].send(message.encode())


running = True
while running:
    try:
        threading.Thread(target=handle_client,
                         args=(serverSock.accept(),),
                         daemon=True).start()
    except KeyboardInterrupt:
        print("\n[Shutting Down]")
        for user in connectedUsers:
            user[0].send('disc\n'.encode())
        running = False
