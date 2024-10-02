import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import numpy as np

# Constants
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2

# Masses (in kg)
m_sun = 1.989e30
m_earth = 5.972e24
m_jupiter = 1.898e27
m_moon = 7.348e22

# Initial conditions: positions (in meters)
# Using AU (astronomical units) for simplicity, 1 AU = 1.496e11 m
r_sun = np.array([0, 0])
r_earth = np.array([1.496e11, 0])  # 1 AU from the Sun
r_jupiter = np.array([7.785e11, 0])  # 5.2 AU from the Sun
r_moon = r_earth + np.array([3.844e8, 0])  # 384,400 km from Earth

# Initial velocities (in meters per second)
v_sun = np.array([0, 0])
v_earth = np.array([0, 29.78e3])  # Earth's orbital speed around the Sun
v_jupiter = np.array([0, 13.07e3])  # Jupiter's orbital speed around the Sun
v_moon = v_earth + np.array([0, 1.022e3])  # Moon's speed relative to Earth

# Set up time parameters
t_end = 3.75e8  # Enough time for Jupiter to complete one orbit (~12 years)
dt = 1e5  # Time step in seconds
steps = int(t_end // dt)

# Prepare arrays to store the positions and velocities
r_sun_array = np.zeros((steps, 2))
r_earth_array = np.zeros((steps, 2))
r_jupiter_array = np.zeros((steps, 2))
r_moon_array = np.zeros((steps, 2))

r_sun_array[0] = r_sun
r_earth_array[0] = r_earth
r_jupiter_array[0] = r_jupiter
r_moon_array[0] = r_moon

v_sun_array = np.zeros((steps, 2))
v_earth_array = np.zeros((steps, 2))
v_jupiter_array = np.zeros((steps, 2))
v_moon_array = np.zeros((steps, 2))

v_sun_array[0] = v_sun
v_earth_array[0] = v_earth
v_jupiter_array[0] = v_jupiter
v_moon_array[0] = v_moon

def gravitational_force(m1, m2, r1, r2):
    r = np.linalg.norm(r1 - r2)
    if r == 0:
        return np.zeros(2)
    force = G * m1 * m2 / r**3 * (r2 - r1)
    return force

fig, ax = plt.subplots(1, 1, figsize=(6, 6))
metadata = dict(title='4-Body Problem', artist='Matplotlib')
writer = FFMpegWriter(fps=15, metadata=metadata)

ax.set_xlim(-8e11, 8e11)
ax.set_ylim(-8e11, 8e11)
l1, = ax.plot([], [], 'y*', markersize=10)  # Sun
l2, = ax.plot([], [], 'bo', markersize=5)   # Earth
l3, = ax.plot([], [], 'ro', markersize=7)   # Jupiter
l4, = ax.plot([], [], 'go', markersize=3)   # Moon

trace1, = ax.plot([], [], 'y-')
trace2, = ax.plot([], [], 'b-', alpha=0.5, linewidth=0.5)
trace3, = ax.plot([], [], 'r-')
trace4, = ax.plot([], [], 'g-', alpha=0.5, linewidth=0.5)

def simulate():
    with writer.saving(fig, "4body_simulation.mp4", 100):
        for i in range(1, steps):
            # Calculate forces between each pair of bodies
            F_sun_earth = gravitational_force(m_sun, m_earth, r_sun_array[i-1], r_earth_array[i-1])
            F_sun_jupiter = gravitational_force(m_sun, m_jupiter, r_sun_array[i-1], r_jupiter_array[i-1])
            F_sun_moon = gravitational_force(m_sun, m_moon, r_sun_array[i-1], r_moon_array[i-1])
            F_earth_jupiter = gravitational_force(m_earth, m_jupiter, r_earth_array[i-1], r_jupiter_array[i-1])
            F_earth_moon = gravitational_force(m_earth, m_moon, r_earth_array[i-1], r_moon_array[i-1])
            F_jupiter_moon = gravitational_force(m_jupiter, m_moon, r_jupiter_array[i-1], r_moon_array[i-1])

            # Calculate net forces on each body
            F_sun = F_sun_earth + F_sun_jupiter + F_sun_moon
            F_earth = -F_sun_earth + F_earth_jupiter + F_earth_moon
            F_jupiter = -F_sun_jupiter - F_earth_jupiter + F_jupiter_moon
            F_moon = -F_sun_moon - F_earth_moon - F_jupiter_moon

            # Update velocities
            v_sun_array[i] = v_sun_array[i-1] + dt * F_sun / m_sun
            v_earth_array[i] = v_earth_array[i-1] + dt * F_earth / m_earth
            v_jupiter_array[i] = v_jupiter_array[i-1] + dt * F_jupiter / m_jupiter
            v_moon_array[i] = v_moon_array[i-1] + dt * F_moon / m_moon

            # Update positions
            r_sun_array[i] = r_sun_array[i-1] + dt * v_sun_array[i]
            r_earth_array[i] = r_earth_array[i-1] + dt * v_earth_array[i]
            r_jupiter_array[i] = r_jupiter_array[i-1] + dt * v_jupiter_array[i]
            r_moon_array[i] = r_moon_array[i-1] + dt * v_moon_array[i]

            # Update the plot every N steps
            if i % 100 == 0:
                l1.set_data(r_sun_array[i, 0], r_sun_array[i, 1])
                l2.set_data(r_earth_array[i, 0], r_earth_array[i, 1])
                l3.set_data(r_jupiter_array[i, 0], r_jupiter_array[i, 1])
                l4.set_data(r_moon_array[i, 0], r_moon_array[i, 1])

                trace1.set_data(r_sun_array[:i, 0], r_sun_array[:i, 1])
                trace2.set_data(r_earth_array[:i, 0], r_earth_array[:i, 1])
                trace3.set_data(r_jupiter_array[:i, 0], r_jupiter_array[:i, 1])
                trace4.set_data(r_moon_array[:i, 0], r_moon_array[:i, 1])

                writer.grab_frame()
                plt.pause(0.01)

# Run the simulation
simulate()
plt.show()

