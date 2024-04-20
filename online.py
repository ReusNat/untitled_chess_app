import threading
from queue import Queue
from socket import *
from constants import *
from common import *

color = ''
isTurn = False
msg_queue = Queue()
serverMsg = ''


def get_message(conn):
    msg = conn.recv(5).decode().rstrip()
    msg_queue.put(msg)


def listen():
    global serverMsg
    while True:
        try:
            res = msg_queue.get(block=False)
            break
        except:
            import time
            time.sleep(0.1)
            pass

    serverMsg = res


def handle_listen(conn):
    threading.Thread(target=get_message, args=[conn]).start()
    listen()


def get_line(conn):
    msg = b''
    while True:
        ch = conn.recv(1)
        msg += ch
        if ch == b'\n' or len(ch) == 0:
            break
    return msg.decode()


def white_castle(square):
    if square == 'g1':
        for piece in allPieces:
            if piece.name == 'w_h_rook':
                coords = common.get_coords('f1')
                pos = [0, 0]
                pos[0] = coords[0] - 45
                pos[1] = coords[1] - 45
                piece.move_sprite(pos)
                break
    elif square == 'c1':
        for piece in allPieces:
            if piece.name == 'w_a_rook':
                coords = common.get_coords('d1')
                pos = [0, 0]
                pos[0] = coords[0] - 45
                pos[1] = coords[1] - 45
                piece.move_sprite(pos)
                break


def black_castle(square):
    if square == 'g8':
        for piece in allPieces:
            if piece.name == 'b_h_rook':
                coords = common.get_coords('f8')
                pos = [0, 0]
                pos[0] = coords[0] - 45
                pos[1] = coords[1] - 45
                piece.move_sprite(pos)
                break
    elif square == 'c8':
        for piece in allPieces:
            if piece.name == 'b_a_rook':
                coords = common.get_coords('d8')
                pos = [0, 0]
                pos[0] = coords[0] - 45
                pos[1] = coords[1] - 45
                piece.move_sprite(pos)
                break


def online_game():
    global color, isTurn, serverMsg
    isTurn = False

    try:
        clientSock = socket(AF_INET, SOCK_STREAM)
        clientSock.connect(('127.0.0.1', 8086))
    except ConnectionRefusedError:
        print('Connection refused')
        exit(1)

    # print(f'client connected {clientSock}')
    # color = get_line(clientSock).rstrip()
    color = clientSock.recv(2).decode().rstrip()
    if 'w' in color:
        isTurn = True

    connected = True
    global running, pieceClicked, clickedPiece, clickedSquare

    legal_moves_lst = []
    while running and connected:
        if not isTurn:
            # print('Not your turn, waiting for move')
            # serverMsg = get_line(clientSock).rstrip()
            # serverMsg = clientSock.recv(5).decode().rstrip()
            handle_listen(clientSock)
            if serverMsg == '':
                continue

            # print(f'{serverMsg=}')
            if 'disc' in serverMsg:
                connected = False
            else:
                for piece in allPieces:
                    pieceSquare = common.ident_square(piece.rect.x, piece.rect.y)
                    if pieceSquare == serverMsg[0:2]:
                        piece.move_to(serverMsg[2:4])

                        if piece.name == 'w_king' and (serverMsg[2:4] == 'g1' or serverMsg[2:4] == 'c1'):
                            white_castle(piece)
                        elif piece.name == 'b_king' and (serverMsg[2:4] == 'g8' or serverMsg[2:4] == 'c8'):
                            black_castle(piece)

                        for _piece in allPieces:
                            _pieceSquare = common.ident_square(_piece.rect.x, _piece.rect.y)
                            if _piece != piece and _pieceSquare == serverMsg[2:4]:
                                _piece.kill()

                        isTurn = True
                        break
                serverMsg = ''
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                clientSock.send('exit\n'.encode())
                clientSock.close()
                break

            # print(f'{isTurn=}')
            if event.type == pygame.MOUSEBUTTONDOWN and isTurn:
                clickPos = event.pos
                square = common.ident_square(clickPos[0], clickPos[1])
                legal_moves_lst = []

                if pieceClicked and square != clickedSquare:
                    pieceClicked = False
                    clientSock.send((clickedSquare+square+'\n').encode())
                    # if get_line(clientSock).rstrip() != '1':
                    if clientSock.recv(2).decode().rstrip() != '1':
                        print('bad move')
                    else:
                        print('good move')

                    if clickedPiece.move_to(square):
                        if 'w_king' == clickedPiece.name \
                                and (square == 'g1' or square == 'c1'):
                            white_castle(square)
                        elif 'b_king' == clickedPiece.name \
                                and (square == 'g8' or square == 'c8'):
                            black_castle(square)
                        for piece in allPieces:
                            if (piece != clickedPiece
                                    and piece.rect.collidepoint(clickPos[0], clickPos[1])):
                                piece.kill()
                                break
                        isTurn = False
                else:
                    # print(square)
                    for piece in allPieces:
                        if (piece.rect.collidepoint(clickPos[0], clickPos[1])
                                and piece.color == color):
                            legal_moves_lst = list(filter(lambda x: square in x, [
                                board.uci(move)
                                for move in board.legal_moves
                            ]))

                            for i in range(len(legal_moves_lst)):
                                legal_moves_lst[i] = legal_moves_lst[i][2:]

                            # print(legal_moves_lst)
                            # print(f'{piece.name=}')
                            pieceClicked = True
                            clickedPiece = piece
                            clickedSquare = square
                            break

        # Draw Stuff
        screen.fill(WHITE)

        common.draw_board()
        allPieces.draw(constants.screen)
        for legal_square in legal_moves_lst:
            pygame.draw.circle(screen, 'white', common.get_coords(legal_square), 40)

        outcome = board.outcome()
        if outcome is not None:
            # print(board.result())
            pygame.draw.rect(screen, 'white', pygame.Rect(295, 490, 400, 75))
            if board.result() == '1-0':
                white_win = win_font.render('White Wins', True, 'black')
                screen.blit(white_win, [300, 500])
            elif board.result() == '0-1':
                black_win = win_font.render('Black Wins', True, 'black')
                screen.blit(black_win, [300, 500])
            else:
                draw = win_font.render('Draw', True, 'black')
                screen.blit(draw, [300, 500])

        pygame.display.flip()
        clock.tick(20)


if __name__ == '__main__':
    online_game()
    pygame.quit()
