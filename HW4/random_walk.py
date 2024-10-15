import numpy as np
import matplotlib.pyplot as plt

seed = 42
np.random.seed(seed)

def randomWalk2D(b, N):
    """
    Compute the 2D random walk with step size b and N steps.
    Return the x and y coordinates, average displacement, and mean square 
    displacement.
    """
    x = np.zeros(N)
    y = np.zeros(N)

    avgDispX = np.zeros(N)
    avgDispY = np.zeros(N)

    MSDX = np.zeros(N)
    MSDY = np.zeros(N)
    
    stepsX = np.where(np.random.rand(N-1) < 0.5, -b, b)
    stepsY = np.where(np.random.rand(N-1) < 0.5, -b, b)

    x[1:] = np.cumsum(stepsX)
    y[1:] = np.cumsum(stepsY)
    
    for i in range(1, N):
        avgDispX[i] = np.mean(x[i:] - x[:-i])
        avgDispY[i] = np.mean(y[i:] - y[:-i])
        MSDX[i] = np.mean((x[i:] - x[:-i])**2)
        MSDY[i] = np.mean((y[i:] - y[:-i])**2)
    
    return x, y, avgDispX, avgDispY, MSDX, MSDY

def analyze_random_walk(randomWalk2D):
    b, N = 1, 1_000
    x, y, avgDispX, avgDispY, MSDX, MSDY = randomWalk2D(b, N)

    # avgDisp = np.sqrt(avgDispX**2 + avgDispY**2)
    MSD = MSDX + MSDY

    fig1, ax1 = plt.subplots()
    ax1.plot(x, y)
    ax1.set_title("2D Random Walk")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.grid(True)
    
    fig2, ax2 = plt.subplots()
    ax2.plot(MSD)
    ax2.plot(np.arange(0, N), 2*np.arange(0, N))
    ax2.set_title("Mean Square Displacement")
    ax2.set_xlabel("Steps")
    ax2.set_ylabel("MSD")
    ax2.grid(True)

    fig3, ax3 = plt.subplots()
    ax3.plot(avgDispX)
    ax3.plot(avgDispY)
    ax3.set_title("Average Displacement")
    ax3.set_xlabel("Steps")
    ax3.set_ylabel("Average Displacement")
    ax3.grid(True)

    plt.show()

    # print("Average Displacement: ", avgDisp[-1])
    # print('Average Displacement at 0th point:', avgDisp[0])
    
    print('Expected Value of MSD at Nth point:', MSD[-1])
    print('2Nb^2:', 2*N*(b**2))

analyze_random_walk(randomWalk2D)