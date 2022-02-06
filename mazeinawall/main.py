from os import system
from testing import testing
from training import training


def main():
    menu()                  # stampa il menu
    command = input(": ")   # attende la scelta dell'utente
    system("clear")

    if command == '1':
        training()

    elif command == '2':
        testing()

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
