import time
from random import randint
import curses
import game
from ai import *
import json
import pickle
import math

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
    distance_old = math.sqrt(old_state[4]**2 + old_state[5]**2)
    distance_new = math.sqrt(new_state[4] ** 2 + new_state[5] ** 2)
    #old_score = old_state[4]*a + b + old_end*c
    old_score = distance_old *a + b + old_end*c
    #new_score = new_state[4]*a + b + new_end*c
    new_score = distance_new * a + b + new_end * c
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
    score_max = None
    for move in arr.keys():
        score = score_move(arr[move][0],arr[move][1],arr[move][2],arr[move][3],arr[move][4],arr[move][5])
        if score_max is None or score_max < score:
            score_max = score
            right_move_ = move

    return right_move_


def decode_move(m):
    if m == 258:
        return "curses.KEY_DOWN"
    if m == 259:
        return "curses.KEY_UP"
    if m == 260:
        return "curses.KEY_LEFT"
    if m == 261:
        return "curses.KEY_RIGHT"

def encode_dataset(m):
    if m == 258:
        return -300
    if m == 259:
        return -100
    if m == 260:
        return +100
    if m == 261:
        return +300

def encode_move(m):
    m = round(m[0])
    if m == -300:
        return 258
    if m == -100:
        return 259
    if m == +100:
        return 260
    if m == +300:
        return 261

if __name__ == '__main__':
    """
    dataset = []
    i = 0
    speed = 1000
    while i < 1000:
        snake_game = game.Game(10, 30, speed, i)
        if snake_game is None:
            print("game is None")
        snake_game.render_init()
        snake_game.clear()
        moves = [258, 259, 260, 261]
        arr = []
        while snake_game.end is False:
            snake_game.render()
            snake_game.win.refresh()
            snake_game.win2.refresh()
            res = dict()
            for move in moves:
                res[move] = snake_game.simulate_move(move)
            right_move = choose_move(res)
            snake_game.key = right_move
            snake_game.win.refresh()
            snake_game.win2.refresh()
            snake_game.win.timeout(0)
            g = snake_game.win.getch()
            if g == 113:
                snake_game.gameover()
            if g == ord("s"):
                i = 1000
            if g == ord("v"):
                speed = int(speed / 10)
                snake_game.pause = speed
            curses.napms(snake_game.pause)
            snake_game.tick()
            snake_game.win.refresh()
            snake_game.win2.refresh()
            dataset.append((right_move, res[right_move][0]))
        i += 1

    curses.endwin()
    for i in range(len(dataset)):
        dataset[i] = (encode_dataset(dataset[i][0]), dataset[i][1])

    d = json.dumps(dataset)

    f = open("./dataset.txt", "w+")
    f.write(d)
    f.close()

    f = open("./dataset.txt", "r")
    r = f.read()
    dataset = json.loads(r)
    x = []
    y = []
    for el in dataset:
        y.append(el[0])
        x.append(tuple(el[1]))
    
    ai1 = ai(500)
    ai1.data_segregation(x, y)
    print("Training...")
    ai1.train()
    print("Evaluation...")
    score = ai1.evaluation()
    print("Score: " + str(score))

    dump = ai1.save()
    f = open("./ai.txt", "wb")
    f.write(dump)
    """
    ai2 = ai(500)
    f = open("./ai.txt", "rb")
    p = f.read()
    ai2.load(p)
    f.close()
    speed = 1000
    snake_game = game.Game(10, 30, speed, 0)
    if snake_game is None:
        print("game is None")
    snake_game.render_init()
    snake_game.clear()

    snake_game.snake = []
    snake_game.snake.append((2, 8))
    snake_game.snake.append((3, 8))
    snake_game.snake.append((4, 8))

    while snake_game.end is False:
        snake_game.render()
        snake_game.win.refresh()
        snake_game.win2.refresh()
        snake_game.key = (encode_move(ai2.trained_model.predict([tuple(snake_game.state)])))
        snake_game.win.refresh()
        snake_game.win2.refresh()
        snake_game.win.timeout(0)
        g = snake_game.win.getch()
        if g == ord("q"):
            snake_game.gameover()
        if g == ord("s"):
            i = 1000
        if g == ord("v"):
            speed = int(speed / 10)
            snake_game.pause = speed
        curses.napms(snake_game.pause)
        snake_game.tick()
        snake_game.win.refresh()
        snake_game.win2.refresh()

    curses.napms(5000)
    curses.endwin()



