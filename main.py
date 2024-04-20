from offline import *
from online import *

title_txt = 'Untitled Chess App'
button_font = pygame.font.Font(None, 50)
title_font = pygame.font.Font(None, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    screen.fill('white')
    title = title_font.render(title_txt, True, 'black')
    screen.blit(title, [150, 100])
    offline_button = Button.Button('Offline Game', 500, 300, 200, 100, font, screen)
    online_button = Button.Button('Online Game', 500, 450, 200, 100, font, screen)

    if offline_button.check_clicked():
        offline_game()

    if online_button.check_clicked():
        try:
            online_game()
        except:
            pass

    offline_button.draw()
    online_button.draw()
    pygame.display.flip()
    clock.tick(20)


pygame.quit()
