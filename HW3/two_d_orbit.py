# F = -k r + q/r^3 r
# k/m = 1
# Solve for the two- dimensional orbits in order to determine 
# how the orbits depend on q/m. Use initial conditions
# such that when q = 0, the orbit is circular.

# d2x/dt2 = -x/r + q/m x/r^3
# d2y/dt2 = -y/r + q/m y/r^3
# r = sqrt(x^2 + y^2)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

def f(r, q_m):
    r_norm = np.linalg.norm(r)
    return -r / r_norm + q_m * r / r_norm**3


def simulate(r_array, v_array, q_m, f, k_m, dt, steps, writer, fig, ax):
    trajectory = []
    with writer.saving(fig, "2d_orbit.mp4", 100):
        for i in range(1, steps):
            F = f(r_array[i-1], q_m)
            a = F / k_m
            v_array[i] = v_array[i-1] + a * dt
            r_array[i] = r_array[i-1] + v_array[i] * dt

            trajectory.append(r_array[i])

            # l1.set_data(r_array[i][0], r_array[i][1])
            # trace1.set_data(*zip(*trajectory))

            # writer.grab_frame()
    ax.plot(*zip(*trajectory), '-', label=f'q/m = {q_m}')
        

if __name__ == '__main__':
    k_m = 1

    dt = 0.1
    t_end = 100

    steps = int(t_end // dt)
    r0 = np.array([1.0, 0.0])
    v0 = np.array([0.0, 1.0])

    r_array = np.zeros((steps, 2))
    v_array = np.zeros((steps, 2))
    r_array[0] = r0
    v_array[0] = v0

    q_ms = [0.0, 0.5, 1.0, 2.0]

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))

    metadata = dict(title='2D Orbit', artist='Matplotlib')
    writer = FFMpegWriter(fps=15, metadata=metadata)

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # ax.set_xlim(-1.5, 1.5)
    # ax.set_ylim(-1.5, 1.5)
    # l1, = ax.plot([], [], 'bo', markersize=5)  # Earth
    # trace1, = ax.plot([], [], 'b-', alpha=0.5, linewidth=0.5)

    for q_m in q_ms:
        simulate(r_array, v_array, q_m, f, k_m, dt, steps, writer, fig, ax)

    ax.legend()
    fig.savefig('2d_orbit.png', dpi=300)
    plt.show()