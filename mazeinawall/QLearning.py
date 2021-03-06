import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from os import system
from datetime import datetime


class QLearning(object):
    def __init__(self, env):
        self.env = env
        self.first_training = True

    def maxAction(self, Q, state, actions: list[str], in_execution=False) -> str:
        """
        Trova l'azione che ha valore massimo per uno stato.

        :param Q: matrice Q
        :param state: stato
        :param actions: possibili azioni
        :param in_execution: se True, quando ci sono azioni con gli stessi valori ne viene scelta una a caso
        :return:
        """

        values = np.array([Q[state, a] for a in actions])
        action = np.argmax(values)

        # TODO: riscrivere meglio
        # prende a caso un'azione se ce ne sono due o piu' uguali
        # solo nella fase di execution !!!
        if in_execution:
            tmp = [i for i, x in enumerate(values) if x == values[action]]
            if len(tmp) > 1:
                action = np.random.choice(tmp)

        return actions[action]

    def saveQ(self, Q, fileName):
        """
        Salva la matrice Q in un file.

        :param Q: matrice Q da salvare
        :param fileName: nome del file su cui salvare la matrice
        """

        numStates = len(self.env.stateSpace)
        Qmatrix = np.zeros((numStates, 4))

        x = 0
        for state in self.env.stateSpace:
            y = 0
            for action in self.env.possibleActions:
                Qmatrix[x][y] = Q[state, action]
                y += 1
            x += 1

        np.savetxt(fileName, Qmatrix, delimiter=" ")

    def loadQ(self, fileName: str) -> dict[tuple[int, str], float]:  # TODO: capire l'associazione tuple - float
        """
        Carica in memoria la matrice Q ottenuta dalla fase di allenamento.

        :param fileName: nome del file che contiene la matrice
        :return:
        """

        # initializing Q(state, action) matrix to zero
        Q = {}
        for state in self.env.stateSpace:
            for action in self.env.possibleActions:
                Q[state, action] = 0
        with open(fileName) as file_name:
            Qmatrix = np.loadtxt(file_name, delimiter=" ")

        x = 0
        for state in self.env.stateSpace:
            y = 0
            for action in self.env.possibleActions:
                Q[state, action] = Qmatrix[x][y]
                y += 1
            x += 1

        return Q

    def execute(self, step_by_step=False, sleep_time=0.5, maxk=30, gui=True):
        """
        Permette l'esecuzione del Q-Learning mostrando a schermo i movimenti dell'agente con il reward ottenuto.
        Permette l'esecuzione step-by-step o automatica.

        :param step_by_step: se True, l'esecuzione viene fatta step-by-step, altrimenti automatica
        :param sleep_time: tempo di attesa tra uno step e l'altro
        :param gui: se True, mostra a schermo il movimento dell'agente con pygame
        """

        # visualizzazione dello stato iniziale
        self.env.reset()
        self.env.render(gui=gui)

        # carico la matrice Q
        Q = self.loadQ("Qmatrix")

        totReward = 0
        if step_by_step:  # esecuzione step-by-step
            command = input("Return: " + str(totReward) + " ExecuteNext?(y/n/uP/dOWN/lEFT/riGTH):")
            while command != 'n':
                if command == 'y':
                    action = self.maxAction(
                        Q,
                        self.env.state_to_int(self.env.moore()),
                        self.env.possibleActions,
                        in_execution=True
                    )
                elif command == 'u':
                    action = 'U'
                elif command == 'd':
                    action = 'D'
                elif command == 'l':
                    action = 'L'
                elif command == 'r':
                    action = 'R'

                observationNext, reward, done, info = self.env.step(action)
                totReward += reward
                print("Action:" + str(action) + " Reward:" + str(reward) + " Actual State: " + str(info) + "\n")

                self.env.render(gui=gui)

                command = input("Return: " + str(totReward) + " ExecuteNext?(y/n/uP/dOWN/lEFT/rIGTH):")

        else:  # esecuzione automatica
            alive = True
            counter = 0
            while alive and counter < maxk:
                action = self.maxAction(
                    Q,
                    self.env.state_to_int(self.env.moore()),
                    self.env.possibleActions,
                    in_execution=True
                )

                observationNext, reward, done, info = self.env.step(action)
                totReward += reward

                print("Action:" + str(action) + " Reward:" + str(reward) + "\n")

                # se l'utente chiude la finestra prima della fine dell'esecuzione il programma termina
                alive = self.env.render(gui=gui)

                counter += 1

                if done:
                    print("Return:" + str(totReward))
                    if gui:
                        self.env.gui.wait()  # aspetta che l'utente chiuda la finestra
                    return True, totReward

                sleep(sleep_time)  # tempo di attesa per visualizzare lo stato successivo
                system("clear")

            return False, totReward

    def training(self, epochs=50000, steps=200, ALPHA=0.1, GAMMA=1.0, EPS=1.0, plot=True, resume=False, plot_name: str = None):
        """
        Funzione che effettua il traning dell'agente con la possibilita' di modificare alcuni parametri.
        Alla fine effettua il salvataggio dela Qmatrix in un file.

        :param epochs: numero di epoche
        :param steps: numero di step per ogni epoca (potrebbe essere il massimo numero di azioni)
        :param ALPHA: learning rate
        :param GAMMA: discount factor
        :param EPS: epsilon-greedy
        :param plot: stampa con matplotlib la learning curve
        :param plot_name: il nome da dare alla foto .png con il grafico del training
        :param resume: se True, invece di inizializzare una nuova matrice Q ricarica quella esistente e la modifica
        """

        # inizializing Q(state, action) matrix to zero
        if resume:
            Q = self.loadQ("Qmatrix")

        elif self.first_training:
            Q = {}
            for state in self.env.stateSpace:
                for action in self.env.possibleActions:
                    Q[state, action] = 0
            self.first_training = False

        else:
            Q = self.loadQ("Qmatrix")

        self.env.reset()
        self.env.render(gui=False)  # nella fase di training la matrice si stampa SOLO sul terminale

        totalRewards = np.zeros(epochs)
        for i in range(epochs):
            if i % int(epochs / 10) == 0:
                print('starting game ', i)

            done = False
            epRewards = 0
            numActions = 0
            observation = self.env.reset()
            while not done and numActions <= steps:
                rand = np.random.random()
                action = self.maxAction(Q, observation, self.env.possibleActions) if rand < (1 - EPS) \
                    else self.env.actionSpaceSample()

                observationNext, reward, done, info = self.env.step(action)
                numActions += 1
                epRewards += reward

                actionNext = self.maxAction(Q, observationNext, self.env.possibleActions)
                Q[observation, action] = Q[observation, action] + ALPHA * (reward +
                                                                           GAMMA * Q[observationNext, actionNext] - Q[
                                                                               observation, action])
                observation = observationNext

                # self.env.render()

            # a ogni epoca fa scendere EPS di un pochino
            # dovrebbe permettere il cambio tra exploration ed exploitation
            if EPS - 2 / epochs > 0:
                EPS -= 2 / epochs
            else:
                EPS = 0

            totalRewards[i] = epRewards
            # self.env.gui.visited_cells.clear()

        plt.plot(totalRewards)

        if plot:
            plt.show()

        if plot_name is not None:
            plt.savefig(f"{plot_name}-{datetime.now().strftime('%H:%M:%S').replace(':', '_')}.png")

        else:
            plt.savefig(f"plt_training_{epochs}_{steps}.png")

        plt.clf()   # ripulisce la figura attuale evitando di stampare piu' grafici uno sopra l'altro

        self.saveQ(Q, "Qmatrix")
