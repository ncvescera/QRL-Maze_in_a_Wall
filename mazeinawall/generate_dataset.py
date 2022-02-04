from GridWorld import GridWorld
from random import randint, seed
import numpy as np
from os import path, mkdir
from maze_utils import generate_grid

seed_number = 69

training_folder = "training"
testing_folder = "testing"

tot_elem_training = 100  # numero di matrici da generare
tot_elem_testing = 10
max_w = 10  # massima altezza
max_h = 10  # massima lunghezza
min_w = 3
min_h = 3


def generate_dataset():
    np.random.seed(seed_number)
    seed(seed_number)

    generate_training(tot_elem_training)
    generate_testing(tot_elem_testing)


def generate_testing(dim: int):
    if not path.exists(testing_folder):
        mkdir(testing_folder)

    for elem in range(dim):
        file_name = f"{testing_folder}/matrice_{elem}"

        w = randint(min_w, max_w)
        h = randint(min_h, max_h)
        walls = randint(1, int(w * h / 2) - 1)

        grid = generate_grid(w, h, walls=walls)
        env = GridWorld(grid=grid)

        np.savetxt(file_name, env.grid, delimiter=" ", fmt='%i')


def generate_training(dim: int):
    if not path.exists(training_folder):
        mkdir(training_folder)

    for elem in range(dim):
        file_name = f"{training_folder}/matrice_{elem}"

        w = randint(min_w, max_w)
        h = randint(min_h, max_h)
        walls = randint(1, int(w * h / 2) - 1)

        grid = generate_grid(w, h, walls=walls)
        env = GridWorld(grid=grid)

        np.savetxt(file_name, env.grid, delimiter=" ", fmt='%i')


if __name__ == "__main__":
    generate_dataset()
