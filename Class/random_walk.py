import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt

seed = 42
np.random.seed(seed)

def randomWalk1D(b, N):
    x = np.zeros(N)
    avgDisp = np.zeros(N)
    MSD = np.zeros(N)

    steps = np.where(rand(N-1) < 0.5, -b, b)
    x[1:] = np.cumsum(steps)

    for i in range(1, N):
        avgDisp[i] = np.mean(x[i:] - x[:-i])
        MSD[i] = np.mean((x[i:] - x[:-i])**2)

    
    plt.plot(x)

    fig2, ax2 = plt.subplots()
    ax2.plot(MSD)

    plt.show()

    return x,avgDisp,MSD


b, N = 1, 1_000
x = randomWalk1D(b, N)
        