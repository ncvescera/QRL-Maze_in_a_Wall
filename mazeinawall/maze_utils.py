import numpy as np
from random import randint

maze_filename = "maze.txt"


def is_solvable(maze, start: tuple[int, int] = None, goal: tuple[int, int] = None) -> bool:
    """
    Controlla se il labirinto è esplorabile: si può raggiungere il goal.
    Se non vengono forniti i parametri start e goal, se li calcola come segue:
        - start = (0, 0)
        - goal = (righe - 1, colonne - 1) [sarebbe l'ultima cella]

    :param maze: labirinto da controllare
    :param start: punto di partenza
    :param goal: punto di arrivo
    :return: True se il labirinto è esplorabile, False altrimenti
    """
    x, y = maze.shape   # prende le dimensioni della matrice per calcolare il goal

    # controlla se è stato fornito start
    if start is None:
        start_position = (0, 0)
    else:
        start_position = start

    # controlla se è stato fornito goal
    if goal is None:
        end_position = (x-1, y-1)
    else:
        end_position = goal

    seen = {start_position}     # elementi visitati
    queue = [start_position]    # coda di elementi da visitare

    while queue:
        i, j = queue.pop(0)
        seen.add((i, j))

        # controlla tutti i vicini (su, giù, sinistra, destra)
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ni, nj = i+di, j+dj   # nuova posizione del vicino

            if (ni, nj) in seen:    # se è già stato visitato
                continue

            elif ni < 0 or nj < 0 or ni >= len(maze) or nj >= len(maze[0]):     # se è fuori dalla matrice
                continue

            elif ni == end_position[0] and nj == end_position[1]:               # se è arrivato alla fine
                return True

            elif maze[ni][nj] == 1:                                             # se è un muro
                continue

            else:                                                               # se è una casella libera
                seen.add((ni, nj))      # aggiunge alla lista visitati
                queue.append((ni, nj))  # aggiunge alla coda da visitare

    return False


def grid_from_file(filename: str) -> tuple[np.ndarray, str]:
    """
    Carica la matrice da file se esiste, altrimenti restituisce None

    :param filename: nome del file da caricare
    :return: la matrice caricata o None
    """
    grid = None
    message = ""

    # prova a caricare da file
    try:
        grid = np.loadtxt(filename, dtype=int)

    except FileNotFoundError:
        grid = None
        message = "File inesistente !"
        return grid, message

    # il file esiste ma risulta vuoto
    if grid is not None and grid.size == 0:
        grid = None
        message = "Il contenuto del file e' errato !"

    elif not is_solvable(grid):
        grid = None
        message = "Il labirinto non e' risolvibile !"

    return grid, message


def generate_grid(m, n, walls=10) -> np.ndarray:
    """
    Genera una matrice di dimensione m x n con un numero di muri pari a walls.
    Fa attenzione a non posizionare muri nella cella goa le start.
    :param walls: numero di muri da inserire nella matrice  # TODO: rendere una percentuale
    :return: matrice di dimensione m x n con muri
    """

    if walls >= (m * n / 2):
        print("Hai scelto troppi muri, non è possibile generare un labirinto esplorabile !!!")
        return None

    solvable = False
    grid = None
    while not solvable:
        grid = np.zeros((m, n), dtype=int)  # matrice piena di 0

        for _ in range(walls):
            # genera a caso una posizione dove inserire il muro
            x = randint(0, m - 1)
            y = randint(0, n - 1)

            # se la cella scelta è il goal o lo stato iniziale la rigenera
            while (x == 0 and y == 0) or (x == (m - 1) and y == (n - 1)):
                x = randint(0, m - 1)
                y = randint(0, n - 1)

            grid[x][y] = 1  # aggiunge il muro

        solvable = is_solvable(grid)

    return grid


"""
    grid = np.array([[0, 1, 1, 0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [1, 1, 0, 0, 1, 1, 0, 1, 0],
                          [1, 1, 0, 0, 1, 0, 0, 0, 0],
                          [1, 1, 1, 1, 1, 0, 0, 0, 0],
                          [1, 1, 0, 0, 0, 0, 0, 0, 0],
                          [1, 1, 1, 1, 1, 1, 1, 0, 0],
                          [1, 1, 1, 1, 1, 1, 1, 1, 0]])
    env = GridWorld(grid=grid)
"""
