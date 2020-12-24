import game
import time
from random import randint

if __name__ == '__main__':
    game = game.Game(10, 30, 200)
    game.render_init()
    game.start()



