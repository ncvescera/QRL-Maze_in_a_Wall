import numpy as np
import random


class GridWorld(object):
    def __init__(self, m=9, n=9, walls=10, grid=None):
        # sezione per la generazione dei seed
        np.random.seed(22)
        random.seed(22)

        # dimensione matrice
        self.m = m
        self.n = n

        if grid is not None:
            self.grid = grid
            self.m, self.n = self.grid.shape
        else:
            self.grid = self.generate_grid(walls)

        # definizione cella goal
        self.goal = (self.m * self.n) - 1

        # definizione spazio degli stati e goal
        self.stateSpace = [i for i in range(16)]  # TODO: capire perche 16
        self.stateGoals = [self.goal]

        # definizione delle azioni possibili e spazio delle azioni
        # TODO: commentare meglio
        self.actionSpace = {'U': -self.m, 'D': self.m, 'L': -1, 'R': 1}
        self.possibleActions = ['U', 'D', 'L', 'R']

        # posizione dell'agente e stato iniziale
        self.agentPosition = 0
        self.set_state(self.agentPosition)

        # init del reward, sarà cambiato in seguito
        self.reward = 0

    def generate_grid(self, walls=10) -> np.ndarray:
        """
        Genera una matrice di dimensione m x n con un numero di muri pari a walls.
        Fa attenzione a non posizionare muri nella cella goa le start.
        :param walls: numero di muri da inserire nella matrice  # TODO: rendere una percentuale
        :return: matrice di dimensione m x n con muri
        """
        grid = np.zeros((self.m, self.n))  # matrice piena di 0

        for _ in range(walls):
            # genera a caso una posizione dove inserire il muro
            x = random.randint(0, self.m - 1)
            y = random.randint(0, self.n - 1)

            # se la cella scelta è il goal o lo stato iniziale la rigenera
            # while x == 0 and y == 0 or x == self.goal and y == self.goal:
            while x == 0 and y == 0 or x == (self.m - 1) and y == (self.n - 1):
                x = random.randint(0, self.m - 1)
                y = random.randint(0, self.n - 1)

            grid[x][y] = 1  # aggiunge il muro

        return grid

    def is_terminal_state(self, state) -> bool:
        """
        Controlla se il stato passato è uno stato finale
        :param state: stato da controllare
        :return: True se è uno stato finale, False altrimenti
        """
        return state in self.stateGoals

    def get_agent_row_column(self, new_state=None):
        if new_state is None:
            x = self.agentPosition // self.m
            y = self.agentPosition % self.n

            return x, y
        else:
            x = new_state // self.m
            y = new_state % self.n

            return x, y

    def set_state(self, state):
        self.agentPosition = state

    def off_grid_move(self, new_state, old_state) -> bool:
        """
        Controlla se il nuovo stato è fuori dalla griglia
        :param new_state: nuovo stato da controllare
        :param old_state: stato precedente alla mossa
        :return: True se è fuori dalla griglia, False altrimenti
        """
        # TODO: ricontrollare
        if new_state not in range(self.n * self.m):  # se il nuovo stato non appartiene agli stati
            return True
        elif old_state % self.m == 0 and new_state % self.m == self.m - 1:
            return True
        elif old_state % self.m == self.m - 1 and new_state % self.m == 0:
            return True
        else:
            return False

    def is_wall_colliding(self, cell) -> bool:
        """
        Controlla se sta cercando di andare contro un muro
        :param cell: nuovo stato da controllare
        :return: True se sta cercando di andare contro un muro, False altrimenti
        """
        if cell == 1:
            return True
        else:
            return False

    def get_state(self, next_position: int = "default") -> np.array:    # TODO: potrebbe dare errore il typing
        """
        Ottiene lo stato dell'agente. Se next_position è diverso da "default", ottiene il nuovo stato dell'agente.
        Lo stato/osservazione è un array del tipo [0, 1, 1, 0].
            Dove :
                [0] -> posizione sopra l'agente (UP)
                [1] -> posizione a sinistra l'agente (LEFT)
                [2] -> posizione a destra dell'agente (RIGHT)
                [3] -> posizione sotto all'agente (DOWN)
        In sostanza il vicinato di Von Neumann.
                    0
                1   A   2
                    3

        :param next_position: nuova posizione dell'agente
        :return: stato dell'agente/osservazione
        """
        # TODO: vedere se si puo' cambiare default con None
        if next_position != "default":
            x, y = self.get_agent_row_column(next_position)
        else:
            x, y = self.get_agent_row_column()

        # TODO: comprendere questi calcoli
        if x > 0:
            a = self.grid[x - 1][y]
        else:
            a = 1

        if y > 0:
            b = self.grid[x][y - 1]
        else:
            b = 1

        if y < self.n - 1:
            d = self.grid[x][y + 1]
        else:
            d = 1

        if x < self.m - 1:
            e = self.grid[x + 1][y]
        else:
            e = 1
        ###

        state = np.array([a, b, d, e])  # stato da ritornare

        return state

    def state_to_int(self, state: np.array) -> int:  # TODO: forse può essere STATIC
        """
        Converte lo stato (array) in un intero.
        Sostanzialmente mappa uno stato a un numero.
        :param state: stato da convertire
        :return: intero rappresentante lo stato
        """
        result = 0
        for i in range(len(state)):
            # mettere anche se uguale a 3
            if state[i] == 1:
                result += 2 ** i  # TODO: forse era 2 ** (i + 1)
        return result

    def calculate_next_state(self, action, next_position) -> int:
        # TODO: ricontrollare meglio la faccenda
        """
        Calcola il nuovo stato dell'agente in base all'azione e alla nuova posizione.
        In base all'azione calcola anche il reward.

        Ricordo che state è un array del tipo [0, 1, 1, 0].
            Dove :
                [0] -> posizione sopra l'agente (UP)
                [1] -> posizione a sinistra l'agente (LEFT)
                [2] -> posizione a destra dell'agente (RIGHT)
                [3] -> posizione sotto all'agente (DOWN)

        :param action: azione che ha eseguito l'agente
        :param next_position: nuova posizione dove si troverà l'agente
        :return: intero che rappresenta lo stato
        """

        state = self.get_state()        # ottento lo stato attuale dell'agente

        to_return = None                # valore da ritornare alla fine
        update_agent_position = True    # controllo se aggiornare la posizione dell'agente

        if self.off_grid_move(next_position, self.agentPosition):   # controlla se si è spostato fuori dalla griglia
            update_agent_position = False                           # se no effettua le azioni in else
            self.reward = -5                                        # se si, si considera una collisione col muro
            to_return = self.state_to_int(state)

        else:
            # reward e risultato uguali per tutti se non impatta contro un muro
            self.reward = 10 if self.is_terminal_state(next_position) else -1
            to_return = self.state_to_int(self.get_state(next_position))

            # controllo se impatta contro un muro: se si, ritorno lo stato corrente e reward -5
            # "ritorno lo stato corrente" = l'agente non si muove e ha un reward di -5 (azione male male)
            # TODO: si dovrebbe poter usare is_wall_colliding
            if action == 'U':
                if self.is_wall_colliding(state[0]):
                    update_agent_position = False
                    self.reward = -5
                    to_return = self.state_to_int(state)
            elif action == 'D':
                if self.is_wall_colliding(state[3]):
                    update_agent_position = False
                    self.reward = -5
                    to_return = self.state_to_int(state)
            elif action == 'L':
                if self.is_wall_colliding(state[1]):
                    update_agent_position = False
                    self.reward = -5
                    return self.state_to_int(state)
            elif action == 'R':
                if self.is_wall_colliding(state[2]):
                    update_agent_position = False
                    self.reward = -5
                    return self.state_to_int(state)

            if update_agent_position:
                self.agentPosition = next_position

        return to_return

    def step(self, action: str) -> tuple[int, int, bool, object]:
        """
        Data un azione la esegue.
        :param action: azione da eseguire. Carattere singolo che rappresenta la key di actionSpace
        :return: nuovo stato, reward, done, info
        """
        agentX, agentY = self.get_agent_row_column()    # TODO: sembra una riga di codice inutile

        current_state = self.get_state()                                    # prende lo stato attuale dell'agente
        resulting_position = self.agentPosition + self.actionSpace[action]  # calcola la nuova posizione dell'agente

        return self.calculate_next_state(action, resulting_position), self.reward, self.is_terminal_state(resulting_position), None

    def reset(self) -> int:
        """
        Resetta lo stato dell'ambiente e ritorna lo stato/osservazione iniziale

        :return: stato/osservazione iniziale
        """
        self.agentPosition = 0  # l'agente viene rimesso allo stato iniziale

        return self.state_to_int(self.get_state())

    def render(self):
        # TODO: aggiungere il rendering grafico con pygmaes
        """
        Stampa lo stato dell'ambiente sullo schermo

        :return:
        """
        # TODO: si puo' migliorare la stampa toglieno lo \n finale

        spaces = " " * 5
        print("-" * (self.n + len(spaces) * (self.n - 1)))

        x, y = self.get_agent_row_column()
        for row in range(self.m):
            for col in range(self.n):
                if row == x and col == y:
                    print('A', end=spaces)                      # disegna agente
                elif row == self.m - 1 and col == self.n - 1:
                    print('o', end=spaces)                      # disegna goal
                elif self.grid[row][col] == 1:
                    print('X', end=spaces)                      # disegna muro
                else:
                    print('-', end=spaces)                      # disegna spazio
            print("\n")
        print("-" * (self.n + len(spaces) * (self.n - 1)))

    def actionSpaceSample(self):
        return np.random.choice(self.possibleActions)
