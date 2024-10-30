import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter


def AdvectionCD(v,D,gamma,L,N,TotalTime,dt, Skip):
# simulates the motion of particles that are driven by a
# velocity v and are contained in a region of size L.
# Periodic boundary conditions are used.
# define parameters
    Nsteps = math.ceil(TotalTime/dt/Skip)
    # Number of time steps
    # define grid
    x,dx = np.linspace(-L/2,L/2,N,retstep=True)
    Time = [Skip*dt*i for i in range(Nsteps)]
    # initialize concentration matrix
    C = np.zeros((N,Nsteps))
    # define initial condition
    C[:,0] = 1
    
    # initialize first derivative array
    dC = np.zeros(N)
    d2C = np.zeros(N)

    metadata = dict(title='Diffuse', artist='Matplotlib')
    writer = FFMpegWriter(fps=15, metadata=metadata)
    fig1 = plt.figure()
    l, = plt.plot([], [],'b-')
    plt.xlim(-L/2,L/2)
    plt.ylim(0,1)

    with writer.saving(fig1,"AdvectionCD.mp4",100):
        for i in range(1,Nsteps):
            C[:,i] = C[:,i-1]
            for _ in range(Skip):
        # compute first derivative
                d2C[0] = 2/(dx**2)*(C[1,i-1] - C[0,i-1]) + 1/dx * (2 - C[0, i-1])
                dC[0] = 1/dx * (C[0, i] - C[1, i]) + 2 - C[0, i]
                dC[1:N-1] = (C[2:N,i-1] - C[:N-2,i-1])/(2*dx)
                d2C[1:N-1] = (C[2:N, i] - 2 * C[1:N-1, i] + C[:N-2, i]) / dx**2
                dC[N-1] = 2/(dx**2)*(C[0,i-1] - C[N-1,i-1]) + 1/dx*(2 + C[N-1,i-1])
                d2C[N-1] = 1/dx*(C[N-1,i-1] - C[0,i-1]) + 2 + C[N-1,i-1]
                # time step concentration
                C[:,i] = -gamma*C[:,i-1] - dt*v*dC[:] + D*dt*d2C[:]
            l.set_data(x,C[:,i])
            writer.grab_frame()
            plt.pause(0.01)
    cmap = plt.get_cmap('inferno')
    fig2,ax2 = plt.subplots()
    im = ax2.pcolormesh(Time,x,C,shading='auto',cmap=cmap)
    plt.show()
    return Time,C


AdvectionCD(1/4,1/2,1,2,100,10,1e-4, 100)