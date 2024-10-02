#Write a function that computes the work done by an ideal gas when it expands from one 
#volume to another.  The volumes and the number of steps should be arguments to the 
#function.  Compute the work done using the lefthand, righthand, and trapezoidal rules. The 
#code should return the three solutions.

# W = int P dV
# P = nRT/V
def lefthand(a, b, n, f):   
    """
    Approximates the integral of a function f 
    over the interval [a, b] using the left hand rule.

    Parameters:
    a (float): The start of the interval.
    b (float): The end of the interval.
    n (int): The number of subintervals.
    f (function): The function to integrate. It should take a single argument and return a float.

    Returns:
    float: The approximate integral of the function f over [a, b].
    """
    dx = (b - a) / n
    return sum(f(a + i * dx) * dx for i in range(n))

def righthand(a, b, n, f):
    """
    Approximates the integral of a function f 
    over the interval [a, b] using the right hand rule.

    Parameters:
    a (float): The start of the interval.
    b (float): The end of the interval.
    n (int): The number of subintervals.
    f (function): The function to integrate. It should take a single argument and return a float.

    Returns:
    float: The approximate integral of the function f over [a, b].
    """
    dx = (b - a) / n
    return sum(f(a + i * dx) * dx for i in range(1, n + 1))

def trapezoidal(a, b, n, f):
    """
    Approximates the integral of a function f 
    over the interval [a, b] using the trapezoidal rule.

    Parameters:
    a (float): The start of the interval.
    b (float): The end of the interval.
    n (int): The number of subintervals.
    f (function): The function to integrate. It should take a single argument and return a float.

    Returns:
    float: The approximate integral of the function f over [a, b].
    """
    dx = (b - a) / n
    return sum((f(a + i * dx) + f(a + (i + 1) * dx)) * dx / 2 for i in range(n))

def pressure(V):
    """
    Calculate the pressure of an ideal gas using the ideal gas law.

    Parameters:
    V (float): Volume of the gas.

    Returns:
    float: Pressure of the gas.

    Notes:
    - The function assumes an ideal gas with a given number of 
    molecules (N) and thermal energy (kbT).
    """
    N = 2.2e23
    kbT = 4e-14

    return N * kbT / V

def workdone(V1, V2, steps):
    f = pressure
    
    return lefthand(V1, V2, steps, f), righthand(V1, V2, steps, f), trapezoidal(V1, V2, steps, f)

if __name__ == "__main__":
    Vi = int(input("Enter initial volume: "))
    Vf = int(input("Enter final volume: "))
    steps = int(input("Enter number of steps: "))
    print(workdone(Vi, Vf, steps))
