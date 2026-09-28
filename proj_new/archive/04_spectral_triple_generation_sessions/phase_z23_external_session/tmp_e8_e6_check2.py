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
b1 = np.array([-1., -1., 0, 0, 0, 0, 0, 0])
b2 = np.array([1., 0, -1., 0, 0, 0, 0, 0])

# E6 roots = those orthogonal to the A2 plane
E6 = np.array([r for r in R if abs(r @ b1) < 1e-9 and abs(r @ b2) < 1e-9])
print("E6 root count:", len(E6))

# find 6 simple roots: a positive system. Choose an ordering: pick a generic
# vector v and take roots with positive projection as positive system.
v = np.array([0.1412, 0.2314, 0.3123, 0.4311, 0.5012, 0.6113, 0.7114, 0.8121])
pos = [r for r in E6 if r @ v > 0]
print("positive roots:", len(pos))

# simple roots = positive roots that are not sums of two positive roots
def is_sum(a):
    for x in pos:
        for y in pos:
            if np.allclose(x + y, a):
                return True
    return False

simples = [a for a in pos if not is_sum(a)]
print("simple roots found:", len(simples))
for a in simples:
    print("  ", np.round(a, 3))

# Cartan matrix
n = len(simples)
C = np.array([[2 * (simples[i] @ simples[j]) / (simples[j] @ simples[j]) for j in range(n)] for i in range(n)])
print("E6 Cartan matrix (rounded):")
print(np.round(C, 1))

# standard E6 Cartan (Bourbaki numbering 1..6: edges (1,3),(2,4),(3,4),(4,5),(5,6))
C6 = np.zeros((6, 6))
for i in range(6):
    C6[i, i] = 2
for (i, j) in [(0, 2), (1, 3), (2, 3), (3, 4), (4, 5)]:
    C6[i, j] = C6[j, i] = -1
print("standard E6 Cartan:")
print(C6.astype(int))
print("matches E6:", np.allclose(C, C6))
