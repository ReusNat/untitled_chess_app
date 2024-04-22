import constants
import Piece

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8']


def ident_square(_x, _y):
    # If click is outside board, return None 
    if _x < 50 or _x > 850:
        return None
    if _y < 100 or _y > 900:
        return None
    
    _square = ''
    
    # Get the column
    if 50 <= _x < 150:
        _square = _square + 'a'
    elif 150 <= _x < 250:
        _square = _square + 'b'
    elif 250 <= _x < 350:
        _square = _square + 'c'
    elif 350 <= _x < 450:
        _square = _square + 'd'
    elif 450 <= _x < 550:
        _square = _square + 'e'
    elif 550 <= _x < 650:
        _square = _square + 'f'
    elif 650 <= _x < 750:
        _square = _square + 'g'
    elif 750 <= _x < 850:
        _square = _square + 'h'

    # Get the row
    if 100 <= _y < 200:
        _square = _square + '8'
    elif 200 <= _y < 300:
        _square = _square + '7'
    elif 300 <= _y < 400:
        _square = _square + '6'
    elif 400 <= _y < 500:
        _square = _square + '5'
    elif 500 <= _y < 600:
        _square = _square + '4'
    elif 600 <= _y < 700:
        _square = _square + '3'
    elif 700 <= _y < 800:
        _square = _square + '2'
    elif 800 <= _y < 900:
        _square = _square + '1'
    
    if _square == '':
        return 'I have no idea man'
    else:
        return _square


def get_coords(_square):
    if _square[0].upper() not in letters or _square[1] not in numbers:
        return None
    
    _x = 0
    _y = 0

    # Set the x coord
    if _square[0].lower() == 'a':
        _x = 100
    elif _square[0].lower() == 'b':
        _x = 200
    elif _square[0].lower() == 'c':
        _x = 300
    elif _square[0].lower() == 'd':
        _x = 400
    elif _square[0].lower() == 'e':
        _x = 500
    elif _square[0].lower() == 'f':
        _x = 600
    elif _square[0].lower() == 'g':
        _x = 700
    elif _square[0].lower() == 'h':
        _x = 800

    # set the y coord
    if _square[1] == '1':
        _y = 850
    elif _square[1] == '2':
        _y = 750
    elif _square[1] == '3':
        _y = 650
    elif _square[1] == '4':
        _y = 550
    elif _square[1] == '5':
        _y = 450
    elif _square[1] == '6':
        _y = 350
    elif _square[1] == '7':
        _y = 250
    elif _square[1] == '8':
        _y = 150
        
    return _x, _y


def draw_board():
    # Draw Stuff
    constants.screen.fill('white')

    # This section just draws the board in the two-tone tan squares
    Piece.pygame.draw.rect(constants.screen, 'black', Piece.pygame.Rect(48, 98, 804, 804), 2)
    Piece.pygame.draw.rect(constants.screen, constants.LIGHT_TAN, Piece.pygame.Rect(50, 100, 800, 800))
    for y in range(0, 8, 2):
        for x in range(0, 8, 2):
            Piece.pygame.draw.rect(constants.screen, constants.DARK_TAN, Piece.pygame.Rect(
                50 + constants.SQUARE_SIZE * y, 800 - constants.SQUARE_SIZE * x, constants.SQUARE_SIZE,
                constants.SQUARE_SIZE))
            Piece.pygame.draw.rect(constants.screen, constants.DARK_TAN, Piece.pygame.Rect(
                150 + constants.SQUARE_SIZE * y, 700 - constants.SQUARE_SIZE * x, constants.SQUARE_SIZE,
                constants.SQUARE_SIZE))

    # The next 2 for loops display the row and column markers outside the board
    i = 0
    for letter in letters:
        text = constants.font.render(letter, True, 'black')
        constants.screen.blit(text, [100 + 100 * i, 910])
        i += 1

    i = 0
    for number in numbers:
        text = constants.font.render(number, True, 'black')
        constants.screen.blit(text, [25, 850 - 100 * i])
        i += 1
