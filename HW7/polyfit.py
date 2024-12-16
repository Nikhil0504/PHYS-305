import numpy as np
import matplotlib.pyplot as plt


def FitDatatoLine(datafile):
    data = np.loadtxt(datafile)
    N, d = data.shape

    x = data[:, 0]

    M = np.zeros((4, 4))
    M[:, 0] = [N, np.sum(x), np.sum(x**2), np.sum(x**3)]
    M[:, 1] = [np.sum(x), np.sum(x**2), np.sum(x**3), np.sum(x**4)]
    M[:, 2] = [np.sum(x**2), np.sum(x**3), np.sum(x**4), np.sum(x**5)]
    M[:, 3] = [np.sum(x**3), np.sum(x**4), np.sum(x**5), np.sum(x**6)]

    b = np.zeros((4, 1))
    b[:, 0] = [np.sum(data[:, 1]), np.sum(x * data[:, 1]),
               np.sum(x**2 * data[:, 1]), np.sum(x**3 * data[:, 1])]

    a = np.linalg.solve(M, b)

    y = a[0] + a[1] * x + a[2] * x**2 + a[3] * x**3

    return x, y

if __name__ == "__main__":
    FitDatatoLine('Data1.txt')
