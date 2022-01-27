from os import lseek
import numpy as np
import matplotlib.pyplot as plt


class QLearning(object):
    def __init__(self, env):
        self.env = env


    def maxAction(self,Q, state, actions):
        values = np.array([Q[state,a] for a in actions])
        action = np.argmax(values)
        action = np.argmax(values)
        return actions[action]

    #print Matrix Q(state, action)
    def printQ(self,Q):
        for i in range(self.env.m):
            for j in range(self.env.n):
                print("(",i,",",j,")")
                for action in self.env.possibleActions:
                    print(Q[i*j,action]," ")
                print(" -")
            print("\n")

    #save Matrix Q(state, action) in fileName
    def saveQ(self,Q,fileName):
        # numStates = self.env.m*self.env.n
        numStates = len(self.env.stateSpace)
        Qmatrix = np.zeros( (numStates, 4))
        x=0
        for state in self.env.stateSpace:
                y=0
                for action in self.env.possibleActions:
                    Qmatrix[x][y]=Q[state, action]
                    y+=1
                x +=1
        np.savetxt(fileName, Qmatrix, delimiter=" ")


    # Loading Q(state, action) matrix
    def loadQ(self,fileName):
        # inizializing Q(state, action) matrix to zero
        Q = {}
        for state in self.env.stateSpace:
            for action in self.env.possibleActions:
                Q[state, action] = 0
        with open(fileName) as file_name:
            Qmatrix = np.loadtxt(file_name, delimiter=" ")
        #print(Qmatrix)
        x=0
        for state in self.env.stateSpace:
                y=0
                for action in self.env.possibleActions:
                        Q[state,action]=Qmatrix[x][y]
                        y+=1
                x+=1
        return Q


    # EXECUTE
    def execute(self):
        self.env.reset()
        self.env.render()
        Q=self.loadQ("Qmatrix")
        totReward=0
        command=input("Return: "+str(totReward)+" ExecuteNext?(y/n/uP/dOWN/lEFT/riGTH):")
        while  command != 'n':
            if command =='y':
                action=self.maxAction(Q, self.env.state_to_int(self.env.get_state()) , self.env.possibleActions)
            elif command == 'u':
                action='U'
            elif command == 'd':
                action='D'
            elif command == 'l':
                action='L'
            elif command == 'r':
                action='R'
            observationNext, reward, done, info = self.env.step(action)
            totReward += reward
            print("Action:"+str(action)+" Reward:"+str(reward)+"\n")
            self.env.render()
            command=input("Return: "+str(totReward)+" ExecuteNext?(y/n/uP/dOWN/lEFT/rIGTH):")

    # TRAINING
    def training(self, epochs=50000, steps=200, ALPHA=0.1, GAMMA=1.0, EPS= 1.0, plot=True):
        '''
        default hyperparameters
        ALPHA = 0.1 is the learning rate of q learning
        GAMMA = 1.0 is the discount factor 
        EPS = 1.0   is the epsilon and is related to the greedy value of the algorithm 
        Epochs = 50000 is the max number of epochs
        Steps = 200 is the max number of actions ( step ) per epoch
    
        '''
    # inizializing Q(state, action) matrix to zero
        Q = {}
        for state in self.env.stateSpace:
            for action in self.env.possibleActions:
                Q[state, action] = 0

        self.env.reset()
        self.env.render()
        totalRewards = np.zeros(epochs)
        for i in range(epochs):
            if i % int(epochs/10) == 0:
                print('starting game ', i)
                #self.env.render()
                #pQ(Q,self.env)
            done = False
            epRewards = 0
            numActions =0 
            observation = self.env.reset()
            while not done and numActions <= steps :
                rand = np.random.random()
                action = self.maxAction(Q,observation, self.env.possibleActions) if rand < (1-EPS) \
                                                        else self.env.actionSpaceSample()
                observationNext, reward, done, info = self.env.step(action)
                numActions+= 1 
                epRewards += reward
                # self.env.render()
                actionNext = self.maxAction(Q, observationNext, self.env.possibleActions)
                Q[observation,action] = Q[observation,action] + ALPHA*(reward + \
                            GAMMA*Q[observationNext,actionNext] - Q[observation,action])
                observation = observationNext
            #self.env.render()
            if EPS - 2 / epochs > 0:
                EPS -= 2 / epochs
            else:
                EPS = 0
            totalRewards[i] = epRewards
            #if epRewards > - 2000:
                #self.env.render()
                #print('Reward:',epRewards)
        if plot:
            plt.plot(totalRewards)
            plt.show()
            #self.printQ(Q)

        self.saveQ(Q,"Qmatrix")
    #   saveQ2(Q,env,"Qmatrix2")
    #   saveQ(Q, "Qmatrix")
