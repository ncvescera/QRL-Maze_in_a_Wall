from GridWorld import GridWorld
from QLearning import QLearning
from os import system
from maze_utils import is_solvable, grid_from_file


def main():
    # prova a caricare la matrice da file
    grid = grid_from_file("matrix")

    # crea l'ambiente
    if grid is None:
        print(f"Generazione matrice random")
        env = GridWorld(5, 6)
    else:
        print(f"Caricata matrice {grid.shape}")

        # controlla che il labirinto sia esplorabile
        if not is_solvable(grid):
            print("Il labirinto non e' esplorabile !!")
            return

        env = GridWorld(grid=grid)

    # inizializza l'algoritmo di QLearning
    QL = QLearning(env)

    menu()                  # stampa il menu
    command = input(": ")   # attende la scelta dell'utente
    system("clear")

    if command == '1':
        print("Training\n")
        print(f"Maze: {env.grid.shape}")

        # QL.training(epochs=50000, steps=1000, ALPHA=0.01, GAMMA=0.5, EPS=0.9, plot=True)
        QL.training(epochs=6000, steps=200, ALPHA=0.1, GAMMA=1.0, EPS=0.9, plot=True)

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

    print(" Maze in a Wall - QLearning")
    print("-+" * 20)
    print("")
    print("\tTraining (1)")
    print("\tExecute step-by step (2)")
    print("\tExit (0)")


if __name__ == '__main__':
    main()
