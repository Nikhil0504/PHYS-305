import numpy as np
import matplotlib.pyplot as plt

# Adjusting domain length to 4 * pi
L = 4 * np.pi  # New domain length
N = 100  # Number of points
dx = L / (N - 1)  # Grid spacing

# Discretized x domain
x = np.linspace(0, L, N)

# Reinitialize the coefficient matrix and RHS vector
A = np.zeros((N, N))
b = np.zeros(N)

# Fill the coefficient matrix using finite differences for the new domain
for i in range(1, N-1):
    A[i, i-1] = 1 / dx**2 - np.sin(x[i-1]) / (2 * dx)  # C_{i-1}
    A[i, i] = -2 / dx**2  # C_i
    A[i, i+1] = 1 / dx**2 + np.sin(x[i+1]) / (2 * dx)  # C_{i+1}

C0 = 1  # C(0)
CL = 0  # C(L)

# Apply boundary conditions
A[0, 0] = 1
A[N-1, N-1] = 1
b[0] = C0
b[N-1] = CL

# Solve the linear system
C = np.linalg.solve(A, b)

# Plot the result
plt.plot(x, C, label='C(x)')
plt.xlabel('x')
plt.ylabel('C(x)')
plt.title('Steady-State Solution for 4π Domain')
plt.legend()
plt.savefig('steady_state.png')
plt.show()
