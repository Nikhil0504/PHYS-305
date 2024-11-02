import numpy as np
import matplotlib.pyplot as plt
from math import pi, sqrt

def BrownianParticles(N, R, L, TotalTime, dt, Skip):
    m = 4 * pi * R**3 / 3  # Mass (relative to particle radius)
    kBT = 2  # Thermal energy
    eta = 0.001  # Viscosity
    zeta = 6 * pi * eta * R  # Friction coefficient
    c = zeta * sqrt(kBT / m)  # Brownian noise scaling
    
    e = 0.03 * zeta * np.sqrt(kBT / m)  # Depth of the LJ potential
    sigma = 2 * R  # Interaction distance based on particle size
    
    Steps = round(TotalTime / dt / Skip)
    
    # Initialize positions of particles randomly within box dimensions
    x = np.zeros((2, N, Steps))
    x[:, :, 0] = L * np.random.rand(2, N)
    
    # Main simulation loop
    for i in range(1, Steps):
        for _ in range(Skip):
            # Brownian motion component
            xi = c * np.random.randn(2, N)
            
            # Distance calculations between particles
            Dx = x[0, :, i-1][:, np.newaxis] - x[0, :, i-1]
            Dy = x[1, :, i-1][:, np.newaxis] - x[1, :, i-1]
            
            # Apply periodic boundary conditions for distance calculations
            Dx = Dx - L * np.round(Dx / L)
            Dy = Dy - L * np.round(Dy / L)
            
            r = np.sqrt(Dx**2 + Dy**2)
            np.fill_diagonal(r, 10)  # Avoid division by zero in self-interaction
            
            # Lennard-Jones force magnitude with cutoff
            FiMag = (6 * e / sigma**2) * (2 * (sigma / r)**14 - (sigma / r)**8)
            FiMag = np.clip(FiMag, None, 1000)  # Clip force to max value
            
            # Calculate forces in x and y directions
            Fi = np.zeros((2, N))
            Fi[0, :] = np.sum(FiMag * Dx, axis=1)
            Fi[1, :] = np.sum(FiMag * Dy, axis=1)
            
            # Update positions with Brownian and interaction forces
            x[:, :, i] = x[:, :, i-1] + (dt / zeta) * (xi + Fi)
            
            # Apply periodic boundary conditions
            x[0, :, i] = np.mod(x[0, :, i], L)
            x[1, :, i] = np.mod(x[1, :, i], L)
    
    # Plot final positions
    plt.figure(figsize=(6, 6))
    plt.plot(x[0, :, -1], x[1, :, -1], 'oy', markersize=4)
    plt.xlim(0, L)
    plt.ylim(0, L)
    plt.xlabel("x (μm)")
    plt.ylabel("y (μm)")
    plt.title("Final Positions of Brownian Particles")
    plt.show()

# Run the simulation
BrownianParticles(500, 1e-2, 1, 0.005, 1e-5, 500)
