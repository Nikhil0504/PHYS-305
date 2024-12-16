import numpy as np
import matplotlib.pyplot as plt
f = np.loadtxt('Problem4_data.txt')
amp = f[:, 1]
time = f[:, 0]
fFFT = np.fft.fft(amp)

PowSpec = np.conj(fFFT) * fFFT

freq = np.fft.fftfreq(len(amp), time[1] - time[0])

# dominant frequency (top 3)
dominant_freq = freq[np.argsort(PowSpec)[-6:]]
print(f'The dominant frequencies are {dominant_freq} Hz')

plt.plot(freq, PowSpec)
# dominant frequencies
plt.plot(dominant_freq, PowSpec[np.argsort(PowSpec)[-6:]], 'o', label='Dominant frequencies')
plt.legend()
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectrum')

plt.xlim(-3, 3)
# log y axis
plt.yscale('log')
plt.savefig('power_spectrum.png')
plt.show()
