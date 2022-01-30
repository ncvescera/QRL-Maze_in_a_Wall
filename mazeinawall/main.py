from GridWorld import GridWorld
from QLearning import QLearning
import numpy as np
from os import system


def main():
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

    # prova a caricare la matrice da file
    grid = grid_from_file("matrix")

    # crea l'ambiente
    if grid is None:
        env = GridWorld(5, 6)
    else:
        env = GridWorld(grid=grid)

    # inizializza l'algoritmo di QLearning
    QL = QLearning(env)

    menu()                  # stampa il menu
    command = input(": ")   # attende la scelta dell'utente
    system("clear")

    if command == '1':
        print("Training\n")
        print(f"Maze: {env.grid.shape}")

        QL.training(epochs=50000, steps=200, ALPHA=0.1, GAMMA=1.0, EPS=1.0, plot=True)

    elif command == '2':
        print("Execute\n")

        # scelta per esecuzione step-by-step
        scelta = input("Esecuzione step-by-step? (y/N): ").lower()
        if scelta == 'y':
            step_by_step = True
        else:
            step_by_step = False

        scelta = input("GUI? (Y/n): ").lower()
        if scelta == 'n':
            gui = False
        else:
            gui = True

        QL.execute(step_by_step=step_by_step, gui=gui)

    else:
        print('End\n')


def menu():
    """
    Stampa il menu iniziale

    """

    system("clear")

    # print("***********************")
    print(" Maze in a Wall - QLearning")
    print("-+" * 20)
    print("")
    print("\tTraining (1)")
    print("\tExecute step-by step (2)")
    print("\tExit (0)")


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

    return grid


"""
# a_star search
def a_star(graph, start, goal):
    visited, queue = set(), [(start, 0)]
    while queue:
        vertex, dist = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(((vertex, dist + 1), graph[vertex] - visited))
            if vertex == goal:
                return dist
    return None
"""


if __name__ == '__main__':
    main()
