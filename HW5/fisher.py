import numpy as np
import matplotlib.pyplot as plt

def propogation(tot_time, dt, skip, D):
    # Calculate steps and grid
    steps = round(tot_time / dt / skip)
    N = 100
    x, dx = np.linspace(0, 10, N, retstep=True, dtype='float')
   
    # Initialize time, solution array, and initial conditions
    time = np.linspace(0, tot_time, steps)
    u = np.zeros((N, steps))
    u[:, 0] = 0.5 * (1 - np.tanh(x / 0.1))  # Initial condition

    # Initialize tracking for wave speed detection
    Time1, Time2 = 0, 0
    stopwatchtime1, stopwatchtime2 = False, False

    for i in range(1, steps):
        u[:, i] = u[:, i - 1]
        
        # Finite difference method for diffusion and reaction terms
        for _ in range(skip):
            dud2 = np.zeros(N)
            dud2[1:N - 1] = (u[2:N, i] - 2 * u[1:N - 1, i] + u[:N - 2, i]) / dx**2
            dud2[0] = 2 * (u[1, i] - u[0, i]) / dx**2
            dud2[-1] = 2 * (u[-2, i] - u[-1, i]) / dx**2

            k1 = u[:, i - 1] * (1 - u[:, i - 1])
            k2 = (u[:, i - 1] + dt * k1) * (1 - (u[:, i - 1] + dt * k1))
            u[:, i] += (dt / 2) * (k1 + k2) + dt * D * dud2

            # Apply boundary conditions
            u[0, i] = 1
            u[-1, i] = 0

        # Detect wavefront using fixed points
        if not stopwatchtime1 and np.any(u[1, i] >= 0.5):
            Time1 = time[i]
            stopwatchtime1 = True
        if stopwatchtime1 and not stopwatchtime2 and np.any(u[4, i] >= 0.5):
            Time2 = time[i]
            stopwatchtime2 = True
            wavespeed = (x[4] - x[1]) / (Time2 - Time1)
            print(f'Calculated wave speed for D = {D} is {wavespeed:.4f}')

    return wavespeed  

def wavespeedfunction():
    diffusionarray = np.linspace(0.1, 1, 10)
    wavespeedlist = []

    for D in diffusionarray:
        wave_speed = propogation(tot_time=20, dt=0.001, skip=20, D=D)
        wavespeedlist.append(wave_speed)
        
    # Plot wave speed vs. diffusion coefficient
    plt.plot(diffusionarray, wavespeedlist, 'y')
    # plot 2 sqrt(D) for comparison
    plt.plot(diffusionarray, 2 * np.sqrt(diffusionarray), 'r')
    plt.title('Wavespeed vs D')
    plt.xlabel('Diffusion Coefficient (D)')
    plt.ylabel('Wave Speed')
    plt.show()

wavespeedfunction()
