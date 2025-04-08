import numpy as np
import matplotlib.pyplot as plt

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
        N = np.random.randn(population_size, num_params) # population_size x num_params 2D Array under Gaussian distribution
        R = np.zeros(population_size) # stores the reward

        #loop through each "offspring"
        for j in range(population_size):
            params_try= params + sigma * N[j]
            R[j] = f(params_try)
        
        m = R.mean()
        A = (R - m) / R.std() # Shift reward so average is 0, and standardizes by making values vary by STDs
        reward_per_iteration[t] = m
        params = params + lr/(population_size * sigma) * np.dot(N.T, A)

    return params, reward_per_iteration

def reward_function(params):
    x0 = params[0]
    x1 = params[1]
    x2 = params[2]
    return -(x0**2 + 0.1*(x1 - 1)**2 + 0.5*(x2+2)**2)

if __name__ == '__main__':
    bests_params, rewards = evolution_strategy(
        f = reward_function,
        population_size=50,
        sigma=0.1,
        lr=1e-3,
        initial_params=np.random.randn(3),
        num_iters=500,
    )

    plt.plot(rewards)
    plt.show()

    print("Final params:", bests_params)