import numpy as np
import random
from gui import GUI


class GridWorld(object):
    def __init__(self, m=9, n=9, walls=10, grid=None):  # TODO: fare in modo di creare matrici random senza seed
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
        self.actionSpace = {'U': -self.n, 'D': self.n, 'L': -1, 'R': 1}
        self.possibleActions = ['U', 'D', 'L', 'R']

        # posizione dell'agente e stato iniziale
        self.agentPosition = 0
        self.set_state(self.agentPosition)

        # init del reward, sarà cambiato in seguito
        self.reward = 0

        # inizializzo l'oggetto responsabile della GUI
        self.gui = None

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

        # TODO: andrebbe commentato e capito che calcolo viene effettuato
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

        # prende le coordinate dell'agente
        if next_position is not None:
            x, y = self.get_agent_row_column(next_position)
        else:
            x, y = self.get_agent_row_column()

        # calcola il vicinato di Von Neumann e lo restituisce come array (spiattellato)
        # e.g.: [0, 1, 1, 0]
        #        U  L  R  D
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

        state = np.array([up, left, right, down])  # stato da ritornare

        return state

    def state_to_int(self, state: np.array) -> int:
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
        info = {str(self.get_state())}

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
            Stampa la matrice nel terminale
            """

            # variabili per stampare la matrice
            to_print = ""   # stringa da stampare alla fine

            spaces = " " * 5    # spazi tra le celle
            line_between_spaces = ("| " + " " * (self.n + len(spaces) * (self.n - 1))) + " |\n"  # linea vuota tra le celle
            horizontal_line = "  " + "-" * (self.n + len(spaces) * (self.n - 1)) + "\n"          # bordo della matrice
            x, y = self.get_agent_row_column()  # posizione dell'agente

            # stampa la matrice
            to_print += horizontal_line         # stampa il bordo superiore
            for row in range(self.m):
                to_print += "| "
                for col in range(self.n):
                    if row == x and col == y:
                        to_print += f"A{spaces}"                      # disegna agente
                    elif row == self.m - 1 and col == self.n - 1:
                        to_print += f"o{spaces}"                      # disegna goal
                    elif self.grid[row][col] == 1:
                        to_print += f"X{spaces}"                      # disegna muro
                    else:
                        to_print += f"-{spaces}"                      # disegna spazio vuoto

                to_print = to_print[:-len(spaces)]  # toglie l'ultimo spazio
                to_print += " |\n"
                to_print += line_between_spaces

            to_print = to_print[:-len(line_between_spaces)]                         # toglie l'ultima riga
            to_print += "  " + "-" * (self.n + len(spaces) * (self.n - 1)) + "\n"   # stampa il bordo inferiore

            print(to_print)

        def gui_render() -> bool:
            """
            Stampa la matrice sullo schermo con pygame

            :return: False se l'utente ha chiuso la finestra, True altrimenti
            """

            # La prima volta che viene chiamato il metodo render inizializza pygame.
            # Evita di generare una finestra di pygame quando non richiesto
            if self.gui is None:
                self.gui = GUI(self.grid)

            return self.gui.draw(self.get_agent_row_column())

        if gui:
            is_alive = gui_render()

        else:
            cli_render()
            is_alive = True  # ritorna sempre True dato che non c'è una finestra di pygame

        return is_alive

    def actionSpaceSample(self):    # TODO: dargli un senso
        return np.random.choice(self.possibleActions)
