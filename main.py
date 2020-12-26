import time
from random import randint
import curses
import game
from ai import *


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


def score_move(old_state, new_state, old_end, new_end, old_snake_score, new_snake_score):
    c = -999999999999999
    b = -1
    a = -4
    old_score = old_state[4]*a + b + old_end*c
    new_score = new_state[4]*a + b + new_end*c
    delta_score = new_score - old_score

    return delta_score


def get_move(state=None):
    r = randint(0, 3)
    if r == 0:
        return curses.KEY_UP
    elif r == 1:
        return curses.KEY_DOWN
    elif r == 2:
        return curses.KEY_LEFT
    elif r == 3:
        return curses.KEY_RIGHT


def choose_move(arr):
    score_max = 0
    right_move = 258
    for move in arr.keys():
        score = score_move(arr[move][0],arr[move][1],arr[move][2],arr[move][3],arr[move][4],arr[move][5])
        if score_max < score:
            score_max = score
            right_move = move

    return right_move


def decode_move(m):
    if m == 258:
        return "curses.KEY_DOWN"
    if m == 259:
        return "curses.KEY_UP"
    if m == 260:
        return "curses.KEY_LEFT"
    if m == 261:
        return "curses.KEY_RIGHT"


if __name__ == '__main__':

    dataset = []
    i = 0
    """
    while i < 2000:    

        
        snake_game = game.Game(10, 30, 200, i)
        if snake_game is None:
            print("game is None")
        snake_game.render_init()

        snake_game.clear()
        while snake_game.end is False:
            snake_game.render()
            state = snake_game.state
            #key = get_move(ai, state)
            #key = get_move()
            key = snake_game.win.getch()
            snake_game.key = key
            snake_game.win.refresh()
            snake_game.win2.refresh()
            snake_game.win.timeout(0)
            g = snake_game.win.getch()
            if g == 113:
                snake_game.gameover()
            curses.napms(snake_game.pause)
            old_state = snake_game.state
            old_end = snake_game.end
            old_snake_score = snake_game.score
            snake_game.tick()
            new_state = snake_game.state
            new_snake_score = snake_game.score
            new_end = snake_game.end
            score_ = score_move(old_state, new_state, new_end, old_end, old_snake_score, new_snake_score)
            dataset.append((old_state, new_state, new_end, old_end, old_snake_score, new_snake_score, score_, key))
       
        i += 1
        
        
        
        """

    snake_game = game.Game(10, 30, 200, 0)
    if snake_game is None:
        print("game is None")
    snake_game.render_init()
    snake_game.clear()
    moves = [258, 259, 260, 261]
    arr = []
    while snake_game.end is False:
        snake_game.render()
        res = dict()
        for move in moves:
            res[move] = snake_game.simulate_move(move)
            print("move: " + str(decode_move(move)))
        right_move = choose_move(res)
        print("right_move: " + str(decode_move(right_move)))
        snake_game.key = right_move
        snake_game.win.refresh()
        snake_game.win2.refresh()
        snake_game.win.timeout(0)
        g = snake_game.win.getch()
        if g == 113:
            snake_game.gameover()
        curses.napms(snake_game.pause)
        snake_game.tick()
        dataset.append((right_move, res[right_move]))

    curses.endwin()
    """
    f = open("./dataset.txt", "w+")
    for i in range(len(dataset)):
        f.write(str(dataset[i])+"\n")
    f.close()
    """

    """
    f = open("./dataset.txt", "r")
    content = f.read()
    #print("Dataset creation...")
    #x, y = create_dataset(1000)
    x = content[]
    ai = ai(500)
    ai.data_segregation(x, y)
    #print("Train...")
    ai.train()
    #print("Evaluation...")
    score = ai.evaluation()
    print("Score: " + str(score))
    """











