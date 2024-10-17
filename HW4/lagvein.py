import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

seed = 42
np.random.seed(seed)

def Langvein2D(R, T, delta_t):
    """
    Compute the Langevin 2D random walk with radius R, time T, and time step delta_t.
    Return the time, x and y coordinates, and velocity.
    """

    # Parameters
    m = 4 * np.pi * R**3 / 3       # mass of the particle
    kBT = 4 * 10**(-14)            # thermal energy
    eta = 0.01                     # viscosity of water
    zeta = 6 * np.pi * eta * R     # drag coefficient
    c = zeta * np.sqrt(kBT / m)    # magnitude of stochastic force
    
    Steps = round(T / delta_t)
    
    x1 = np.zeros((2,Steps))
    v1 = np.zeros((2,Steps))

    MSD = np.zeros(Steps)
    
    t = np.arange(0, T, delta_t)
    
    for i in tqdm(range(1, Steps), desc="Simulating Langevin 2D walk"):
        
        x1_i = c * np.random.randn(2)
        v1[:,i] = ((1 - zeta * delta_t/2/m) * v1[:,i-1] + delta_t * x1_i/m) / (1 + zeta * delta_t/2/m)
        
        v1mid = (v1[:,i] + v1[:,i-1]) / 2
        x1[:,i] = x1[:,i-1] + delta_t*v1mid
        
        MSD[i] = np.mean(x1[0, :i]**2 + x1[1, :i]**2)

    return t, x1, v1, MSD


def analyze_langevin_walk():
    R, T, delta_t = 1e-6, 0.001, 1e-9
    t, x1, v1, MSD = Langvein2D(R, T, delta_t)

    fig1, ax1 = plt.subplots()
    ax1.plot(x1[0,:], x1[1,:])
    # ax1.plot(x2[0,:], x2[1,:])
    ax1.set_title("2D Langevin Random Walk")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.grid(True)

    fig2, ax2 = plt.subplots()
    ax2.plot(t, MSD)
    ax2.set_title("Mean Square Displacement")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("MSD")
    ax2.grid(True)

    plt.show()

    print("Mean Square Displacement: ", MSD[-1])


analyze_langevin_walk()