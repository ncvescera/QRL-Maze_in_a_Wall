from GridWorld import GridWorld
from QLearning import QLearning
import numpy as np
from os import system

def main():
    menu()

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

    env = GridWorld(10, 10)
    QL = QLearning(env)

    command = input(": ")
    system("clear")

    if command == '1':
        print("Training\n")
        QL.training(epochs=50000, steps=200, ALPHA=0.1, GAMMA=1.0, EPS=1.0, plot=True)
    elif command == '2':
        print("Execute\n")
        QL.execute()

    else:
        print('End\n')


def menu():
    system("clear")

    print("***********************")
    print("GridWorld Demo")
    print("***********************")
    print("")
    print("\tTraining (1)")
    print("\tExecute step-by step (2)")
    print("\tExit (0)")


if __name__ == '__main__':
    main()
