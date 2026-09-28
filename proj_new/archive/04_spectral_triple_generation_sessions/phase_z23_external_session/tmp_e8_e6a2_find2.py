import numpy as np
from itertools import product

def e8_roots():
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (-1, 1):
                for sj in (-1, 1):
                    v = np.zeros(8)
                    v[i], v[j] = si, sj
                    roots.append(v)
    for signs in product([-1, 1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(0.5 * np.array(signs))
    return np.array(roots)

R = e8_roots()
print("E8 roots:", len(R))

# Find an A2 pair: two roots with beta1 . beta2 = -1 (and |beta|=sqrt2 each)
# which together with their orthogonal complement gives E6 x A2.
def cartan_of(roots):
    # roots: list of vectors; compute Cartan matrix
    n = len(roots)
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            C[i, j] = 2 * (roots[i] @ roots[j]) / (roots[j] @ roots[j])
    return C

found = []
for a in range(len(R)):
    for b in range(a + 1, len(R)):
        if abs(R[a] @ R[b] + 1) < 1e-9:
            # candidate A2 pair {beta_a, beta_b}; check orthogonals form E6
            orth = [r for r in R if abs(r @ R[a]) < 1e-9 and abs(r @ R[b]) < 1e-9]
            if len(orth) == 72:
                # rank check: Gram matrix of orth has rank 6
                G = np.array([[x @ y for y in orth] for x in orth])
                if np.linalg.matrix_rank(G, tol=1e-6) == 6:
                    # find 6 simple roots of the E6 subsystem
                    found.append((a, b))
                    print("candidate A2: e-basis vectors")
                    print("  beta1 =", np.round(R[a], 3))
                    print("  beta2 =", np.round(R[b], 3))
                    print("  orthogonal roots:", len(orth), "rank:", np.linalg.matrix_rank(G, tol=1e-6))
                    break
    if found:
        break

if not found:
    print("no candidate found")
