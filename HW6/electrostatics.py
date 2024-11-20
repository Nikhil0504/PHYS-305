import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def LaplaceMissingRect(Hout, Wout, Hin, Win, Xin, Yin, Nx, Ny, V0):
    # solve Laplace’s equation in a rectangular domain
    # of height Hout and width Wout that has a rectangular
    # conductor of size Hin by Win inside it with bottom left
    # corner at (Xin,Yin). The number of gridpoints
    # in x and y are Nx and Ny, respectively. 
    # The outer conductor is grounded and the inner one is at potential V0.

    # make grid
    x, dx = np.linspace(0, Wout, Nx, retstep=True)
    y, dy = np.linspace(0, Hout, Ny, retstep=True)

    # initialize potential
    X, Y = np.meshgrid(x, y)

    # mask out location of inner conductor
    InMask = (X >= Xin) & (X <= (Xin + Win)) & (Y >= Yin) & (Y <= (Yin + Hin))
    Mask = ~InMask

    # find Edge of Inner Mask
    Edge = InMask & np.roll(InMask, 1, axis=1) # left edge
    Edge |= InMask & np.roll(InMask, -1, axis=1) # right edge
    Edge |= InMask & np.roll(InMask, 1, axis=0) # bottom edge
    Edge |= InMask & np.roll(InMask, -1, axis=0) # top edge

    Mask |= Edge
    Unknowns = np.count_nonzero(Mask)

    Link = -np.ones((Ny, Nx)).astype(int)
    Link[Mask] = np.arange(Unknowns)

    Lap = np.zeros((Unknowns, Unknowns))
    Del = [dy, dx]

    for i in range(2):
        Here = Mask & np.roll(Mask, 1, axis=i)
        SLink = np.roll(Link, 1, axis=i)

        Lap[Link[Here], Link[Here]] += -1/Del[i]**2
        Lap[Link[Here], SLink[Here]] += 1/Del[i]**2
        Lap[SLink[Here], Link[Here]] += 1/Del[i]**2
        Lap[Link[Here], SLink[Here]] += -1/Del[i]**2

    # define boundary conditions for top rows in Lap 
    Lap[Link[0, :], :] = 0
    Lap[Link[0, :], Link[0, :]] = 1

    Lap[Link[Ny-1, :], :] = 0
    Lap[Link[Ny-1, :], Link[Ny-1, :]] = 1

    Lap[Link[:, 0], :] = 0
    Lap[Link[:, 0], Link[:, 0]] = 1

    Lap[Link[:, Nx-1], :] = 0
    Lap[Link[:, Nx-1], Link[:, Nx-1]] = 1

    Lap[Link[Edge], :] = 0
    Lap[Link[Edge], Link[Edge]] = 1

    # source vector
    b = np.zeros(Unknowns)
    b[Link[Edge]] = V0

    Phi = np.zeros((Ny, Nx))
    Phi[Mask] = np.linalg.solve(Lap, b)
    Phi[~Mask] = V0

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Phi, cmap=cm.jet, antialiased=False, vmin=0, vmax=V0)
    ax.set_xlim(-0.2, Wout+0.2)
    ax.set_ylim(-0.2, Hout+0.2)
    ax.set_zlim(-0.2, 1.2*V0)
    plt.show()

    return Phi
    
if __name__ == "__main__":
    LaplaceMissingRect(40, 10, 4, 10, 2, 2, 160, 60, 1) 
