# U = -g^2 e^(- lambda r) / r
# F = g^2 e^(- lambda r) / r^3  (\lambda r + 1) (r_2 - r_1)

from importlib import metadata
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
import numpy as np

m1 = 1
m2 = 1
t_end = 30
dt = 0.01
skip = 10

metadata = dict(title='Yukawa Potential', artist='Matplotlib')
writer = FFMpegWriter(fps=15, metadata=metadata)

fig, ax = plt.subplots()
l1, = ax.plot([], [], 'bo')
l2, = ax.plot([], [], 'ro')

plt.xlim(-1, 1)
plt.ylim(-1, 1)

def Yukawa(m1, m2, t_end, dt, skip):
    g = 1
    lam = 0.5
    mu = m1 * m2 / (m1 + m2)
    steps = round(t_end / dt / skip)

    r1 = np.zeros((steps, 2))
    r2 = np.zeros((steps, 2))
    v1 = np.zeros((steps, 2))
    v2 = np.zeros((steps, 2))
    time = np.zeros((steps, 1))

    # COM initial conditions
    r1[0, 0] = -m2 / (m1 + m2)
    r2[0, 0] = m1 / (m1 + m2)
    v1[0, 1] = -np.sqrt(3*mu*np.exp(-0.5)/2)/m1
    v2[0, 1] = np.sqrt(3*mu*np.exp(-0.5)/2)/m2

    # Midpoint variables
    r1mid = np.zeros((1, 2))
    r2mid = np.zeros((1, 2))
    v1mid = np.zeros((1, 2))
    v2mid = np.zeros((1, 2))

    with writer.saving(fig, "yukawa_potential.mp4", 100):
        for i in range(1, steps):
            r1[i, :] = r1[i - 1, :]
            r2[i, :] = r2[i - 1, :]
            v1[i, :] = v1[i - 1, :]
            v2[i, :] = v2[i - 1, :]
            time[i] = time[i - 1]

            l1.set_data(r1[i,0],r1[i,1])
            l2.set_data(r2[i,0],r2[i,1])
            writer.grab_frame()
            plt.pause(0.02)

            for _ in range(skip):
                r1mid[0, :] = r1[i, :] + 0.5 * dt * v1[i, :]
                r2mid[0, :] = r2[i, :] + 0.5 * dt * v2[i, :]

                r = np.linalg.norm(r1mid - r2mid)
                Fmag = g**2 * np.exp(-lam * r) * (lam * r + 1) / r**3 

                v1mid[0, :] = 0.5 * v1[i, :]
                v2mid[0, :] = 0.5 * v2[i, :]

                v1[i,:] += dt * Fmag * (r2[i,:]- r1[i,:]) / m1
                v2[i,:] += dt * Fmag * (r1[i,:]- r2[i,:]) / m2

                v1mid[0, :] += 0.5 * v1[i, :]
                v2mid[0, :] += 0.5 * v2[i, :]

                r1[i, :] += dt * v1mid[0, :]
                r2[i, :] += dt * v2mid[0, :]
        
    return r1, r2, v1, v2, time


r1, r2, v1, v2, time = Yukawa(m1, m2, t_end, dt, skip)

