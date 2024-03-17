import pygame.rect
from constants import *


class Button:
    def __init__(self, text, x_pos, y_pos, width, height, font,
                 _screen, _board=None):
        self.text = text
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.font = font
        self.screen = _screen
        self.draw()
        self.board = _board

    def draw(self):
        text = self.font.render(self.text, True, BLACK)
        button_rect = pygame.rect.Rect((self.x, self.y), (self.width, self.height))
        if self.check_clicked():
            pygame.draw.rect(self.screen, 'dark red', button_rect, 0, 5)
        else:
            pygame.draw.rect(self.screen, 'red', button_rect, 0, 5)
        pygame.draw.rect(self.screen, 'black', button_rect, 2, 5)
        self.screen.blit(text, (self.x, self.y))

    def check_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x, self.y), (self.width, self.height))
        if left_click and button_rect.collidepoint(mouse_pos):
            self.board.reset()
            make_all_pieces()
            return True
        else:
            return False
