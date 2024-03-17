from sys import argv
from offline import *
from online import *

if len(argv) >= 3 and argv[1] == 'online':
    online_game()
else:
    offline_game()
    
pygame.quit()
