from constants import *
import Button
from common import *


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


def offline_game():
    global running, pieceClicked, clickedPiece, clickedSquare
    reset_button = Button.Button('Reset', 900, 100,
                                 100, 50, font, screen,
                                 lambda: [board.reset(), make_all_pieces()])
    legal_moves_lst = []
    while running:

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if reset_button.check_clicked():
                reset_button.run_function()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = event.pos
                square = common.ident_square(clickPos[0], clickPos[1])
                legal_moves_lst = []

                if square is not None and pieceClicked and square != clickedSquare:
                    pieceClicked = False
                    if clickedPiece.move_to(square):
                        if 'w_king' == clickedPiece.name \
                                and (square == 'g1' or square == 'c1'):
                            white_castle(square)
                        elif 'b_king' == clickedPiece.name\
                                and (square == 'g8' or square == 'c8'):
                            black_castle(square)
                        for piece in allPieces:
                            if piece != clickedPiece and piece.rect.collidepoint(clickPos[0], clickPos[1]):
                                piece.kill()
                                break
                else:
                    for piece in allPieces:
                        if piece.rect.collidepoint(clickPos[0], clickPos[1]):
                            legal_moves_lst = list(filter(lambda x: square in x, [
                                board.uci(move)
                                for move in board.legal_moves
                            ]))

                            for i in range(len(legal_moves_lst)):
                                legal_moves_lst[i] = legal_moves_lst[i][2:]

                            pieceClicked = True
                            clickedPiece = piece
                            clickedSquare = square
                            break

        common.draw_board()
        allPieces.draw(constants.screen)
        for legal_square in legal_moves_lst:
            pygame.draw.circle(screen, 'white', get_coords(legal_square), 40)
        reset_button.draw()

        outcome = board.outcome()
        if outcome is not None:
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
    offline_game()
    pygame.quit()
