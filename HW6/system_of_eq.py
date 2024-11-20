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


if __name__ == "__main__":
    A = np.array([
    [-1,  1,  0,  0,  0],  
    [ 1, -3, 1,  0,  0],  
    [ 0,  1, -3, 1,  0],  
    [ 0,  0,  1, -3, 1],  
    [ 0,  0,  0, -1,  1]   
])
    b = np.array([-1, 0, 0, 0, 1]) # RHS

    x = GJ(A,b)

    print("Solution:")
    print(x)
    print("Check if A @ x = b")
    print(np.allclose(A @ x, b))
    print("Check if x = np.linalg.solve(A, b)")
    print(np.allclose(x, np.linalg.solve(A, b)))