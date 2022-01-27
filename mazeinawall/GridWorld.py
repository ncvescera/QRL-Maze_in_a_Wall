from os import lseek
import numpy as np
import random
import matplotlib.pyplot as plt


class GridWorld(object):
    def __init__(self, m=9, n=9, walls=10):
        np.random.seed(22)                 # seed per la generazioni delle mura
        random.seed(22)
        
        self.grid = np.array([[0, 1, 1, 0, 0, 0, 0, 0, 0],
                              [0, 1, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [1, 1, 0, 0, 1, 1, 0, 1, 0],
                              [1, 1, 0, 0, 1, 0, 0, 0, 0],
                              [1, 1, 1, 1, 1, 0, 0, 0, 0],
                              [1, 1, 0, 0, 0, 0, 0, 0, 0],
                              [1, 1, 1, 1, 1, 1, 1, 0, 0],
                              [1, 1, 1, 1, 1, 1, 1, 1, 0]])
        
        self.m = m
        self.n = n
        self.goal = (self.m * self.n) - 1
        # self.grid = self.generate_grid(walls)
        self.reward = 0
        # self.stateSpace = [i for i in range(self.m*self.n)]
        self.stateSpace = [i for i in range(16)]
        self.stateGoals = [self.goal]

        self.actionSpace = {'U': -self.m, 'D': self.m, 'L': -1, 'R': 1}
        self.possibleActions = ['U', 'D', 'L', 'R']
        
        self.agentPosition = 0
        self.set_state(self.agentPosition)

    def generate_grid(self, walls=10):
        grid = np.zeros((self.m, self.n))

        for _ in range(walls):
            x = random.randint(0, self.m - 1)
            y = random.randint(0, self.n - 1)

            while x == 0 and y == 0 or x == self.goal and y == self.goal:
                x = random.randint(0, self.m - 1)
                y = random.randint(0, self.n - 1)

            grid[x][y] = 1

        return grid

    def is_terminal_state(self, state):  #  goal state
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
        #x, y = self.get_agent_row_column()
        #self.grid[x][y] = 0
        self.agentPosition = state
        #x, y = self.get_agent_row_column()
        #self.grid[x][y] = 1

    def off_grid_move(self, new_state, old_state):
        # if we move into a row not in the grid
        #if new_state not in self.stateSpace:
        if new_state not in range(self.n*self.m):
            return True
        # if we're trying to wrap around to next row
        elif old_state % self.m == 0 and new_state % self.m == self.m - 1:
            return True
        elif old_state % self.m == self.m - 1 and new_state % self.m == 0:
            return True
        else:
            return False

    def is_wall_colliding(self, new_state):
        x, y = self.get_agent_row_column(new_state)
        if self.grid[x][y] == 1:
            return True
        else:
            return False

    def getState(self,  nextPosition = "default"):

        if nextPosition != "default":
            x, y = self.get_agent_row_column(nextPosition)
            # x = nextPosition // self.m
            # y = nextPosition % self.n
        else:
            x, y = self.get_agent_row_column()

        #print(x,y)

        if x > 0:
            a = self.grid[x-1][y]
        else:
            a = 1

        if y > 0:
            b = self.grid[x][y-1]
        else:
            b = 1

        #c = self.grid[x][y]
        
        if y < self.n - 1:
            d = self.grid[x][y+1]
        else:
            d = 1
        
        if x < self.m - 1:
            e = self.grid[x+1][y]
        else:
            e = 1

        #print("--------------------")
        #print(a)
        #print(b)
        #print(c)
        #print(d)
        #print(e)
        #print("--------------------")
        
        state = np.array([a,b,d,e])
        # print(state)
        #print(state)
        
        return state

    def state_to_int(self, state):
        result = 0
        for i in range(len(state)):
            # mettere anche se uguale a 3
            if state[i] == 1:
                result += 2**(i)
        return result

    def calculate_next_state(self, action, nextPosition):
        state = self.getState()
        #print(nextPosition)
        # state[0] -> U
        # state[1] -> R
        # state[2] -> D
        # state[3] -> L
        # controllo azione eseguita, e in base ad essa ritorno lo stato ottenuto
        if action == 'U':
            if state[0] == 1:
                self.reward = -5
                return self.state_to_int(state)
            else:
                self.agentPosition = nextPosition
                self.reward = 10 if self.is_terminal_state(nextPosition) else -1
                return self.state_to_int(self.getState(nextPosition))
        elif action == 'D':
            if state[3] == 1:
                self.reward = -5
                return self.state_to_int(state)
            else:
                self.agentPosition = nextPosition
                self.reward = 10 if self.is_terminal_state(nextPosition) else -1
                return self.state_to_int(self.getState(nextPosition))
        elif action == 'L':
            if state[1] == 1:
                self.reward = -5
                return self.state_to_int(state)
            else:
                self.agentPosition = nextPosition
                self.reward = 10 if self.is_terminal_state(nextPosition) else -1
                return self.state_to_int(self.getState(nextPosition))
        elif action == 'R':
            if state[2] == 1:
                self.reward = -5
                return self.state_to_int(state)
            else:
                self.agentPosition = nextPosition
                self.reward = 10 if self.is_terminal_state(nextPosition) else -1
                return self.state_to_int(self.getState(nextPosition))

    def step(self, action):
        agentX, agentY = self.get_agent_row_column()
        current_state = self.getState()
        resulting_position = self.agentPosition + self.actionSpace[action]

        
        if not self.off_grid_move(resulting_position, self.agentPosition):
            return self.calculate_next_state(action, resulting_position), self.reward, self.is_terminal_state(resulting_position), None
        else:
            self.reward = -5                                                                                    
            return self.state_to_int(current_state), self.reward, self.is_terminal_state(self.agentPosition), None

    def reset(self):
        self.agentPosition = 0
        #self.grid = np.zeros((self.m, self.n))
        return self.state_to_int(self.getState())

    def render(self):
        print('------------------------------------------')
        x, y = self.get_agent_row_column()
        for row in range(self.m):
            for col in range(self.n):
                if row == x and col == y:                   # disegna agente
                    print('A', end='\t')
                elif row == self.m-1 and col == self.n-1:   # disegna goal
                    print('o', end='\t')
                elif self.grid[row][col] == 1:              # disegna muro
                    print('X', end='\t')
                else:                                       # disegna spazio
                    print('-', end='\t')
            print('\n')
        print('------------------------------------------')

    def actionSpaceSample(self):
        return np.random.choice(self.possibleActions)
#####
