import numpy as np
import gym
from gym import spaces
from Maze import Maze


class MazeEnv(gym.Env):
    # Because of google colab, we cannot implement the GUI ('human' render mode)
    # metadata = {'render.modes': ['console']}
    # Define constants for clearer code

    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3

    AGENT = 1
    WALL = 2
    SPACE = 0

    def __init__(self, n=0, m=0):
        super(MazeEnv, self).__init__()

        self.m = m
        self.n = n
        # Size of the 1D-grid
        self.grid_size = n*m
        # Initialize the agent at the right of the grid
        self.agent_pos = {"x": 0, "y": 0}
        self.goal = {"x": n-1, "y": m-1}

        self.mondo = Maze(n, m)
        self.actions = self.mondo.actions

        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions, we have two: left and right
        # n_actions = 2
        n_actions = len(self.actions.keys())
        self.action_space = spaces.Discrete(n_actions)
        # The observation will be the coordinate of the agent
        # this can be described both by Discrete and Box space
        self.observation_space = spaces.Box(
            # low=(0, 0),
            # high=(n-1, m-1),
            low=0,                  # TODO: ricontrollare meglio, potrebbe essere 2x2
            high=self.grid_size,    # TODO: ricontrollare meglio, potrebbe essere 4x4 (la massima dimensione del vicinato di moore)
            shape=(n, m),   # TODO: ricontrollare, alcuni la omettono
            dtype=np.int32  # TODO: potrebbe essere uint32
        )

    def reset(self):
        """
        Important: the observation must be a numpy array
        :return: (np.array)
        """
        # Initialize the agent at the right of the grid
        self.agent_pos = {"x": 0, "y": 0}

        # here we convert to float32 to make it more general (in case we want to use continuous actions)
        # creo la matrice
        matrix = np.zeros((self.n, self.m))

        # posiziono l'agente
        matrix[self.agent_pos["x"]][self.agent_pos["y"]] = self.AGENT

        self.mondo = matrix.copy()

        # ritorno l'osservazione
        return matrix
        # return np.array([self.agent_pos]).astype(np.float32)

    def step(self, action):
        temp_agent_pos = self.agent_pos.copy()

        if action == self.LEFT:
            temp_agent_pos["y"] -= 1
        elif action == self.RIGHT:
            temp_agent_pos["y"] += 1
        elif action == self.UP:
            temp_agent_pos["x"] -= 1
        elif action == self.DOWN:
            temp_agent_pos["x"] += 1
        else:
            raise ValueError("Received invalid action={} which is not part of the action space".format(action))

        # l'ambiente forse e' cicilico e lo fa ritronare daccapo
        # Account for the boundaries of the grid
        # self.agent_pos = np.clip(self.agent_pos, 0, self.grid_size)
        wall_impact = False
        # Are we at the left of the grid?
        done = bool(temp_agent_pos == self.goal)
        # done = bool(self.agent_pos == 0)

        # Null reward everywhere except when reaching the goal (left of the grid)
        reward = -1
        if self.mondo[temp_agent_pos["x"]][temp_agent_pos["y"]] == self.WALL:
            reward = -5
            wall_impact = True
        elif done:
            reward = 10
        # reward = 1 if self.agent_pos == 0 else 0

        if not wall_impact:
            self.mondo[self.agent_pos["x"]][self.agent_pos["y"]] = self.SPACE   # cancella la vecchia pos dell'agente
            self.agent_pos = temp_agent_pos.copy()                              # aggiorna la posizione dell'agente
            self.mondo[self.agent_pos["x"]][self.agent_pos["y"]] = self.AGENT   # stampa l'agente nella nuova pos

        # Optionally we can pass additional info, we are not using that for now
        info = {}

        return self.mondo, reward, done, info

    def render(self, mode='console'):
        if mode != 'console':
            raise NotImplementedError()

        for i in range(self.n):
            for j in range(self.m):
                if self.mondo[i][j] == self.AGENT:
                    print("x", end="")
                elif i == self.goal["x"] and j == self.goal["y"]:
                    print("o", end="")
                elif self.mondo[i][j] == self.WALL:
                    print("|", end="")
                elif self.mondo[i][j] == self.SPACE:
                    print(".", end="")
                else:
                    raise ValueError("Qualcosa nel mondo non ha funzionato")

            print("")
        # agent is represented as a cross, rest as a dot
        # print("." * self.agent_pos, end="")
        # print("x", end="")
        # print("." * (self.grid_size - self.agent_pos))

    def close(self):
        pass