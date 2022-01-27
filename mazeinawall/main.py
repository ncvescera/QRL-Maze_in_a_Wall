from GridWorld import GridWorld
from QLearning import QLearning


if __name__ == '__main__':
    env = GridWorld(10, 10)
    QL = QLearning(env)

    '''self.grid = np.array([[0, 1, 1, 0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [1, 1, 0, 0, 1, 1, 0, 1, 0],
                          [1, 1, 0, 0, 1, 0, 0, 0, 0],
                          [1, 1, 1, 1, 1, 0, 0, 0, 0],
                          [1, 1, 0, 0, 0, 0, 0, 0, 0],
                          [1, 1, 1, 1, 1, 1, 1, 0, 0],
                          [1, 1, 1, 1, 1, 1, 1, 1, 0]])
    '''

    # TODO: migliorare output menu
    command = input("***********************\nGridWorld Demo\n***********************\nTraining (1)  \nExecute step-by step (2)\nExit (0)")
    if command == '1':
        print("Training\n")
        QL.training(epochs=50000, steps=200, ALPHA=0.1, GAMMA=1.0, EPS=1.0, plot=True)
    elif command == '2':
        print("Execute\n")
        QL.execute()
    else:
        print('End\n')
