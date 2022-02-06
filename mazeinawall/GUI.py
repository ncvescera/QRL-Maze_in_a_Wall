import pygame
import numpy as np


class GUI:
    """
    Questa classe gestisce la rappresentazione grafica della simulazione.
    """

    wall_color = (0, 0, 0)
    col_grid = (0, 0, 0)
    col_background = (255, 255, 255)
    start_color = (0, 255, 0)
    goal_color = (0, 0, 255)
    agent_color = (255, 0, 0)
    path_color = (192, 192, 192)

    def __init__(self, matrix: np.ndarray, cell_size=65):
        self.matrix = matrix
        self.x, self.y = self.matrix.shape

        # definizione della posizione start e goal per mostrarle a schermo
        self.start = (0, 0)
        self.goal = (self.x - 1, self.y - 1)

        self.cell_size = cell_size

        # inizializza il set di celle visitate (per colorare il path)
        self.visited_cells = set()

        # inizializza la finestra di pygame
        self.surface = None
        # self.__init_pygame()

    def __init_pygame(self):
        """
        Inizializza la finestra di pygame.
        """

        pygame.init()
        self.surface = pygame.display.set_mode((self.y * self.cell_size, self.x * self.cell_size))
        pygame.display.set_caption("QML Learning")

    def draw(self, agent_pos: tuple) -> bool:
        """
        Stampa a schermo la matrice.
        Se l'utente chiude la finestra prima della fine dell'esecuzione:
            e.g.: chiusura della finestra di pygame prima della fine dell'esecuzione automatica
        questo metodo suggerisce al chiamante d'interrompere l'esecuzione del programma.

        :param agent_pos: posizione dell'agente
        :return: False se l'utente ha chiuso la finestra prima della fine, True altrimenti
        """

        if self.surface is None:
            self.__init_pygame()

        agent_x, agent_y = agent_pos

        for i in range(self.x):
            for j in range(self.y):
                if self.matrix[i][j] == 1:
                    col = self.wall_color

                else:
                    col = self.col_background

                if i == agent_x and j == agent_y:
                    self.visited_cells.add((i, j))
                    col = self.agent_color

                elif i == self.start[0] and j == self.start[1]:
                    col = self.start_color

                elif i == self.goal[0] and j == self.goal[1]:
                    col = self.goal_color
                elif (i, j) in self.visited_cells:
                    col = self.path_color

                # stampa la cella corrente
                pygame.draw.rect(self.surface, col, (j * self.cell_size, i * self.cell_size, self.cell_size - 1, self.cell_size - 1))

        pygame.display.update()

        # controlla se l'utente chiude la finestra
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        return True

    def cli(self, agent_pos: tuple) -> bool:
        """
        Stampa la matrice nel terminale
        """

        # variabili per stampare la matrice
        to_print = ""  # stringa da stampare alla fine

        spaces = " " * 5  # spazi tra le celle
        line_between_spaces = ("| " + " " * (self.y + len(spaces) * (self.y - 1))) + " |\n"  # linea vuota tra le celle
        horizontal_line = "  " + "-" * (self.y + len(spaces) * (self.y - 1)) + "\n"  # bordo della matrice
        x, y = agent_pos    # posizione dell'agente

        # stampa la matrice
        to_print += horizontal_line  # stampa il bordo superiore
        for row in range(self.x):
            to_print += "| "
            for col in range(self.y):
                if row == x and col == y:
                    to_print += f"A{spaces}"  # disegna agente
                elif row == self.x - 1 and col == self.y - 1:
                    to_print += f"o{spaces}"  # disegna goal
                elif self.matrix[row][col] == 1:
                    to_print += f"X{spaces}"  # disegna muro
                else:
                    to_print += f"-{spaces}"  # disegna spazio vuoto

            to_print = to_print[:-len(spaces)]  # toglie l'ultimo spazio
            to_print += " |\n"
            to_print += line_between_spaces

        to_print = to_print[:-len(line_between_spaces)]  # toglie l'ultima riga
        to_print += "  " + "-" * (self.y + len(spaces) * (self.y - 1)) + "\n"  # stampa il bordo inferiore

        print(to_print)

        return True

    def wait(self):
        """
        Attende che l'utente chiuda la finestra.
        Questo permette di non chiudere immediatamente la finestra quando l'esecuzione automatica è terminata.
        """

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
