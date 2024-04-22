import pygame.rect
from constants import *

# The button class makes it easier for all the buttons in the UI work effectively.
# The class also has the ability to store a function, but I ended up not needing that functionality


class Button:
    def __init__(self, text, x_pos, y_pos, width, height, _font,
                 _screen, _function=None):
        self.text = text
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.font = font
        self.screen = _screen
        self.draw()
        self.function = _function

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
            return True
        else:
            return False

    def run_function(self):
        self.function()
