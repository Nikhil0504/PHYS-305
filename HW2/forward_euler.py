# Use the forward Euler method to solve 
# dx/dt = x - x^2
# with initial condition, x(0) = 0.1. Investigate how the solution depends on time step, using a 
# range of values between ∆t = 0.01 and 3. Pay special attention to the range of ∆t between 2 
# and 3. Provide graphs to show all the behaviors you find. Try to come up with an explanation 
# for what happens between ∆t = 2 and 3.

import numpy as np
import matplotlib.pyplot as plt

# Define the function for dx/dt = x - x^2
def dx_dt(x):
    return x - x**2

# Forward Euler method for a single step
def forward_euler(x, dt, f):
    return x + dt * f(x)

# Solve using Forward Euler method
def solve_euler(x0, t_end, dt, f):
    time = np.arange(0, t_end, dt)

    N = np.zeros_like(time)
    N[0] = x0

    for i in range(1, len(time)):
        N[i] = forward_euler(N[i-1], dt, f)
    
    return time, N


if __name__ == "__main__":
    # Initial condition and total time
    x0 = 0.1
    t_end = 30

    # Time step values, including range between 2 and 3
    dt_s = np.concatenate([np.linspace(0.01, 2, 6), np.linspace(2, 3, 4)])

    # Plotting results for each time step
    plt.figure(figsize=(10, 6))
    for dt in dt_s:
        time, N = solve_euler(x0, t_end, dt, dx_dt)
        plt.plot(time, N, label=f"dt = {dt:.2f}")

    # Labels and legend
    plt.xlabel("Time")
    plt.ylabel("x")
    plt.legend()
    plt.title("Forward Euler Method Solution with Different Time Steps")
    plt.grid(True)
    plt.savefig("forward_euler.png")
    plt.show()