import numpy as np
import random


class Maze:

    ACTIONS_VALUES = ["N", "S", "E", "W"]
    ACTIONS_NAMES = ["up", "down", "right", "left"]
    WALL = 1

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.maze = np.zeros((self.n, self.m), dtype=np.int32)

        self.actions = dict(zip(self.ACTIONS_NAMES, self.ACTIONS_VALUES))

        # TODO: aggiungere parte dove vengono generate le mura
        for _ in range(10):
            x = random.randint(0, n-1)
            y = random.randint(0, m-1)

            self.maze[y][x] = self.WALL

    def moore(self, pos: tuple[int, int]):
        # pos = (x_val, y_val)
        x, y = pos
        vicini = np.zeros((3, 3), dtype=np.int32)

        # TODO: migliorare il calcolo
        vicini[0][0] = self.maze[(x - 1)][(y - 1)] if (x - 1) >= 0 and y - 1 >= 0 else 1
        vicini[0][1] = self.maze[(x - 1)][y] if (x - 1) >= 0 else 1
        vicini[0][2] = self.maze[(x - 1)][(y + 1)] if (x - 1) >= 0 and y + 1 < self.m else 1
        vicini[1][0] = self.maze[x][(y - 1)] if (y - 1) >= 0 else 1
        vicini[1][1] = self.maze[x][y]
        vicini[1][2] = self.maze[x][(y + 1)] if (y + 1) < self.n else 1
        vicini[2][0] = self.maze[(x + 1)][(y - 1)] if (x + 1) < self.n and y - 1 >= 0 else 1
        vicini[2][1] = self.maze[(x + 1)][y] if (x + 1) < self.n else 1
        vicini[2][2] = self.maze[(x + 1)][(y + 1)] if (x + 1) < self.n and y + 1 < self.m else 1

        return vicini

    def check_move(self, pos: tuple[int, int], action: str) -> tuple[bool, tuple[int, int]]:
        to_return = False
        x, y = pos
        new_pos = (x, y)

        if action == self.actions["up"]:
            if (x-1) >= 0 and self.maze[(x-1)][y] != self.WALL:
                to_return = True
                new_pos = ((x - 1), y)
        elif action == self.actions["down"]:
            if (x+1) < self.n and self.maze[(x+1)][y] != self.WALL:
                to_return = True
                new_pos = ((x + 1), y)
        elif action == self.actions["right"]:
            if (y+1) < self.m and self.maze[x][(y+1)] != self.WALL:
                to_return = True
                new_pos = (x, (y + 1))
        elif action == self.actions["left"]:
            if (y-1) >= 0 and self.maze[x][(y-1)] != self.WALL:
                to_return = True
                new_pos = (x, (y - 1))
        else:
            raise ValueError(f"E' stata selezionata un'azione invalida: {action}")

        return to_return, new_pos
