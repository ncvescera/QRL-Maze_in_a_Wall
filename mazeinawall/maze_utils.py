import numpy as np


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


def grid_from_file(filename: str) -> np.ndarray:
    """
    Carica la matrice da file se esiste, altrimenti restituisce None

    :param filename: nome del file da caricare
    :return: la matrice caricata o None
    """

    # prova a caricare da file
    try:
        grid = np.loadtxt(filename, dtype=int)

    except FileNotFoundError:
        grid = None

    # il file esiste ma risulta vuoto
    if grid.size == 0:
        grid = None

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
