import numpy as np
import matplotlib.pyplot as plt

seed = 42
np.random.seed(seed)

def BrownianParticles(N, R, L, TotalTime, dt, Skip, sigma, e):
    kBT = 0.004
    eta = 0.001
    zeta = 6*np.pi*eta*R
    c = zeta * np.sqrt(kBT)

    Steps = round(TotalTime/dt/Skip)
    Time = np.arange(0,TotalTime,dt*Skip)

    x = np.zeros((2, N, Steps))
    x[:, :, 0] = L * np.random.rand(2, N)

    Fi = np.zeros((2, N))

    for i in range(1,Steps):
        x[:, :, i] = x[:, :, i-1]

        for _ in range(Skip):
            # compute the random force
            xi = c * np.random.randn(2, N)

            # interaction force
            Dx = np.meshgrid(x[0, :, i-1])
            Dx -= Dx.transpose()

            Dy = np.meshgrid(x[1, :, i-1])
            Dy -= Dy.transpose()

            # boundary conditions
            Dx[Dx < -L/2] += L
            Dx[Dx > L/2] -= L

            Dy[Dy < -L/2] += L
            Dy[Dy > L/2] -= L

            r = np.sqrt(Dx**2 + Dy**2)
            
            np.fill_diagonal(r, 10)

            FiMag = e*((sigma/r)**(14) - (sigma/r)**8)
            Fi[0,:] = np.sum(FiMag*Dx,axis=1)
            Fi[1,:] = np.sum(FiMag*Dy,axis=1)

            x[:, :, i] += (dt/zeta)*(xi + Fi)

            # boundary conditions
            Mask = x[0,:,i]>L
            x[0,Mask,i] = x[0,Mask,i] - L
            Mask = x[0,:,i]<0
            x[0,Mask,i] = x[0,Mask,i] + L
            Mask = x[1,:,i]>L
            x[1,Mask,i] = x[1,Mask,i] - L
            Mask = x[1,:,i]<0
            x[1,Mask,i] = x[1,Mask,i] + L
    
    return Time, x

            

BrownianParticles(2, 1, 10, 10, 0.01, 1)