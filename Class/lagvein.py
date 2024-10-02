import numpy as np
import matplotlib.pyplot as plt


def Lagvein1D(R, totaltime, dt):
    m = 4 * np.pi * R**3 / 3
    kBT = 4e-14
    eta = 0.01
    zeta = 6*np.pi*eta*R
    c = zeta * np.sqrt(kBT / m)

    Steps = round(totaltime / dt)

    x = np.zeros((2, Steps), 'float')
    v = np.zeros((2, Steps), 'float')
    time = np.array([i * dt for i in range(Steps)], 'float')

    for i in range(Steps):
        xi = c * np.random.randn(2)

        v[:, i] = ((1-zeta*dt/2/m)*v[:,i-1] + dt*xi/m)/(1+zeta*dt/2/m)
        vmid = 0.5*( v[:,i] + v[:,i-1] )
        x[:,i] = x[:,i-1] + dt*vmid
    
    plt.plot(x[0,:],x[1,:])
    plt.show()
    return time,x,v

Lagvein1D(1, 10, 0.01)
                    