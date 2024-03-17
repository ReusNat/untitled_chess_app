import threading
from socket import *
from constants import *

color = ''
isTurn = False


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


def ui():
    global running, pieceClicked, clickedPiece, clickedSquare, isTurn

    legal_moves_lst = []
    while running:
        outcome = board.outcome()
        if outcome is not None:
            print(outcome)
            board.reset()
            make_all_pieces()

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and isTurn:
                clickPos = event.pos
                square = common.ident_square(clickPos[0], clickPos[1])
                legal_moves_lst = []

                if pieceClicked and square != clickedSquare:
                    pieceClicked = False
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
                    print(square)
                    for piece in allPieces:
                        if (piece.rect.collidepoint(clickPos[0], clickPos[1])
                                and piece.color == color):
                            legal_moves_lst = list(filter(lambda x: square in x, [
                                board.uci(move)
                                for move in board.legal_moves
                            ]))

                            for i in range(len(legal_moves_lst)):
                                legal_moves_lst[i] = legal_moves_lst[i][2:]

                            print(legal_moves_lst)
                            print(f'{piece.name=}')
                            pieceClicked = True
                            clickedPiece = piece
                            clickedSquare = square
                            break

        # Draw Stuff
        screen.fill(WHITE)

        common.draw_board()
        for legal_square in legal_moves_lst:
            pygame.draw.circle(screen, 'white', common.get_coords(legal_square), 40)

        pygame.display.flip()
        clock.tick(20)


def online_game():
    global color, isTurn
    isTurn = False

    try:
        clientSock = socket(AF_INET, SOCK_STREAM)
        clientSock.connect(('127.0.0.1', 8085))
    except ConnectionRefusedError:
        print('Connection refused')
        exit(1)

    color = get_line(clientSock)
    if color == 'w':
        isTurn = True

    threading.Thread(target=ui, daemon=True).start()
    connected = True
    while connected:
        serverMessage = get_line(clientSock)
        if 'Connection Error' in serverMessage:
            connected = False
        else:
            message = input("message: ")
            if 'exit' in message:
                clientSock.send((message + '\n').encode())
                connected = False
