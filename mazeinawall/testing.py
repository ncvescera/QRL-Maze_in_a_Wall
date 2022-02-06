from GridWorld import GridWorld
from QLearning import QLearning
from maze_utils import grid_from_file, maze_filename


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

    # avvio la fase di esecuzione
    QL.execute(step_by_step=step_by_step, gui=gui)


if __name__ == '__main__':
    testing()
