import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

import multiprocessing
from multiprocessing.dummy import Pool

pool = Pool(4)

current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, '..', 'data', 'train.csv')

df = pd.read_csv(csv_path)

#convert to numpy
data = df.values.astype(np.float32)

#randomize and split the data
np.random.shuffle(data)

X = data[:, 1:] / 255.
Y = data[:, 0].astype(np.int32)

Xtrain = X[:-1000]
Ytrain = Y[:-1000]
Xtest =  X[-1000:]
Ytest =  Y[-1000:]


print("Finished loading in and splitting data")

#layer sizes
D = Xtrain.shape[1]
M = 100
K = len(set(Y))

def softmax(a):
    c = np.max(a, axis=1, keepdims=True)

    #Start by subtracting the max from each column, since we don't like exponeitating large numbers
    e = np.exp(a-c)
    return e / e.sum(axis=-1, keepdims=True)

def relu(x):
    return x * (x>0)

#Yields worst results than log accuarcy
def log_likelihood(Y,P):
    # assume Y is not one-hot encoded
    N = len(Y)
    return np.log(P[np.arange(N), Y]).mean()

class ANN:
    #Constructor
    def __init__(self, D, M, K):
        self.D = D
        self.M = M
        self.K = K
    
    def init(self):
        #Randomly intializes neural network weights
        #Seperate from constructor for situations when we want specific weights
        D, M, K = self.D, self.M, self.K
        self.W1 = np.random.randn(D, M) / np.sqrt(D)
        self.b1 = np.zeros(M)
        self.W2 = np.random.randn(M,K) / np.sqrt(M)
        self.b2 = np.zeros(K)
    
    #Neural Network Feed Forward operation
    def forward(self, X):
        Z = np.tanh(X.dot(self.W1) + self.b1)
        return softmax(Z.dot(self.W2) + self.b2)
    
    #Returns accuarcy given a set of data
    def score(self, X, Y):
        P = np.argmax(self.forward(X), axis=1)
        return np.mean(Y==P)
    
    #Returns all params of the neural network
    def get_params(self):
        # return a 1D flat array of parameters
        return np.concatenate([self.W1.flatten(), self.b1, self.W2.flatten(), self.b2])
    
    #Takes in parameters and shifts them back to neural network weights and assigns them to the neural network
    def set_params(self, params):
        # params is a flat list
        # unflatten into individual weights
        D,M,K = self.D, self.M, self.K
        self.W1 = params[:D * M].reshape(D,M)
        self.b1 = params[D * M:D * M + M]
        self.W2 = params[D * M + M:D * M + M + M * K].reshape(M,K)
        self.b2 = params[-K:]

def evolution_strategy(
        f, # Callable function that returns a reward
        population_size, # How much offspring to create in each generation
        sigma, # Standard deviation for the noise that gets added to the parameter for each offspring
        lr, # Learning rate
        initial_params, # 1D Vector of parameters in starting point for optimization
        num_iters # How many generations of offspring to create until return
        ):

    # assume initial params is a 1-D array
    num_params = len(initial_params)
    reward_per_iteration = np.zeros(num_iters)

    params = initial_params
    for t in range(num_iters):
        t0 = datetime.now()
        N = np.random.randn(population_size, num_params) # population_size x num_params 2D Array under Gaussian distribution

        ### slow way
        #R = np.zeros(population_size) # stores the reward
        #loop through each "offspring"
        #for j in range(population_size):
        #    params_try= params + sigma * N[j]
        #    R[j] = f(params_try)

        # fast way with pool
        R = pool.map(f, [params + sigma * N[j] for j in range(population_size)])
        R = np.array(R)
        
        m = R.mean()
        A = (R - m) / R.std() # Normalize rewards: zero mean and unit variance
        reward_per_iteration[t] = m
        params = params + lr/(population_size * sigma) * np.dot(N.T, A)
        print("Iter:", t, "Avg Reward:", m, "Duration:", (datetime.now() - t0))

    return params, reward_per_iteration

def reward_function(params):
    model = ANN(D,M,K)
    model.set_params(params)
    #Ptrain = model.forward(Xtrain)
    #return log_likelihood(Ytrain,Ptrain)
    return model.score(Xtrain, Ytrain)



if __name__ == '__main__':
    model = ANN(D,M,K)
    model.init()
    params = model.get_params()
    best_params, rewards = evolution_strategy(
        f = reward_function,
        population_size=50,
        sigma=0.1,
        lr=0.2,
        initial_params=params,
        num_iters=600,
    )

    # plot the rewards per iteration
    plt.plot(rewards)
    plt.show()

    # final train and test accuracy
    model.set_params(best_params)
    print("Train score:", model.score(Xtrain, Ytrain))
    print("Test score:", model.score(Xtest, Ytest))
