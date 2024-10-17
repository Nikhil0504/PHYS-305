import numpy as np
import matplotlib.pyplot as plt

def forward_euler(m, v0, zeta, alpha, beta, r1_init, r2_init, v1_init, v2_init, d1_init, d2_init, dt, steps):
    # Initialize variables
    r1, r2 = r1_init, r2_init
    v1, v2 = v1_init, v2_init
    d1, d2 = d1_init, d2_init
    
    positions_r1 = []
    positions_r2 = []
    velocities_v1 = []
    velocities_v2 = []
    
    for _ in range(steps):
        # Compute r and its magnitude
        r = np.linalg.norm(r1 - r2)

        # equations of motion
        dv1_dt = (zeta / m) * (v0 * d1 - v1) + (alpha / (m * r)) * (v2 - v1)
        dv2_dt = (zeta / m) * (v0 * d2 - v2) + (alpha / (m * r)) * (v1 - v2)
        
        
        dd1_dt = (beta / r**2) * np.cross(np.cross(d1, d2), d1)
        dd2_dt = (beta / r**2) * np.cross(np.cross(d2, d1), d2)
        
        # Update velocities and directions using forward Euler method
        v1 += dv1_dt * dt
        v2 += dv2_dt * dt
        d1 += dd1_dt * dt
        d2 += dd2_dt * dt

        # Normalize d1 and d2 to ensure they remain unit vectors
        d1 /= np.linalg.norm(d1)
        d2 /= np.linalg.norm(d2)
        
        # Update positions
        r1 += v1 * dt
        r2 += v2 * dt
        
        positions_r1.append(r1.copy())
        positions_r2.append(r2.copy())
        velocities_v1.append(v1.copy())
        velocities_v2.append(v2.copy())
    
    return np.array(positions_r1), np.array(positions_r2), np.array(velocities_v1), np.array(velocities_v2)

# Example usage of the function
m = 1.0  # mass
v0 = 1.0  # constant swimming speed
zeta = 0.5  # constant
alpha = 0.1  # constant
beta = 0.2  # constant
dt = 0.01  # time step
steps = 1000  # number of steps

# Initial positions and velocities
r1_init = np.array([1.0, 0.0, 0.0])
r2_init = np.array([-1.0, 0.0, 0.0])
v1_init = np.array([0.0, 1.0, 0.0])
v2_init = np.array([0.0, -1.0, 0.0])
d1_init = np.array([1.0, 0.0, 0.0])
d2_init = np.array([-1.0, 0.0, 0.0])

# Run the forward Euler solver
positions_r1, positions_r2, velocities_v1, velocities_v2 = forward_euler(m, v0, zeta, alpha, beta, r1_init, r2_init, v1_init, v2_init, d1_init, d2_init, dt, steps)

# Plot the trajectories of the two objects
plt.figure(figsize=(10, 6))

plt.plot(positions_r1[:, 0], positions_r1[:, 1], label="Object 1 Trajectory", color='blue')
plt.plot(positions_r2[:, 0], positions_r2[:, 1], label="Object 2 Trajectory", color='red')

plt.title("Trajectories of Two Self-Propelled Objects")
plt.xlabel("x position")
plt.ylabel("y position")
plt.legend()
plt.grid(True)
plt.show()
