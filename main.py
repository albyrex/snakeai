import time
from random import randint
import curses
import game
from ai import *
import keyboard

def get_move(ai, state):
    r = ai.trained_model.predict([state])
    if r == 0:
        return curses.KEY_UP
    elif r == 1:
        return curses.KEY_DOWN
    elif r == 2:
        return curses.KEY_LEFT
    elif r == 3:
        return curses.KEY_RIGHT


def create_dataset(n):
    data = dict()
    data["data"] = []
    data["target"] = []
    for i in range(n):
        elem = (randint(0, 1), randint(0, 1), randint(0, 1), randint(0, 1))
        data["data"].append(elem)
        put = False
        for y in range(len(elem)):
            if elem[y] == 1:
                data["target"].append(y)
                put = True
                break
        if put == False:
            data["target"].append(-1)
    return data["data"], data["target"]



def score_move(old_state, new_state, end, new_snake_score, old_snake_score):
    delta_d = old_state[4] - new_state[4]
    delta_score = old_snake_score - new_snake_score
    c = -999999999999999
    b = 1
    a = -1
    old_score = old_state[4]*a + old_state[5]*b + old_end*c
    new_score = new_state[4]*a + new_state[5]*b + new_end*c
    delta_score = new_score - old_score
    return delta_score

if __name__ == '__main__':
    dataset = []
    print("Dataset creation...")
    x, y = create_dataset(1000)
    ai = ai(500)
    ai.data_segregation(x, y)
    print("Train...")
    ai.train()
    print("Evaluation...")
    score = ai.evaluation()
    print("Score: " + str(score))

    game = game.Game(10, 30, 200)
    game.render_init()

    game.clear()
    while game.end is False:
        game.render()
        state = game.state
        key = get_move(ai, state)
        game.key = key
        game.win.refresh()
        game.win2.refresh()
        game.win.timeout(0)
        g = game.win.getch()
        if g == 113:
            game.gameover()
        curses.napms(game.pause)
        game.tick()
        new_state = game.state
        end = game.end
        score_move = score_move(new_state, end)

    print(game.score)














