# Write code that integrates sin x between two user-defined limits using the lefthand, righthand 
# and trapezoidal rules.  Determine the error in these integrations as a function of the step size.

from math import sin, cos
from work_done import lefthand, righthand, trapezoidal
from error_check import error

import matplotlib.pyplot as plt

def sin_anlytical(a, b):
    """
    Calculate the analytical integral of the sine function from a to b.

    Parameters:
    a (float): The lower limit of integration.
    b (float): The upper limit of integration.

    Returns:
    float: The result of the integral, which is cos(a) - cos(b).
    """
    return cos(a) - cos(b)

def sin_integral(a, b, steps):
    """
    Calculate the integral of the sine function over a given 
    interval using three different methods.

    Parameters:
    a (float): The start of the interval.
    b (float): The end of the interval.
    steps (int): The number of steps to divide the interval into.

    Returns:
    tuple: A tuple containing the integral estimates using the 
    left-hand rule, right-hand rule, and trapezoidal rule.
    """
    f = sin
    return (lefthand(a, b, steps, f), 
            righthand(a, b, steps, f), 
            trapezoidal(a, b, steps, f))

if __name__ == "__main__":
    a = 0
    b = 3.14159

    # Define the step sizes from 1 to 1e7
    steps = [1 * 10**i for i in range(8)]
    lf_errs = []
    rh_errs = []
    tp_errs = []

    print("Analytical solution: ", sin_anlytical(a, b))

    for step in steps:
        lf_err, rh_err, tp_err = error(a, b, step, sin_integral, sin_anlytical)
        print(f"Step: {step}")
        print(f"Lefthand error: {lf_err}")
        print(f"Righthand error: {rh_err}")
        print(f"Trapezoidal error: {tp_err}")
        print()
        lf_errs.append(lf_err)
        rh_errs.append(rh_err)
        tp_errs.append(tp_err)
    
    plt.plot(steps, lf_errs, 'o', label="Lefthand")
    plt.plot(steps, rh_errs, 'o', label="Righthand")
    plt.plot(steps, tp_errs, 'o', label="Trapezoidal")
    plt.xlabel("Step size")
    plt.ylabel("Error")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.show()
