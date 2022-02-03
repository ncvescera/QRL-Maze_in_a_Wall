from GridWorld import GridWorld
from random import randint
import numpy as np


tot_elem = 100  # numero di matrici da generare
max_w = 10  # massima altezza
max_h = 10  # massima lunghezza
min_w = 3
min_h = 3

for elem in range(tot_elem):
    file_name = f"matrici/matrice_{elem}"

    w = randint(min_w, max_w)
    h = randint(min_h, max_h)
    walls = randint(1, int(w * h / 2) - 1)

    env = GridWorld(w, h, walls=walls)
    np.savetxt(file_name, env.grid, delimiter=" ",  fmt='%i')