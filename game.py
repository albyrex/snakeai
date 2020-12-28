import curses
from random import randint
import math


class Game:
    def __init__(self, n_row, n_column, pause, id):
        self.food = (2, 5)
        self.end = False
        self.score = 100
        self.pause = pause
        self.n_row = n_row
        self.n_column = n_column
        self.snake = []
        self.key = -1
        self.win = ""
        self.state = []
        self.win2 = ""
        self.id = id

    def clear(self):
        self.score = 100
        self.end = False
        self.food = (2, 5)
        self.snake = []
        self.snake.append((2, 2))
        self.snake.append((3, 2))
        self.snake.append((4, 2))
        self.snake.append((5, 2))
        self.snake.append((6, 2))
        self.state = []
        self.update_state()

    def render_init(self):
        curses.initscr()
        win = curses.newwin(self.n_row + 2, self.n_column + 2, 0, 0)
        # win.timeout(self.pause)
        curses.noecho()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        win.keypad(True)
        win.leaveok(True)
        self.win = win
        self.win2 = curses.newwin(5, self.n_column + 2, self.n_row + 3, 0)
        self.clear()
        self.render()

    def render(self):
        self.win2.erase()
        self.win2.border()
        self.win2.addstr(1, 2, str(self.state) + ": " + str(self.key))
        self.win2.addstr(3, 2, "id: " + str(self.id))
        # self.win2.timeout(self.pause)

        self.win.erase()
        # self.win.timeout(self.pause)
        self.win.border()
        self.win.addstr(0, 2, 'Score : ' + str(self.score) + ' ' + str(len(self.snake)))
        self.win.addstr(self.food[0], self.food[1], "*", curses.color_pair(1))
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
        # curses.endwin()
        #print("END")

    def update_state(self):
        self.state = [1, 1, 1, 1, 0, 0]
        if (self.snake[0][0] - 1, self.snake[0][1]) in self.snake[1:]:
            self.state[0] = 0
        if (self.snake[0][0] + 1, self.snake[0][1]) in self.snake[1:]:
            self.state[1] = 0
        if (self.snake[0][0], self.snake[0][1] - 1) in self.snake[1:]:
            self.state[2] = 0
        if (self.snake[0][0], self.snake[0][1] + 1) in self.snake[1:]:
            self.state[3] = 0
        if self.snake[0][0] - 1 == 0:
            self.state[0] = 0
        if self.snake[0][0] + 1 == self.n_row + 1:
            self.state[1] = 0
        if self.snake[0][1] - 1 == 0:
            self.state[2] = 0
        if self.snake[0][1] + 1 == self.n_column + 1:
            self.state[3] = 0

        #a, b = self.distance_angle_head_apple()
        a,b = self.distance_v_o()
        self.state[4] = a
        self.state[5] = b



    def distance_v_o(self):
        #dist = math.sqrt((self.snake[0][0] - self.food[0]) ** 2 + (self.snake[0][1] - self.food[1]) ** 2)
        return self.snake[0][0] - self.food[0], self.snake[0][1] - self.food[1]

    def distance_angle_head_apple(self):
        dist = math.sqrt((self.snake[0][0] - self.food[0]) ** 2 + (self.snake[0][1] - self.food[1]) ** 2)
        if (self.snake[0][1] - self.food[1]) == 0:
            angle = 0
        else:
            angle = math.atan((self.snake[0][0] - self.food[0]) / (self.snake[0][1] - self.food[1]))
        return dist, angle

    def tick(self):
        self.generate_new_head()
        eaten = False
        if self.snake[0] != self.food:
            self.snake.pop()
            self.score -= 1
        elif self.snake[0] == self.food:
            eaten = True

        self.update_state()

        if eaten:
            self.food = ()
            self.generate_food()
            self.score += 50

        collision = self.check_collision()
        if collision or self.score < 0:
            self.gameover()

    def simulate_move(self, key):
        backup_state = self.state.copy()
        backup_end = self.end
        backup_snake = self.snake.copy()
        backup_food = self.food
        backup_score = self.score

        backup_key = self.key

        self.key = key
        self.tick()
        new_state = self.state.copy()
        new_end = self.end
        new_snake = self.snake.copy()
        new_food = self.food
        new_score = self.score

        self.state = backup_state
        self.end = backup_end
        self.snake = backup_snake
        self.food = backup_food
        self.score = backup_score

        self.key = backup_key

        return backup_state, new_state, backup_end, new_end, backup_score, new_score

    def simulate_move_(self, real_move, moves_):
        backup_state = self.state.copy()
        backup_end = self.end
        backup_snake = self.snake.copy()
        backup_food = self.food
        backup_score = self.score
        backup_key = self.key

        self.key = real_move
        self.tick()
        new_state = self.state.copy()
        new_end = self.end
        new_snake = self.snake.copy()
        new_food = self.food
        new_score = self.score
        if self.end is True:
            self.state = backup_state
            self.end = backup_end
            self.snake = backup_snake
            self.food = backup_food
            self.score = backup_score
            self.key = backup_key
            return (backup_state, new_state, backup_end, new_end, backup_score, new_score), new_end

        for list_of_moves in moves_:
            if self.end is True:
                break
            for move in list_of_moves:
                self.key = move
                self.false_tick()
                if self.end is True:
                    break

        self.state = backup_state
        self.end = backup_end
        self.snake = backup_snake
        self.food = backup_food
        self.score = backup_score
        self.key = backup_key

        return (backup_state, new_state, backup_end, new_end, backup_score, new_score), new_end

    def false_tick(self):
        self.generate_new_head()
        self.snake.pop()
        self.score -= 1
        collision = self.check_collision()
        if collision or self.score < 0:
            self.gameover()


    def start(self):
        self.clear()
        while self.end is False:
            self.render()
            self.key = self.win.getch()
            self.tick()
