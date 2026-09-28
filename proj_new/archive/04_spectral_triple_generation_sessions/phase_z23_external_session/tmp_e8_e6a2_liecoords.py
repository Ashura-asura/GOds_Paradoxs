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

# Bourbaki E8 simple roots in e-basis:
#   alpha1 = e1-e2, ..., alpha7 = e7-e8, alpha8 = 1/2(e1+e8) - 1/2(e2+...+e7)?
# The standard Bourbaki: alpha8 = 1/2*(e1 + e8 - e2 - e3 - e4 - e5 - e6 - e7)
alphas = []
for i in range(7):
    v = np.zeros(8); v[i], v[i + 1] = 1, -1
    alphas.append(v)
v = np.zeros(8)
v[0] = 0.5; v[7] = 0.5
for i in range(1, 7):
    v[i] = -0.5
alphas.append(v)
A = np.array(alphas)  # rows = alpha_i in e-basis
print("Bourbaki alpha8 =", v)
# verify Cartan is E8 (Bourbaki numbering: edges 1-3, 2-4, 3-4, 4-5, 5-6, 6-7, 7-8)
C = np.array([[2 * A[i] @ A[j] / (A[j] @ A[j]) for j in range(8)] for i in range(8)])
print("Cartan from Bourbaki realization:")
print(np.round(C, 1).astype(int))

# The A2 pair found by brute force:
b1 = np.array([-1., -1., 0, 0, 0, 0, 0, 0])
b2 = np.array([1., 0, -1., 0, 0, 0, 0, 0])
# express b1, b2 in alpha-basis: e-coords x = sum c_i alpha_i  =>  c = x @ inv(A)
c1 = b1 @ np.linalg.inv(A)
c2 = b2 @ np.linalg.inv(A)
print("\nb1 = -alpha2?", np.allclose(c1, [0, -1, 0, 0, 0, 0, 0, 0]))
print("b2 = -alpha3-alpha4?", np.allclose(c2, [0, 0, -1, -1, 0, 0, 0, 0]))

# E6 roots = orthogonal to A2 plane
E6 = np.array([r for r in R if abs(r @ b1) < 1e-9 and abs(r @ b2) < 1e-9])
print("\nE6 root count:", len(E6))

# find simple roots of E6 (as before, with the same generic vector)
vgen = np.array([0.1412, 0.2314, 0.3123, 0.4311, 0.5012, 0.6113, 0.7114, 0.8121])
pos = [r for r in E6 if r @ vgen > 0]

def is_sum(a):
    for x in pos:
        for y in pos:
            if np.allclose(x + y, a):
                return True
    return False

simples = [a for a in pos if not is_sum(a)]
print("E6 simple roots:", len(simples))
print("\nE6 simple roots expressed in E8 alpha-basis (LiE coordinates):")
for s in simples:
    cs = np.round(s @ np.linalg.inv(A), 6)
    print("  ", cs.astype(int).tolist() if np.allclose(cs, np.round(cs)) else cs)
