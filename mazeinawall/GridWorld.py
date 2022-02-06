import numpy as np
import random
from GUI import GUI
from maze_utils import is_solvable


class GridWorld(object):

    # TODO: fare in modo di creare matrici random senza seed
    def __init__(self, grid, seeded=False):
        # sezione per la generazione dei seed
        if seeded:
            np.random.seed(22)
            random.seed(22)

        self.grid = grid
        self.m, self.n = self.grid.shape    # dimensione matrice

        # definizione cella goal
        self.goal = (self.m * self.n) - 1

        # definizione spazio degli stati e goal
        """
        viene da 2^4 = 16, dove
            2: il numero di elementi possibili in una cella dell'osservazione (0 o 1)
            4: il numero delle celle dell'osservazione (e.g. [0, 1, 1, 0])
        """
        self.stateSpace = [i for i in range(2**8)]
        self.stateGoals = [self.goal]

        # definizione delle azioni possibili e spazio delle azioni
        # la griglia viene vista come un array 1D (piatto). Muoversi in su di 1 cella nella matrice
        # vuol dire spostarsi di -n caselle nell'array.
        self.actionSpace = {'U': -self.n, 'D': self.n, 'L': -1, 'R': 1}
        self.possibleActions = ['U', 'D', 'L', 'R']

        # posizione dell'agente e stato iniziale
        self.agentPosition = 0
        self.set_state(self.agentPosition)

        # init del reward, sarà cambiato in seguito
        self.reward = 0

        # inizializzo l'oggetto responsabile della GUI
        self.gui = None

    def is_terminal_state(self, state: int) -> bool:
        """
        Controlla se il stato passato è uno stato finale

        :param state: stato da controllare
        :return: True se è uno stato finale, False altrimenti
        """

        return state in self.stateGoals

    def get_agent_row_column(self, new_state: int = None):
        """
        Ritorna le coordinate x, y della posizione dell'agente se new_state è None,
        altrimenti ritorna le coordinate x, y della posizione nuova dell'agente in new_state

        :param new_state: nuovo stato dell'agente
        :return: coordinate x, y della posizione dell'agente
        """

        # per prendere la x si effettua la divisione e si prende solo la parte intera
        # così questo calcolo funziona per tutte le matrici.
        if new_state is None:
            x = int(self.agentPosition / self.n)
            y = self.agentPosition % self.n

            return x, y
        else:
            x = int(new_state / self.n)
            y = new_state % self.n

            return x, y

    def set_state(self, state: int):
        """
        Imposta lo stato dell'agente.
        :param state: nuovo stato da impostare
        """

        self.agentPosition = state

    def off_grid_move(self, new_state, old_state) -> bool:
        """
        Controlla se il nuovo stato è fuori dalla griglia

        :param new_state: nuovo stato da controllare
        :param old_state: stato precedente alla mossa
        :return: True se è fuori dalla griglia, False altrimenti
        """

        if new_state not in range(self.n * self.m):  # se il nuovo stato non appartiene agli stati
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

    def get_state(self, next_position: int = None) -> np.array:
        if next_position is not None:
            x, y = self.get_agent_row_column(next_position)
        else:
            x, y = self.get_agent_row_column()

        vicini = []
                    #  UL         U         UR       L      R       DL       D      DR
        for move in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_x, new_y = x + move[0], y + move[1]     # nuova posizione da osservare
            to_add = 0

            if new_x < 0:
                to_add = 1
            elif new_y < 0:
                to_add = 1
            elif new_x > self.m - 1:
                to_add = 1
            elif new_y > self.n - 1:
                to_add = 1
            else:
                to_add = self.grid[new_x][new_y]

            vicini.append(to_add)

        return np.array(vicini)

    def get_state_old(self, next_position: int = None) -> np.array:
        """
        Ottiene lo stato dell'agente. Se next_position è diverso da "default", ottiene il nuovo stato dell'agente.
        Lo stato/osservazione è un array del tipo [0, 1, 1, 0].
            Dove :
                [0] -> posizione sopra l'agente (UP)
                [1] -> posizione a destra l'agente (RIGHT)
                [2] -> posizione sotto all'agente (DOWN)
                [3] -> posizione a sinistra dell'agente (LEFT)
        In sostanza il vicinato di Von Neumann.
                    0
                3   A   1
                    2

        :param next_position: nuova posizione dell'agente
        :return: stato dell'agente/osservazione
        """

        # prende le coordinate dell'agente
        if next_position is not None:
            x, y = self.get_agent_row_column(next_position)
        else:
            x, y = self.get_agent_row_column()

        # calcola il vicinato di Von Neumann e lo restituisce come array (spiattellato)
        # e.g.: [0, 1, 1, 0]
        #        U  R  D  L
        #
        # ogni if controlla se la relativa posizione controllate è fuori dalla matrice
        # se lo è viene considerata come un muro
        if x > 0:
            up = self.grid[x - 1][y]
        else:
            up = 1

        if y > 0:
            left = self.grid[x][y - 1]
        else:
            left = 1

        if y < self.n - 1:
            right = self.grid[x][y + 1]
        else:
            right = 1

        if x < self.m - 1:
            down = self.grid[x + 1][y]
        else:
            down = 1

        state = np.array([up, right, down, left])  # stato da ritornare

        return state

    def state_to_int(self, state: np.array) -> int:
        """
        Converte lo stato (array) in un intero.
        Sostanzialmente mappa uno stato a un numero.

        :param state: stato da convertire
        :return: intero rappresentante lo stato
        """

        return int("".join([str(x) for x in state]), 2)
        # return int("".join(map(str, state)), 2)

    def calculate_next_state(self, action, next_position) -> int:
        """
        Calcola il nuovo stato dell'agente in base all'azione e alla nuova posizione.
        In base all'azione calcola anche il reward.

        Ricordo che state è un array del tipo [0, 1, 1, 0].
            Dove :
                [0] -> posizione sopra l'agente (UP)
                [1] -> posizione a destra l'agente (RIGHT)
                [2] -> posizione sotto all'agente (DOWN)
                [3] -> posizione a sinistra dell'agente (LEFT)

        :param action: azione che ha eseguito l'agente
        :param next_position: nuova posizione dove si troverà l'agente
        :return: intero che rappresenta lo stato
        """

        state = self.get_state()        # ottengo lo stato attuale dell'agente

        to_return = None                # valore da ritornare alla fine
        update_agent_position = True    # controllo se aggiornare la posizione dell'agente

        # controlla se si è spostato fuori dalla griglia, in caso si considera una collisione col muro
        # se no effettua le azioni in else
        if self.off_grid_move(next_position, self.agentPosition):
            update_agent_position = False
            self.reward = -5
            to_return = self.state_to_int(state)

        else:
            # reward e risultato uguali per tutti se non impatta contro un muro
            self.reward = 10 if self.is_terminal_state(next_position) else -1
            to_return = self.state_to_int(self.get_state(next_position))

            # controllo se impatta contro un muro: se si, ritorno lo stato corrente e reward -5
            # "ritorno lo stato corrente" = l'agente non si muove e ha un reward di -5 (azione male male)
            if action == 'U':
                if self.is_wall_colliding(state[1]):
                    update_agent_position = False
                    self.reward = -5
                    to_return = self.state_to_int(state)
            elif action == 'D':
                if self.is_wall_colliding(state[6]):
                    update_agent_position = False
                    self.reward = -5
                    to_return = self.state_to_int(state)
            elif action == 'L':
                if self.is_wall_colliding(state[3]):
                    update_agent_position = False
                    self.reward = -5
                    to_return = self.state_to_int(state)
            elif action == 'R':
                if self.is_wall_colliding(state[4]):
                    update_agent_position = False
                    self.reward = -5
                    to_return = self.state_to_int(state)

            # se True, vuol dire che l'agente non è andato contro un muro e quindi si può spostare
            if update_agent_position:
                self.agentPosition = next_position

        return to_return

    def step(self, action: str) -> tuple[int, int, bool, object]:
        """
        Data un azione la esegue.
        :param action: azione da eseguire. Carattere singolo che rappresenta la key di actionSpace
        :return: nuovo stato, reward, done, info
        """

        # calcola la nuova posizione dell'agente
        resulting_position = self.agentPosition + self.actionSpace[action]
        next_state = self.calculate_next_state(action, resulting_position)

        actual_state = self.get_state()
        info = {str(actual_state), str(self.state_to_int(actual_state))}

        # effettua la mossa
        return next_state, self.reward, self.is_terminal_state(resulting_position), info

    def reset(self) -> int:
        """
        Resetta lo stato dell'ambiente e ritorna lo stato/osservazione iniziale

        :return: stato/osservazione iniziale
        """

        self.agentPosition = 0  # l'agente viene rimesso allo stato iniziale

        return self.state_to_int(self.get_state())

    def render(self, gui=True) -> bool:
        """
        Stampa lo stato dell'ambiente sullo schermo

        :return: True se il rendering è andato a buon fine, False se l'utente ha chiuso la finestra
        """

        def cli_render():
            """
            Stampa la matrice su terminale

            :return: True sempre dato che non c'e' una finestra di pygame da chiudere
            """

            # Inizializza l'oggetto GUI solo quando serve per evitare spreco di risorse
            if self.gui is None:
                self.gui = GUI(self.grid)

            return self.gui.cli(self.get_agent_row_column())

        def gui_render() -> bool:
            """
            Stampa la matrice sullo schermo con pygame

            :return: False se l'utente ha chiuso la finestra, True altrimenti
            """

            # Inizializza l'oggetto GUI solo quando serve per evitare spreco di risorse
            # Evita di generare una finestra di pygame quando non richiesto
            if self.gui is None:
                self.gui = GUI(self.grid)

            return self.gui.draw(self.get_agent_row_column())

        if gui:
            is_alive = gui_render()

        else:
            is_alive = cli_render()  # ritorna sempre True dato che non c'è una finestra di pygame

        return is_alive

    def actionSpaceSample(self):    # TODO: dargli un senso
        return np.random.choice(self.possibleActions)
