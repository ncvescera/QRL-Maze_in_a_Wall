import numpy as np
import gym
from gym import spaces
from Maze import Maze
from CommonElements import CommonElements
from time import sleep
from os import system


class MazeEnv(gym.Env):
    def __init__(self, n=0, m=0):
        super(MazeEnv, self).__init__()

        self.m = m
        self.n = n
        self.maze_size = (n, m)
        self.maze_size_int = n * m

        # Initialize the agent at the right of the grid
        self.agent_pos = {"x": 0, "y": 0}
        self.goal = {"x": n-1, "y": m-1}

        self.mondo = Maze(n, m)
        self.actions = self.mondo.actions
        self.items = CommonElements.items()

        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions, we have two: left and right
        # n_actions = 2
        n_actions = len(self.actions)
        self.action_space = spaces.Discrete(n_actions)
        # The observation will be the coordinate of the agent
        # this can be described both by Discrete and Box space

        low = np.zeros((3, 3), dtype=np.int32)
        high = np.ones((3, 3), dtype=np.int32)
        high[1][1] = 0
        self.observation_space = spaces.Box(
            low=low,
            high=high,
            dtype=np.int32  # TODO: potrebbe essere uint32
        )
        """
        self.observation_space = spaces.Box(
            low=np.zeros(len(self.maze_size), dtype=np.int32),                  # TODO: ricontrollare meglio, potrebbe essere 2x2
            high=np.array(self.maze_size, dtype=np.int32) - np.ones(len(self.maze_size), dtype=np.int32),    # TODO: ricontrollare meglio, potrebbe essere 4x4 (la massima dimensione del vicinato di moore)
            # shape=(n, m),   # TODO: ricontrollare, alcuni la omettono
            dtype=np.int32  # TODO: potrebbe essere uint32
        )
        """

    def reset(self):
        """
        Important: the observation must be a numpy array
        :return: (np.array)
        """
        # Initialize the agent at the right of the grid
        self.agent_pos = {"x": 0, "y": 0}
        obs = self.mondo.moore(tuple(self.agent_pos.values()))
        # print(obs)

        return obs

    def step(self, action):
        """
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
        """
        valid, new_pos = self.mondo.check_move(
            tuple(self.agent_pos.values()),
            action
        )
        self.agent_pos = {'x': new_pos[0], 'y': new_pos[1]}

        done = bool(self.agent_pos == self.goal)

        reward = 0
        if valid:
            reward = -1
        elif done:
            reward = 10
        else:
            reward = -5

        # Optionally we can pass additional info, we are not using that for now
        info = {}

        return self.mondo.moore(tuple(self.agent_pos.values())), reward, done, info

    def render(self, mode='console'):
        if mode != 'console':
            raise NotImplementedError()

        system("clear")

        maze = self.mondo.maze

        for i in range(self.n):
            for j in range(self.m):
                if i == self.agent_pos["x"] and j == self.agent_pos["y"]:    # disegna l'agente
                    print("x", end="")
                elif i == self.goal["x"] and j == self.goal["y"]:
                    print("o", end="")
                elif maze[i][j] == self.items["wall"]:
                    print("|", end="")
                elif maze[i][j] == self.items["space"]:
                    print(".", end="")
                else:
                    raise ValueError("Qualcosa nel mondo non ha funzionato")

            print("")
        print("")
        sleep(0.1)

    def close(self):
        pass
