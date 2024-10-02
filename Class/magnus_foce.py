# mass m, rotational velocity omega, rho air density,
# A cross sectional area, S/m = 4 * 10^-4
# m dv/dt = -m g z^hat - rho A |v| v + S omega cross v
# write equation that solves this equation given initial conditions (velcoity)
# this is known as the magnus force

import numpy as np
import matplotlib.pyplot as plt

def magnus_force(v, g, m, rho, A, S_m, omega):
    return -g - (rho * A * np.linalg.norm(v) * v) / m + S_m * np.cross(omega, v)


def runge_kutta_step(v, g, m, rho, A, S_m, omega, dt):
    k1 = dt * magnus_force(v, g, m, rho, A, S_m, omega)
    k2 = dt * magnus_force(v + 0.5 * k1, g, m, rho, A, S_m, omega)
    k3 = dt * magnus_force(v + 0.5 * k2, g, m, rho, A, S_m, omega)
    k4 = dt * magnus_force(v + k3, g, m, rho, A, S_m, omega)

    return v + (k1 + 2 * k2 + 2 * k3 + k4) / 6


def magnus_force_trajectory(v0, t0, tf, dt, g, m, rho, A, S_m, omega):
    t = np.arange(t0, tf, dt)
    v = np.zeros((len(t), 3))
    v[0] = v0

    for i in range(1, len(t)):
        v[i] = runge_kutta_step(v[i - 1], g, m, rho, A, S_m, omega, dt)

    return t, v


if __name__ == "__main__":
    # Initial conditions
    t0, tf, dt = 0, 10, 0.01

    g = np.array([0, 0, 9.81])

    m = 0.5
    A = 0.1

    S_m = 4e-4
    rho = 1.293

    # v0 = np.array([10, 0, 0])
    # omega = np.array([0, 0, 10])

    # check with multiple initial conditions
    v0s = [np.array([10, 0, 0]), np.array([0, 10, 0]), np.array([0, 0, 10])]
    omegas = [np.array([0, 0, 10]), np.array([0, 10, 0]), np.array([10, 0, 0])]

    fig, ax = plt.subplots(3, 1, figsize=(3, 6))
    ax = ax.flatten()

    for v0, omega in zip(v0s, omegas):
        t, v = magnus_force_trajectory(v0, t0, tf, dt, g, m, rho, A, S_m, omega)

        ax[0].plot(t, v[:, 0], label="x")
        ax[1].plot(t, v[:, 1], label="y")
        ax[2].plot(t, v[:, 2], label="z")

        plt.xlabel("Time (s)")
        plt.ylabel("Velocity (m/s)")
        # plt.legend()
    
    plt.show()