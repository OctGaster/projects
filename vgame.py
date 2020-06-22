import sys
import re
from enum import Enum
import random
import numpy as np


CELL_NOT_FOUND = -1

VECTOR_TEMPLATES = [
    [1,] * 3 + [0,] * 6,
    [0,] * 3 + [1,] * 3 + [0,] * 3,
    [0,] * 6 + [1,] * 3,
    [1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1]
]

def find_closest_template(v_state, target):
    it = 0
    min_dev = 10
    len_state = np.linalg.norm(v_state)
    if len_state == 0:
        return TEMPLATE_NOT_FOUND, 0
    for i, temp in enumerate(VECTOR_TEMPLATES):
        len_temp = np.linalg.norm(temp)
        cosinus = np.dot(v_state, temp) / len_state / len_temp
        dev = abs(cosinus - target)
        if dev < min_dev:
            min_dev = dev
            it = i
    return it, min_dev


class Status(Enum):
    XWins = 'X wins'
    OWins = 'O wins'
    Draw = 'Draw'
    Unfinished = 'Game not finished'


def ai_step(game_state, mach_mark):
    if np.linalg.norm(game_state) == 0:
        game_state[np.random.randint(9)] = mach_mark
        return
    it1, dist1 = find_closest_template(game_state, mach_mark)
    it2, dist2 = find_closest_template(game_state, -mach_mark)
    if dist1 < dist2:
        it = it1
    else:
        it = it2
    cell_number = CELL_NOT_FOUND
    temp = VECTOR_TEMPLATES[it]
    for i, cell in enumerate(temp):
        if cell != 0 and game_state[i] == 0:
            game_state[i] = mach_mark
            cell_number = i
            break
    if cell_number == CELL_NOT_FOUND:
        invert_vector_state = [1 if cell == 0 else 0 for cell in game_state]
        it, _ = find_closest_template(invert_vector_state, 1)
        temp = VECTOR_TEMPLATES[it]
        for i, cell in enumerate(temp):
            if cell != 0 and game_state[i] == 0:
                game_state[i] = mach_mark
                break


class Game:
    def __init__(self, machine_moves_first=False):
        self.mach_mark = 0
        self.user_mark = 0
        if machine_moves_first:
            self.mach_mark = 1
        else:
            self.mach_mark = -1
        self.user_mark = -self.mach_mark
        self.state = np.array([0,] * 9, dtype=float)
        if machine_moves_first:
            self.make_mach_step()

    def status(self):
        dot_products = np.array([
            np.dot(self.state, temp) for temp in VECTOR_TEMPLATES
        ], dtype=float)
        if any(dot_products == 3):
            return Status.XWins
        elif any(dot_products == -3):
            return Status.OWins
        elif any(self.state == 0):
            return Status.Unfinished
        return Status.Draw

    def make_user_step(self, x, y):
        if (not 0 < x < 4) or (not 0 < y < 4):
            raise IndexError('Coordinates should be from 1 to 3!')
        if self.state[3 * (3 - y) + x - 1] != 0:
            raise IndexError('This cell is occupied! Choose another one!')
        self.state[3 * (3 - y) + x - 1] = self.user_mark

    def make_mach_step(self):
        if np.linalg.norm(self.state) == 0:
            self.state[np.random.randint(9)] = self.mach_mark
            return
        it1, dist1 = find_closest_template(self.state, self.mach_mark)
        it2, dist2 = find_closest_template(self.state, self.user_mark)
        if dist1 < dist2:
            it = it1
        else:
            it = it2
        cell_number = CELL_NOT_FOUND
        temp = VECTOR_TEMPLATES[it]
        for i, cell in enumerate(temp):
            if cell != 0 and self.state[i] == 0:
                self.state[i] = self.mach_mark
                cell_number = i
                break
        if cell_number == CELL_NOT_FOUND:
            invert_vector_state = [1 if cell == 0 else 0 for cell in self.state]
            it, _ = find_closest_template(invert_vector_state, 1)
            temp = VECTOR_TEMPLATES[it]
            for i, cell in enumerate(temp):
                if cell != 0 and self.state[i] == 0:
                    self.state[i] = self.mach_mark
                    break

    def print_state(self):
        print('---------')
        for i in range(3):
            sys.stdout.write('| ')
            for j in range(3):
                if self.state[i * 3 + j] == 0:
                    sys.stdout.write(' ')
                elif self.state[i * 3 + j] == 1:
                    sys.stdout.write('X')
                else:
                    sys.stdout.write('O')
                sys.stdout.write(' ')
            sys.stdout.write('|\n')
        print('---------')

    def update(self):
        ai_step(self.state, self.user_mark)
        self.print_state()
        stat = self.status()
        if stat != Status.Unfinished:
            print(stat.value)
            exit(0)
        ai_step(self.state, self.mach_mark)
        self.print_state()
        stat = self.status()
        if stat != Status.Unfinished:
            print(stat.value)
            exit(0)


choice = input('Perform AI match? (y/n)')
if choice == 'y':
    game = Game()
    while 1:
        game.update()
elif choice == 'n':
    move_order = random.choice([0, 1])
    if move_order:
        print('Machine makes first step')
    else:
        print('First step is yours')
    game = Game(machine_moves_first=move_order)
    game.print_state()
    while 1:
        try:
            x, y = input('Enter the coordinates > ').split()
            x = int(x)
            y = int(y)
            game.make_user_step(x, y)
            game.print_state()
        except ValueError:
            print('You should enter numbers!')
            continue
        except IndexError as error:
            print(error)
            continue
        stat = game.status()
        if stat != Status.Unfinished:
            print(stat.value)
            exit(0)
        print('Machine makes move')
        game.make_mach_step()
        game.print_state()
        stat = game.status()
        if stat != Status.Unfinished:
            print(stat.value)
            exit(0)
