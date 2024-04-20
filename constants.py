from Piece import *
import common
import pygame
import chess

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_TAN = (166, 123, 91)
LIGHT_TAN = (245, 222, 179)
WIDTH = 1000
HEIGHT = 1000
SIZE = (WIDTH, HEIGHT)
SQUARE_SIZE = 800//8

board = chess.Board()


def make_piece(imageName, _square, name):
    global board
    _piece = Piece(imageName, board, name)
    _coords = common.get_coords(_square)
    _piece.rect.x = _coords[0] - 45
    _piece.rect.y = _coords[1] - 45
    return _piece


def make_all_pieces():
    for piece in allPieces:
        piece.kill()

    w_a_pawn = make_piece('pawn.png', 'a2', 'w_a_pawn')
    allPieces.add(w_a_pawn)
    w_b_pawn = make_piece('pawn.png', 'b2', 'w_b_pawn')
    allPieces.add(w_b_pawn)
    w_c_pawn = make_piece('pawn.png', 'c2', 'w_c_pawn')
    allPieces.add(w_c_pawn)
    w_d_pawn = make_piece('pawn.png', 'd2', 'w_d_pawn')
    allPieces.add(w_d_pawn)
    w_e_pawn = make_piece('pawn.png', 'e2', 'w_e_pawn')
    allPieces.add(w_e_pawn)
    w_f_pawn = make_piece('pawn.png', 'f2', 'w_f_pawn')
    allPieces.add(w_f_pawn)
    w_g_pawn = make_piece('pawn.png', 'g2', 'w_g_pawn')
    allPieces.add(w_g_pawn)
    w_h_pawn = make_piece('pawn.png', 'h2', 'w_h_pawn')
    allPieces.add(w_h_pawn)

    w_a_rook = make_piece('rook.png', 'a1', 'w_a_rook')
    allPieces.add(w_a_rook)
    w_b_horsie = make_piece('knight.png', 'b1', 'w_b_horsie')
    allPieces.add(w_b_horsie)
    w_c_bishop = make_piece('bishop.png', 'c1', 'w_c_bishop')
    allPieces.add(w_c_bishop)
    w_queen = make_piece('queen.png', 'd1', 'w_queen')
    allPieces.add(w_queen)
    w_king = make_piece('king.png', 'e1', 'w_king')
    allPieces.add(w_king)
    w_f_bishop = make_piece('bishop.png', 'f1', 'w_f_bishop')
    allPieces.add(w_f_bishop)
    w_g_horsie = make_piece('knight.png', 'g1', 'w_g_horsie')
    allPieces.add(w_g_horsie)
    w_h_rook = make_piece('rook.png', 'h1', 'w_h_rook')
    allPieces.add(w_h_rook)

    b_a_pawn = make_piece('pawn1.png', 'a7', 'b_a_pawn')
    allPieces.add(b_a_pawn)
    b_b_pawn = make_piece('pawn1.png', 'b7', 'b_b_pawn')
    allPieces.add(b_b_pawn)
    b_c_pawn = make_piece('pawn1.png', 'c7', 'b_c_pawn')
    allPieces.add(b_c_pawn)
    b_d_pawn = make_piece('pawn1.png', 'd7', 'b_d_pawn')
    allPieces.add(b_d_pawn)
    b_e_pawn = make_piece('pawn1.png', 'e7', 'b_e_pawn')
    allPieces.add(b_e_pawn)
    b_f_pawn = make_piece('pawn1.png', 'f7', 'b_f_pawn')
    allPieces.add(b_f_pawn)
    b_g_pawn = make_piece('pawn1.png', 'g7', 'b_g_pawn')
    allPieces.add(b_g_pawn)
    b_h_pawn = make_piece('pawn1.png', 'h7', 'b_h_pawn')
    allPieces.add(b_h_pawn)

    b_a_rook = make_piece('rook1.png', 'a8', 'b_a_rook')
    allPieces.add(b_a_rook)
    b_b_horsie = make_piece('knight1.png', 'b8', 'b_b_horsie')
    allPieces.add(b_b_horsie)
    b_c_bishop = make_piece('bishop1.png', 'c8', 'b_c_bishop')
    allPieces.add(b_c_bishop)
    b_queen = make_piece('queen1.png', 'd8', 'b_queen')
    allPieces.add(b_queen)
    b_king = make_piece('king1.png', 'e8', 'b_king')
    allPieces.add(b_king)
    b_f_bishop = make_piece('bishop1.png', 'f8', 'b_f_bishop')
    allPieces.add(b_f_bishop)
    b_g_horsie = make_piece('knight1.png', 'g8', 'b_g_horsie')
    allPieces.add(b_g_horsie)
    b_h_rook = make_piece('rook1.png', 'h8', 'b_h_rook')
    allPieces.add(b_h_rook)


# Init Pieces
make_all_pieces()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Unnamed Chess App')

clock = pygame.time.Clock()
running = True
pieceClicked = False
clickedPiece = None
clickedSquare = ''
pygame.init()
font = pygame.font.Font(None, 30)
win_font = pygame.font.Font(None, 100)
