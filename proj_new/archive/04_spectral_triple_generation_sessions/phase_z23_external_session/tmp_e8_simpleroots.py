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

# Bourbaki E8 simple roots in the e-basis (with alpha8 half-integer):
# Standard realization:
#   alpha1 = e1 - e2
#   alpha2 = e2 - e3
#   alpha3 = e3 - e4
#   alpha4 = e4 - e5
#   alpha5 = e5 - e6
#   alpha6 = e6 - e7
#   alpha7 = e7 - e8
#   alpha8 = -1/2*(e1 + ... + e8) - ... let's use the standard one:
#   alpha8 = 1/2*(e1 + e8) - 1/2*(e2 + e3 + e4 + e5 + e6 + e7)?? 
# The conventional Bourbaki choice:
#   alpha8 = -1/2 * (e1 + e2 + e3 + e4 + e5 + e6 + e7) + 1/2 * e8? 
# Let's determine it by requiring the Cartan matrix to be the E8 one.
def cartan(alphas):
    n = len(alphas)
    return np.array([[2 * alphas[i] @ alphas[j] / (alphas[j] @ alphas[j]) for j in range(n)] for i in range(n)])

# Known E8 Cartan matrix (Bourbaki numbering 1..8, edges: 1-3,2-4,3-4,4-5,5-6,6-7,6-8)
C8 = np.zeros((8, 8))
for i in range(8):
    C8[i, i] = 2
for (i, j) in [(0, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7)]:
    C8[i, j] = C8[j, i] = -1
print("target E8 Cartan:\n", C8.astype(int))

# Try candidate: alpha_i = e_i - e_{i+1} for i=1..7, alpha8 = (e7 - e8 + something)?
# Standard: alpha8 = -1/2*(e1+e2+...+e7) + 1/2*e8  -> check Cartan
alphas = []
for i in range(7):
    v = np.zeros(8); v[i], v[i+1] = 1, -1
    alphas.append(v)
v = np.zeros(8)
for i in range(7):
    v[i] = -0.5
v[7] = 0.5
alphas.append(v)
alphas = np.array(alphas)
C = cartan(alphas)
print("candidate Cartan (a8 = -1/2 sum_{1..7} + 1/2 e8):\n", np.round(C, 1))
print("matches E8:", np.allclose(C, C8))
