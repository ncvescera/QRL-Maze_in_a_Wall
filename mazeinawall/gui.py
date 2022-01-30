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

    def __init__(self, matrix: np.ndarray, cell_size=65):
        self.matrix = matrix
        self.x, self.y = self.matrix.shape

        # definizione della posizione start e goal per mostrarle a schermo
        self.start = (0, 0)
        self.goal = (self.x - 1, self.y - 1)

        self.cell_size = cell_size
        self.surface = None

        # inizializza la finestra di pygame
        self.__init_pygame()

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

        agent_x, agent_y = agent_pos

        for i in range(self.x):
            for j in range(self.y):
                if self.matrix[i][j] == 1:
                    col = self.wall_color

                else:
                    col = self.col_background

                if i == agent_x and j == agent_y:
                    col = self.agent_color

                elif i == self.start[0] and j == self.start[1]:
                    col = self.start_color

                elif i == self.goal[0] and j == self.goal[1]:
                    col = self.goal_color

                # stampa la cella corrente
                pygame.draw.rect(self.surface, col, (j * self.cell_size, i * self.cell_size, self.cell_size - 1, self.cell_size - 1))

        pygame.display.update()

        # controlla se l'utente chiude la finestra
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

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
