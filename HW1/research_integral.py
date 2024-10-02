import math
from work_done import trapezoidal

# Define the function as 1 - e^(-x) / x(1 + x^2)
# f = lambda x: (1 - math.exp(-x)) / (x * (1 + x**2))
def f(x):
    """
    Compute the value of the function f(x) = (1 - exp(-x)) / (x * (1 + x^2)).

    Parameters:
    x (float): The input value for which the function is evaluated.

    Returns:
    float: The computed value of the function at the given input x.
    """
    return (1 - math.exp(-x)) / (x * (1 + x**2))

# Define the cutoff value
lambda_val = 22.36

# Define the step size
delta_x = 0.0316

# Calculate the number of intervals
n = int((lambda_val - 0) / delta_x)

print(trapezoidal(1e-6, 22.36, n, f))