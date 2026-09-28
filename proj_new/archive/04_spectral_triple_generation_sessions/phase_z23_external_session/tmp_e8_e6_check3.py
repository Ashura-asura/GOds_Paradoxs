import numpy as np
from itertools import product, permutations

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
b1 = np.array([-1., -1., 0, 0, 0, 0, 0, 0])
b2 = np.array([1., 0, -1., 0, 0, 0, 0, 0])
E6 = np.array([r for r in R if abs(r @ b1) < 1e-9 and abs(r @ b2) < 1e-9])
v = np.array([0.1412, 0.2314, 0.3123, 0.4311, 0.5012, 0.6113, 0.7114, 0.8121])
pos = [r for r in E6 if r @ v > 0]

def is_sum(a):
    for x in pos:
        for y in pos:
            if np.allclose(x + y, a):
                return True
    return False

simples = np.array([a for a in pos if not is_sum(a)])
n = 6
C = np.array([[2 * (simples[i] @ simples[j]) / (simples[j] @ simples[j]) for j in range(n)] for i in range(n)])
C = np.rint(C).astype(int)
print("found Cartan (order [a,b,c,d,e,f]):\n", C)

C6 = np.zeros((6, 6), dtype=int)
for i in range(6):
    C6[i, i] = 2
for (i, j) in [(0, 2), (1, 3), (2, 3), (3, 4), (4, 5)]:
    C6[i, j] = C6[j, i] = -1
print("standard E6:\n", C6)

# search over all relabelings of the found matrix
for p in permutations(range(6)):
    perm = np.array([0,1,2,3,4,5])[list(p)]
    Cp = C[np.ix_(p, p)]
    if np.array_equal(Cp, C6):
        print("ISOMORPHIC to standard E6 via permutation", p)
        break
else:
    print("NOT isomorphic")
