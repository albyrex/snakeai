import curses
from random import randint

class Game:
    def __init__(self, n_row, n_column, pause):
        self.food = (2, 5)
        self.end = False
        self.score = 100
        self.pause = pause
        self.n_row = n_row
        self.n_column = n_column
        self.snake = []
        self.key = -1
        self.win = ""

    def clear(self):
        self.score = 100
        self.end = False
        self.food = (2, 5)
        self.snake = []
        self.snake.append((2, 2))
        self.snake.append((3, 2))
        self.snake.append((2, 2))
        self.snake.append((4, 2))
        self.snake.append((2, 2))
        self.snake.append((5, 2))
        self.snake.append((2, 2))
        self.snake.append((6, 2))

    def render_init(self):
        curses.initscr()
        win = curses.newwin(self.n_row + 2, self.n_column + 2, 0, 0)
        win.timeout(self.pause)
        curses.noecho()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        win.keypad(True)
        win.leaveok(True)
        self.win = win
        self.clear()
        self.render()

    def render(self):
        self.win.erase()
        self.win.border()
        self.win.addstr(0, 2, 'Score : ' + str(self.score) + ' ')
        self.win.addstr(self.food[0], self.food[1], "ò", curses.color_pair(1))
        for point in self.snake[1:]:
            self.win.addch(point[0], point[1], 'o', curses.color_pair(2))

        x = self.snake[0][0] - self.snake[1][0]
        y = self.snake[0][1] - self.snake[1][1]
        c = '>'
        if x == 1 and y == 0:
            c = 'v'
        elif x == 0 and y == 1:
            c = '>'
        elif x == -1 and y == 0:
            c = '^'
        elif x == 0 and y == -1:
            c = '<'
        self.win.addch(self.snake[0][0], self.snake[0][1], c, curses.color_pair(2))


    def generate_food(self):
        if self.food == ():
            food = self.snake[0]
            while food in self.snake:
                food = (randint(1, self.n_row), randint(1, self.n_column))
        self.food = food

    def check_collision(self):
        if (
                self.snake[0] in self.snake[1:] or
                self.snake[0][0] == self.n_row + 1 or
                self.snake[0][0] == 0 or
                self.snake[0][1] == self.n_column + 1 or
                self.snake[0][1] == 0
        ):
            return True
        else:
            return False

    def generate_new_head(self):
        if self.key == curses.KEY_UP:
            new_point = (self.snake[0][0] - 1, self.snake[0][1])
        elif self.key == curses.KEY_RIGHT:
            new_point = (self.snake[0][0], self.snake[0][1] + 1)
        elif self.key == curses.KEY_DOWN:
            new_point = (self.snake[0][0] + 1, self.snake[0][1])
        elif self.key == curses.KEY_LEFT:
            new_point = (self.snake[0][0], self.snake[0][1] - 1)
        else:
            x = self.snake[0][0] - self.snake[1][0] + self.snake[0][0]
            y = self.snake[0][1] - self.snake[1][1] + self.snake[0][1]
            new_point = (x, y)

        self.snake.insert(0, new_point)

    def gameover(self):
        self.end = True
        print("END")

    def tick(self):
        self.generate_new_head()
        if self.snake[0] != self.food:
            self.snake.pop()
            self.score -= 1
        elif self.snake[0] == self.food:
            self.food = ()
            self.generate_food()
            self.score += 50

        collision = self.check_collision()
        if collision or self.score < 0:
            self.gameover()

    def start(self):
        self.clear()
        while self.end is False:
            self.render()
            self.key = self.win.getch()
            self.tick()
