import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

def Diffusion(TotalTime, dt, Skip, D, N, size):
    Steps = round(TotalTime/dt/Skip)

    x, dx = np.linspace(-size / 2, size / 2, N, retstep=True)
    Time = [Skip*dt*i for i in range(Steps)]

    C = np.zeros((N, Steps))
    C[:, 0] = np.exp(-x**2/0.1**2)

    dCd2 = np.zeros(N)

    metadata = dict(title='Diffusion', artist='Matplotlib')
    writer = FFMpegWriter(fps=15, metadata=metadata, bitrate=3000, codec='h264')

    fig1 = plt.figure()
    data, = plt.plot([], [], 'b-')

    plt.xlim(x[0], x[-1])
    plt.ylim(0, 1)

    with writer.saving(fig1, "Diffusion.mp4", 100):
        for i in range(1, Steps):
            C[:, i] = C[:, i-1]

            for _ in range(Skip):
                dCd2[0] = 2 * (C[1, i] - C[0, i]) / dx**2
                dCd2[1:N-1] = (C[2:N, i] - 2 * C[1:N-1, i] + C[:N-2, i]) / dx**2
                dCd2[N-1] = 2 * (C[N-2,i] - C[N-1,i]) / dx**2

                C[:, i] += D * dt * dCd2
        
            data.set_data(x, C[:, i])
            writer.grab_frame()
            plt.pause(0.02)
    
    cmap = plt.get_cmap('inferno')

    fig2, ax2 = plt.subplots()
    im = ax2.pcolormesh(Time, x, C, cmap=cmap)

    plt.show()

    return C, Time

if __name__ == "__main__":
    C, Time = Diffusion(10, 0.001/4, 50, 0.01, 250, 1)
