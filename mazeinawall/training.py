from GridWorld import GridWorld
from QLearning import QLearning
from maze_utils import grid_from_file, maze_filename
from os import walk


# dataset path
dataset = "training"

# training values
epochs = 80000
steps = 1500
ALPHA = 0.1
GAMMA = 1.0
EPS = 0.9


def training():
    """
    Avvia la fase di training/apprendimento.

    Permette all'utente di:
     - scegliere se riprendere o meno un allenamento precedente (ricaricare la matrice Q e modificarla)
     - Caricare un labirinto esistente oppure utilizzare le metrici nella cartella "training"

    :return:
    """
    grid = None
    env = None
    QL = None

    print("Training\n")

    # scelta per modifica della matrice Q esistente
    scelta = input("Riprendere allenamento ? (Y/n)").lower()
    resume = True if scelta != 'n' else False

    # scelta per utilizzo di singola matrice o dataset
    scelta = input("Caricare labirinto esistente ? (Y/n)").lower()
    if scelta != 'n':
        print(f"Avvio training sul labirinto esistente")

        grid, message = grid_from_file(maze_filename)

        if grid is None:
            print(message)
            return

        print(f"Caricato labirinto {grid.shape}")

        env = GridWorld(grid=grid)
        QL = QLearning(env)
        QL.training(epochs=epochs, steps=steps, ALPHA=ALPHA, GAMMA=GAMMA, EPS=EPS, plot=True, resume=resume)

    else:
        print(f"Avvio training sul dataset: {dataset}")

        QL = QLearning(None)

        # ottengo tutti i file nella cartella del dataset
        filenames = next(walk(dataset), (None, None, []))[2]
        for file in filenames:
            grid, message = grid_from_file(f"{dataset}/{file}")

            if grid is None:
                print(f"Errore in {file}: {message}")

            print(f"Caricato labirinto {grid.shape}")

            env = GridWorld(grid=grid)
            QL.env = env
            QL.training(epochs=epochs, steps=steps, ALPHA=ALPHA, GAMMA=GAMMA, EPS=EPS, plot=False, resume=resume, plot_name=file)


if __name__ == "__main__":
    training()
