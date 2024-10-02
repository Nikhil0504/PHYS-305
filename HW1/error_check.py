# Write code that uses the function from Problem 3 to compute the error between each of the 
# three integration methods and the analytic solution.  Use at least 7 different step sizes for each 
# method and determine how the error scales with step size.

from work_done import workdone
from math import log

import matplotlib.pyplot as plt

def work_done_analytical(V1, V2):
    """
    Calculate the work done analytically for an 
    ideal gas during an isothermal process.

    Parameters:
    V1 (float): Initial volume of the gas.
    V2 (float): Final volume of the gas.

    Returns:
    float: The work done by the gas during the expansion or compression.

    Notes:
    - The function assumes an ideal gas with a given number of 
    molecules (N) and thermal energy (kbT).
    - The natural logarithm (log) is used in the calculation.
    """
    N = 2.2e23
    kbT = 4e-14

    return N * kbT * log(V2/V1)


def error(X1, X2, steps, function, analytical):
    """
    Calculate the absolute error between numerical and analytical solutions.

    Parameters:
    X1 (float): The starting point of the interval.
    X2 (float): The ending point of the interval.
    steps (int): The number of steps to divide the interval into.
    function: A function that takes X1, X2, and steps as arguments 
    and returns three numerical solutions.
    analytical: A function that takes X1 and X2 as arguments and 
    returns the analytical solution.

    Returns:
    tuple: A tuple containing the absolute errors for the left, 
    right, and top numerical solutions.
    """
    lf, rh, tp = function(X1, X2, steps)
    an = analytical(X1, X2)

    return abs(an - lf), abs(an - rh), abs(an - tp)

if __name__ == "__main__":
    V1 = int(input("Enter initial volume: "))
    V2 = int(input("Enter final volume: "))

    # Define the step sizes from 1 to 1e7
    steps = [1 * 10**i for i in range(8)]
    lf_errs = []
    rh_errs = []
    tp_errs = []

    for step in steps:
        lf_err, rh_err, tp_err = error(V1, V2, step, workdone, work_done_analytical)
        lf_errs.append(lf_err)
        rh_errs.append(rh_err)
        tp_errs.append(tp_err)
        print(f"Step: {step}")
        print(f"Lefthand error: {lf_err}")
        print(f"Righthand error: {rh_err}")
        print(f"Trapezoidal error: {tp_err}")
        print()
    
    plt.plot(steps, lf_errs, 'o', label="Lefthand")
    plt.plot(steps, rh_errs, 'o', label="Righthand")
    plt.plot(steps, tp_errs, 'o', label="Trapezoidal")
    plt.xlabel("Step size")
    plt.ylabel("Error")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.show()
    
