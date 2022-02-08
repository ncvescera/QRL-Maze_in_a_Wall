from random import randint, seed
import numpy as np
from os import path, mkdir
from maze_utils import generate_grid

seed_number = 69

training_folder = "training"
testing_folder = "testing"

tot_elem_training = 100  # numero di matrici da generare
tot_elem_testing = 20    # numero di matrici da generare
max_w = 10               # massima altezza
max_h = 10               # massima lunghezza
min_w = 3                # minima altezza
min_h = 3                # minima larghezza


def generate_dataset():
    """
    Genera il dataset di training e testing creando matrici a caso
    di dimensione massima 10x10, minima 3x3 e con un numero minimo di 1 muro

    :return:
    """

    # imposto il seed
    np.random.seed(seed_number)
    seed(seed_number)

    generate_training(tot_elem_training)
    generate_testing(tot_elem_testing)


def generate_testing(dim: int):
    """
    Genera il dataset di testing.
    Se la cartella non esiste la crea e la popola con matrici a caso.

    :param dim: numero di matrici da creare
    :return:
    """
    # se la cartella non esiste la creo
    if not path.exists(testing_folder):
        mkdir(testing_folder)

    for elem in range(dim):
        file_name = f"{testing_folder}/matrice_{elem}"

        # scelta random di w, h e walls
        w = randint(min_w, max_w)
        h = randint(min_h, max_h)
        walls = randint(1, int(w * h / 2) - 1)

        grid = generate_grid(w, h, walls=walls)

        np.savetxt(file_name, grid, delimiter=" ", fmt='%i')


def generate_training(dim: int):
    """
    Genera il dataset di training.
    Se la cartella non esiste la crea e la popola con matrici a caso.

    :param dim: numero di matrici da creare
    :return:
    """

    # se la cartella non esiste la creo
    if not path.exists(training_folder):
        mkdir(training_folder)

    for elem in range(dim):
        file_name = f"{training_folder}/matrice_{elem}"\

        # scelta random di w, h e walls
        w = randint(min_w, max_w)
        h = randint(min_h, max_h)
        walls = randint(1, int(w * h / 2) - 1)

        grid = generate_grid(w, h, walls=walls)

        np.savetxt(file_name, grid, delimiter=" ", fmt='%i')


if __name__ == "__main__":
    generate_dataset()
