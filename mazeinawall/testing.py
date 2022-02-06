from GridWorld import GridWorld
from QLearning import QLearning
from maze_utils import grid_from_file, maze_filename


def testing():
    print("Execute\n")

    grid, message = grid_from_file(maze_filename)

    if grid is None:
        print(message)
        return

    env = GridWorld(grid=grid)
    QL = QLearning(env)

    # scelta per esecuzione step-by-step
    scelta = input("Esecuzione step-by-step? (y/N): ").lower()
    step_by_step = True if scelta == 'y' else False

    scelta = input("GUI? (Y/n): ").lower()
    gui = False if scelta == 'n' else True

    QL.execute(step_by_step=step_by_step, gui=gui)


if __name__ == '__main__':
    testing()
