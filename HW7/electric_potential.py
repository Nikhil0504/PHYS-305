import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

def PoissonSolver(height, width, Nx, Ny, charge_density_func):
    epsilon0 = 1

    # Create grid
    x, dx = np.linspace(0, width, Nx, retstep=True)
    y, dy = np.linspace(0, height, Ny, retstep=True)
    X, Y = np.meshgrid(x, y)

    num_unknowns = Nx * Ny
    indices = np.arange(num_unknowns).reshape((Ny, Nx))

    # Initialize Laplacian matrix
    Laplacian = np.zeros((num_unknowns, num_unknowns))
    Laplacian[indices, indices] = -2 / dx**2 - 2 / dy**2
    Laplacian[indices, np.roll(indices, 1, axis=1)] += 1 / dx**2
    Laplacian[indices, np.roll(indices, -1, axis=1)] += 1 / dx**2
    Laplacian[indices, np.roll(indices, 1, axis=0)] += 1 / dy**2
    Laplacian[indices, np.roll(indices, -1, axis=0)] += 1 / dy**2

    # Apply boundary conditions
    for boundary in [indices[0, :], indices[-1, :], indices[:, 0], indices[:, -1]]:
        Laplacian[boundary, :] = 0
        Laplacian[boundary, boundary] = 1

    # Create charge density vector
    rho = charge_density_func(X, Y)
    b = -rho.flatten() / epsilon0

    # Apply boundary conditions to b
    for boundary in [indices[0, :], indices[-1, :], indices[:, 0], indices[:, -1]]:
        b[boundary] = 0

    # Solve for potential
    potential = np.linalg.solve(Laplacian, b)
    potential = potential.reshape((Ny, Nx))

    return X, Y, potential

# Charge density function
def charge_density_func(x, y):
    return np.sin(2 * np.pi * x) * (np.sin(np.pi * y)**2)

charge_density_func = np.vectorize(charge_density_func)

X, Y, potential = PoissonSolver(height=2, width=4, Nx=100, Ny=50, charge_density_func=charge_density_func)

# Plot the potential
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, Y, potential, cmap=cm.jet)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('Potential (Φ)')
ax.set_title('Electric Potential')
fig.savefig('electric_potential.png')
plt.show()

