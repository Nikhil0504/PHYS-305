import numpy as np

def GJ(A,b):
    # peforms Gauss-Jordan elimination to solve A x = b
    W, L = A.shape
    B = A.astype(float)
    x = b.astype(float)

    vals = np.arange(W)

    for j in range(W):
        # check if diagonal element is zero, pivot if it is
        if B[j,j] == 0:
            # in the jth column find and number points that are nonzero
            nonzero_idx = j + np.nonzero(B[j:, j])[0][0]
            # swap rows in both B and x
            B[[j, nonzero_idx]] = B[[nonzero_idx, j]]
            x[[j, nonzero_idx]] = x[[nonzero_idx, j]]

        # divide the jth row of B by the diagonal element, likewise for x
        norm = B[j,j]
        B[j,:] /= norm
        x[j] /= norm

        # get mask for rows to update (all except j where B[:,j] is nonzero)
        mask = (vals != j) & (B[:,j] != 0)
        
        # vectorized row operations
        norms = B[mask,j]
        B[mask,:] -= np.outer(norms, B[j,:])
        x[mask] -= norms * x[j]
    
    return x


N = 500
# define a large second derivative matrix
A = np.zeros((N,N))
A[0,0] = 1
A[1:N-1, 0:N-2] += np.eye(N-2)
A[1:N-1, 1:N-1] -= 2 * np.eye(N-2)
A[1:N-1, 2:N] += np.eye(N-2)

A[N-1,N-1] = 1
print(A)
# define the solution vector
b = np.ones(N)# put in correct boundary conditions
b[0] = 0
b[N-1] = 0

from time import time
t1 = time()
x1 = GJ(A,b)
t2 = time()
print(f'GJ time: {t2-t1:.4f}')

# t3 = time()
# x2 = np.linalg.solve(A,b)
# t4 = time()

# print(f'numpy time: {t4-t3:.4f}')

# from scipy.sparse.linalg import spsolve
# from scipy.sparse import csr_matrix
# t5 = time()
# x3 = spsolve(csr_matrix(A),b)
# t6 = time()
# print(f'spsolve time: {t6-t5:.4f}')

# # check if the two solutions are the same
# print(np.allclose(x1,x2))
# print(np.allclose(x1,x3))
