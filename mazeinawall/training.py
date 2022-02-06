from GridWorld import GridWorld
from QLearning import QLearning
from maze_utils import grid_from_file, generate_grid
from os import walk


dataset = "training"
existing_matrix = "matrix"

# training values
epochs = 10000
steps = 1500
ALPHA = 1.0
GAMMA = 1.0
EPS = 0.9


def training():
    grid = None
    env = None
    QL = None

    print("Training Script")

    scelta = input("Riprendere allenamento ? (Y/n)")
    resume = True if scelta != 'n' else False

    scelta = input("Caricare matrice gia' esistente ? (Y/n)")
    if scelta != 'n':
        grid, message = grid_from_file(existing_matrix)

        if grid is None:
            print(message)
            return

        env = GridWorld(grid=grid)
        QL = QLearning(env)
        QL.training(epochs=epochs, steps=steps, ALPHA=ALPHA, GAMMA=GAMMA, EPS=EPS, plot=True, resume=resume)

    else:
        filenames = next(walk(dataset), (None, None, []))[2]
        QL = QLearning(None)

        for file in filenames:
            grid, message = grid_from_file(f"{dataset}/{file}")

            if grid is None:
                print(f"Errore in {file}: {message}")

            env = GridWorld(grid=grid)
            QL.env = env
            QL.training(epochs=epochs, steps=steps, ALPHA=ALPHA, GAMMA=GAMMA, EPS=EPS, plot=False, resume=resume, plot_name=file)


if __name__ == "__main__":
    training()
