# dx/dt = a - x + x^2 y
# dy/dx = b - x^2 y

# where a and b are constants.  Write a function that uses a semi-implicit Backward Euler to 
# solve this system of equations and find values for a and b such that x and y oscillate in time. 
# For time-stepping using the semi-implicit method, evaluate the linear term in x at time t + ∆t, 
# but evaluate the term x2y at time t.  Hint for finding the oscillations: The initial concentrations 
# of x and y need to be close to but not equal to the equilibrium concentrations. Determine the 
# equilibrium values and use values that are close to this for the initial conditions. 
import numpy as np
import matplotlib.pyplot as plt
from forward_euler import forward_euler


# Define the system of equations from question
def dx_dt(x, y, a):
    return a - x + x**2 * y

def dy_dt(x, y, b):
    return b - x**2 * y

# Backward Euler method for a single step
def backward_euler(x, dt, f):
    return x / (1 - dt * f(x))

def semi_implicit_backward_euler(x, y, dt, a, b):
    x_new = backward_euler(x, dt, lambda x: a - x + x**2 * y)
    y_new = forward_euler(y, dt, lambda y: b - x_new**2 * y)

    return x_new, y_new

# Solve using semi-implicit backward Euler method
def solve_semi_implicit_euler(x0, y0, t_end, dt, a, b):
    time = np.arange(0, t_end, dt)

    x = np.zeros_like(time)
    y = np.zeros_like(time)

    x[0] = x0
    y[0] = y0

    for i in range(1, len(time)):
        # x[i], y[i] = semi_implicit_backward_euler(x[i-1], y[i-1], dt, a, b)
        x[i] = (x[i-1] + (dt * (a + x[i-1]**2 * y[i-1]))) / (1 + dt)
        y[i] = y[i-1] + dt * (b - x[i-1]**2 * y[i-1])

    return time, x, y


if __name__ == "__main__":
    # Constants a and b
    # As = [3.2, 3.5]  # Try a range of values for a
    # Bs = [3.2, 3.5]  # Try a range of values for b
    Bs = [0.3, 3.5]
    As = [np.cbrt(Bs[0]) - Bs[0], 3.5]

    for a, b in zip(As, Bs):
        # Initial conditions and total time
        x_eq = a + b
        y_eq = b / (a + b)**2
        epsilon = 0.01

        x0 = x_eq + epsilon
        y0 = y_eq + epsilon

        # Time step values
        t_end = 50
        dt = 0.05

        # Solve using semi-implicit backward Euler method
        time, x, y = solve_semi_implicit_euler(x0, y0, t_end, dt, a, b)
        plt.plot(time, x, label="x")
        plt.plot(time, y, label="y")
        plt.title(f"Solution for a = {a}, b = {b}")
        plt.xlabel("Time")
        plt.ylabel("Concentration")
        plt.legend()
        plt.savefig(f"semi_implicit_backward_euler_{a}_{b}.png")
        plt.show()