import pygame
import common
import chess

allPieces = pygame.sprite.Group()


class Piece (pygame.sprite.Sprite):
    def __init__(self, png_name, _board, _pieceName):
        pygame.sprite.Sprite.__init__(self)
        self.board = _board
        if '1' in png_name:
            self.color = 'b'
        else:
            self.color = 'w'

        self.name = _pieceName
        self.image = pygame.image.load(f'images/{png_name}')
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        
    def move_sprite(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
    def move_to(self, square):
        currSquare = common.ident_square(self.rect.x, self.rect.y)
        move = chess.Move.from_uci(currSquare + square)
        
        if move in self.board.legal_moves:
            coords = common.get_coords(square)
            self.rect.x = coords[0] - 45
            self.rect.y = coords[1] - 45
            self.board.push(move)
            return True
        else:
            return False
    