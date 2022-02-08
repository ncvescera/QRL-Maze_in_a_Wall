from GridWorld import GridWorld
from QLearning import QLearning
from maze_utils import grid_from_file, maze_filename
from os import walk


# dataset path
dataset = "training"

# training values
EPOCHS = 80000
STEPS = 1500
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

    # valori training di default
    epochs = EPOCHS
    steps = STEPS
    alpha = ALPHA
    gamma = GAMMA
    eps = EPS

    print("Training\n")

    # scelta dei parametri di training
    scelta = input("Vuoi specificare dei parametri per il training ? (y/N) ").lower()
    if scelta == 'y':
        scelta = input(f"Epochs (default {EPOCHS}): ")
        epochs = int(scelta) if scelta != '' else EPOCHS

        scelta = input(f"Steps (default {STEPS}): ")
        steps = int(scelta) if scelta != '' else STEPS

        scelta = input(f"Alpha (default {ALPHA}): ")
        alpha = float(scelta) if scelta != '' else ALPHA

        scelta = input(f"Gamma (default {GAMMA}): ")
        gamma = float(scelta) if scelta != '' else GAMMA

        scelta = input(f"EPS (default {EPS}): ")
        eps = float(scelta) if scelta != '' else EPS

    # print(epochs, steps, alpha, gamma, eps)

    # scelta per modifica della matrice Q esistente
    scelta = input("Riprendere allenamento ? (Y/n)").lower()
    resume = True if scelta != 'n' else False

    # salva su file i valori scelti per il training
    log_training_values(epochs, steps, alpha, gamma, eps)

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
        QL.training(epochs=epochs, steps=steps, ALPHA=alpha, GAMMA=gamma, EPS=eps, plot=True, resume=resume)

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
            QL.training(epochs=epochs, steps=steps, ALPHA=alpha, GAMMA=gamma, EPS=eps, plot=False, resume=resume, plot_name=file)


def log_training_values(epochs, steps, alpha, gamma, eps):
    with open('.training_values', 'w') as f:
        f.write(f"e: {epochs}\n")
        f.write(f"s: {steps}\n")
        f.write(f"a: {alpha}\n")
        f.write(f"g: {gamma}\n")
        f.write(f"eps: {eps}\n")


if __name__ == "__main__":
    training()
