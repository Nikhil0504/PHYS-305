from polyfit import FitDatatoLine

import matplotlib.pyplot as plt
import numpy as np

# fit data using lambda d^2 f/dx^2 - f = f_data
def regularized_fit(x, f_data, lambda_):
    dx = x[1] - x[0]

    fits = {}
    for lam in lambda_:
        # matrix
        n = len(x)
        matrix = np.zeros((n, n))
        main_dig = -1 - 2 * lam / (dx**2)
        np.fill_diagonal(matrix, main_dig)

        off_dig = lam / (dx**2)
        np.fill_diagonal(matrix[:, 1:], off_dig)
        np.fill_diagonal(matrix[1:], off_dig)

        matrix[0, 0] = -1 / dx
        matrix[0, 1] = 1 / dx

        # rhs should contain 0 then f_data
        rhs = np.zeros(n)
        rhs[1:] = f_data[1:]

        # solve
        f = np.linalg.solve(matrix, rhs)
        fits[lam] = -f
    
    return fits

x, y = FitDatatoLine('Problem2_data.txt')
data = np.loadtxt('Problem2_data.txt')

# third order polynomial
a = np.polyfit(data[:, 0], data[:, 1], 3)
y_poly = np.polyval(a, data[:, 0])

plt.plot(data[:, 0], data[:, 1], 'o', label='Data')
plt.plot(data[:, 0], y_poly, '-', label='Third order polynomial')
plt.plot(x, y, '--', label='Fitted line')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.savefig('third_poly.png')
plt.show()


lambda_ = [1e-3, 1e-2, 1e-1, 1, 10]
fits = regularized_fit(x, data[:, 1], lambda_)
plt.plot(data[:, 0], data[:, 1], 'o', label='Data')

for lam in lambda_:
    plt.plot(x, fits[lam], label=f'$\lambda$ = {lam}')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.savefig('third_poly_with_lambda.png')
plt.show()