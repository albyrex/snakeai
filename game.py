import curses
from random import randint
import time
import threading


class Game:
    def __init__(self, n_row, n_column, pause):
        self.food = []
        self.end = False
        self.score = 0
        self.last_id = 0
        self.pause = pause
        self.n_row = n_row
        self.n_column = n_column
        self.map = [n_row, n_column]
        self.snake = []
        self.absolute_direction = "up"
        self.key = -1

    def clear(self):
        self.score = 0
        self.end = False
        self.food = []
        self.food.append(2)
        self.food.append(5)
        self.snake = []
        self.snake.append((2, 2))
        self.snake.append((3, 2))
        self.snake.append((2, 2))
        self.snake.append((4, 2))
        self.snake.append((2, 2))
        self.snake.append((5, 2))
        self.snake.append((2, 2))
        self.snake.append((6, 2))
        self.absolute_direction = "up"
        self.key = -1

    def render_init(self):
        curses.initscr()
        win = curses.newwin(self.n_row + 2, self.n_column + 2, 0, 0)
        curses.curs_set(0)
        win.nodelay(1)
        win.timeout(200)
        self.win = win
        self.clear()
        self.render()

    def render(self):
        self.win.clear()
        self.win.border(0)
        self.win.addstr(0, 2, 'Score : ' + str(self.score) + ' ')
        self.win.addch(self.food[0], self.food[1], 'p')
        for i, point in enumerate(self.snake):
            if i == 0:
                self.win.addch(point[0], point[1], '#')
            else:
                self.win.addch(point[0], point[1], 'o')
        self.win.getch()


    def generate_food(self):
        if self.food is False:
            food = []
            while food in self.snake:
                food = [randint(1, self.n_row), randint(1, self.n_column)]
        return food

    def check_collision(self):
        if (self.snake[0] in self.snake[1:-1] or
                self.snake[0][0] == self.n_row + 1 or
                self.snake[0][0] == 1 or
                self.snake[0][1] == self.n_column + 1 or
                self.snake[0][1] == 1
        ):
            return True
        else:
            return False

    def generate_new_head(self, key):
        new_point = [self.snake[0][0], self.snake[0][1]]
        self.key = key
        if self.key == curses.KEY_UP:
            self.absolute_direction = "up"
            new_point[0] -= 1
        elif self.key == curses.KEY_RIGHT:
            self.absolute_direction = "right"
            new_point[1] += 1
        elif self.key == curses.KEY_DOWN:
            self.absolute_direction = "down"
            new_point[0] += 1
        elif self.key == curses.KEY_LEFT:
            self.absolute_direction = "left"
            new_point[1] -= 1

        if new_point != self.snake[0]:
            self.snake.insert(0, new_point)
        self.key = -1


    def gameover(self):
        self.end = True
        global stop_thread
        stop_thread = True
        print("END")

    def tick(self, key):
        self.generate_new_head(key)
        if self.snake[0] != self.food:
            self.snake.pop()
            self.score -= 1
        else:
            self.food = self.generate_food()
            self.score += 10
        collision = self.check_collision()
        if collision:
            self.gameover()




    def start(self):
        self.clear()
        while self.end is False:
            key = self.win.getch()
            self.tick(key)
            self.key = -1
            self.render()
            time.sleep(self.pause)
