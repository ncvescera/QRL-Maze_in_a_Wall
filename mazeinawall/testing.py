from GridWorld import GridWorld
from QLearning import QLearning
from maze_utils import grid_from_file, maze_filename
from os import walk

dataset = "testing"


def testing():
    """
    Avvia la fase di testing/execution.

    Permette di:
     - scegliere all'utente se la fase di esecuzione deve essere fatta step-by-step oppure automatica
     - se l'output verra' stampato su terminale o su una finestra apposita (GUI).

    :return:
    """

    print("Execute\n")

    # carica labirinto da file
    grid, message = grid_from_file(maze_filename)

    # controlla se e' stato caricato con successo
    if grid is None:
        print(message)
        return

    # creo l'ambiente e l'algoritmo per il qlearning
    env = GridWorld(grid=grid)
    QL = QLearning(env)

    # scelta per esecuzione step-by-step
    scelta = input("Esecuzione step-by-step? (y/N): ").lower()
    step_by_step = True if scelta == 'y' else False

    # scelta GUI
    scelta = input("GUI? (Y/n): ").lower()
    gui = False if scelta == 'n' else True

    scelta = input("Utilizzare dataset di testing (y/N): ").lower()
    if scelta == 'y':
        # ottengo tutti i file nella cartella del dataset
        filenames = next(walk(dataset), (None, None, []))[2]
        for file in filenames:
            grid, message = grid_from_file(f"{dataset}/{file}")

            if grid is None:
                print(f"Errore in {file}: {message}")

            print(f"Caricato labirinto {grid.shape}")

            env = GridWorld(grid=grid)
            QL.env = env
            QL.execute(step_by_step=step_by_step, gui=gui)

    else:
        # avvio la fase di esecuzione
        QL.execute(step_by_step=step_by_step, gui=gui)


if __name__ == '__main__':
    testing()
