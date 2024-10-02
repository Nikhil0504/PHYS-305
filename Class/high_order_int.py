# integral 1/sqrt(pi) int_1^10 e^(-v^2) v^2 dv

# using simpson's rule
import numpy as np

def integrand(v):
    return (1 / np.sqrt(np.pi)) * np.exp(-v**2) * v**2

a = 1
b = 10
n = 101
h = (b - a) / n

def simpson(a, b, n, f):
    x, dx = np.linspace(a, b, n+1, retstep=True)
    y = f(x)
    s = y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2])
    return s * dx / 3

print(simpson(a, b, n, integrand))