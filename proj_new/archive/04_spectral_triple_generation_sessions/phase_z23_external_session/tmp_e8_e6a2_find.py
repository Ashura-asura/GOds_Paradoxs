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

# E8 simple roots in this basis (standard Bourbaki-like ordering):
# alpha1 = e1-e2, alpha2 = e2-e3, alpha3 = e3-e4, alpha4 = e4-e5,
# alpha5 = e5-e6, alpha6 = e6-e7, alpha7 = e7-e8, alpha8 = 1/2(e1+..+e8) - 1/2 sum? 
# Use: alpha_i = e_i - e_{i+1} for i=1..7; alpha8 = -1/2(e1+..+e8) (the E8 simple roots in
# this realization are alpha1..alpha7 = e_i-e_{i+1} and alpha8 = -1/2 sum of all e_i
# such that the last root has coefficient 2: theta = e7+e8? no.)
# Correct standard realization (e-basis, E8):
#   alpha1..alpha7 = e_i - e_{i+1}
#   alpha8 = -1/2*(e1+...+e7) + 1/2*e8   ... this is one choice. Let's verify Cartan matrix.
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

def cartan(simple):
    n = len(simple)
    return np.array([[2 * (simple[i] @ simple[j]) / (simple[j] @ simple[j])
                      for j in range(n)] for i in range(n)])

C = cartan(alphas)
print("E8 Cartan matrix check:\n", np.round(C, 1))

# E6 = nodes 1..6 (LiE diagram: 1-3-4-5-6-7-8 chain with 2 attached to 3 means
# in our numbering 1..7 chain plus 2 attached to 3... need E6 to match LiE's.
# LiE E8 diagram: chain 1-3-4-5-6-7-8, node 2 attached to node 3.
# So E6 = nodes {1,2,3,4,5,6} of LiE = our nodes {1,2,3,4,5,6} similarly.
# Find A2 roots orthogonal to alpha1..alpha6:
e6_nodes = [0, 1, 2, 3, 4, 5]
orth = []
for r in R:
    if all(abs(r @ alphas[i]) < 1e-9 for i in e6_nodes):
        orth.append(r)
print("roots orthogonal to E6 nodes:", len(orth))
for r in orth:
    print(" ", np.round(r, 3))
