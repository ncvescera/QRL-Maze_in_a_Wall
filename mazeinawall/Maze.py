import numpy as np
import random


class Maze:

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.__maze = np.zeros((self.n, self.m), dtype=np.int32)

        # TODO: aggiungere parte dove vengono generate le mura
        for _ in range(10):
            x = random.randint(0, n-1)
            y = random.randint(0, m-1)

            self.__maze[y][x] = 1

    @property
    def world(self):
        return self.__maze

    def moore(self, pos: tuple[int, int]):
        # pos = {"x": val, "y": val}
        x, y = pos
        vicini = np.zeros((3, 3), dtype=np.int32)

        # TODO: migliorare il calcolo
        vicini[0][0] = self.__maze[(x - 1)][(y - 1)] if (x-1) >= 0 and y-1 >= 0 else 1
        vicini[0][1] = self.__maze[(x - 1)][y] if (x-1) >= 0 else 1
        vicini[0][2] = self.__maze[(x - 1)][(y + 1)] if (x-1) >= 0 and y+1 < self.m else 1
        vicini[1][0] = self.__maze[x][(y - 1)] if (y-1) >= 0 else 1
        vicini[1][1] = self.__maze[x][y]
        vicini[1][2] = self.__maze[x][(y + 1)] if (y+1) < self.n else 1
        vicini[2][0] = self.__maze[(x + 1)][(y - 1)] if (x+1) < self.n and y-1 >= 0 else 1
        vicini[2][1] = self.__maze[(x + 1)][y] if (x+1) < self.n else 1
        vicini[2][2] = self.__maze[(x + 1)][(y + 1)] if (x+1) < self.n and y+1 < self.m else 1

        return vicini
