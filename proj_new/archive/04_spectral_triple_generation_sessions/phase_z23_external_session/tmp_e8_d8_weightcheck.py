import numpy as np
from itertools import product

# E8 root system in R^8: {+-e_i +- e_j} (112) + {1/2(+-1,...) even sign count} (128)
def e8_roots():
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (-1, 1):
                for sj in (-1, 1):
                    v = np.zeros(8)
                    v[i], v[j] = si, sj
                    roots.append(v)
    # half-integer roots: even number of minus signs (or even number of plus signs)
    for signs in product([-1, 1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(0.5 * np.array(signs))
    return np.array(roots)

R = e8_roots()
print("total E8 roots:", len(R))

# D8 roots: the {+-e_i +- e_j} subset
d8_mask = np.array([np.count_nonzero(r) > 0 and all(abs(x) == 1 or x == 0 for x in r) for r in R])
d8_roots = R[d8_mask]
print("D8 roots inside E8:", len(d8_roots))

# D8 simple roots: e1-e2, e2-e3, ..., e7-e8, e7+e8
d8_simple = []
for i in range(7):
    v = np.zeros(8); v[i], v[i+1] = 1, -1
    d8_simple.append(v)
v = np.zeros(8); v[6], v[7] = 1, 1
d8_simple.append(v)
d8_simple = np.array(d8_simple)

# weight lattice map: express each E8 weight in D8 fundamental-weight coords
# D8 fundamental weights (omega_i): for i<7: (1,...,1,0,...,0) - ... use Weyl:
# omega_i = e1+...+e_i for i<=6; omega7 = (e1+...+e7 - e8)/2; omega8 = (e1+...+e8)/2
def d8_fund_wts():
    w = []
    for i in range(1, 7):
        v = np.zeros(8); v[:i] = 1
        w.append(v)
    v = np.ones(8); v[7] = -1
    w.append(v / 2)
    v = np.ones(8)
    w.append(v / 2)
    return np.array(w)

F = d8_fund_wts()
# inverse: express vector x in basis F (over Q)
Finv = np.linalg.inv(F)

def to_d8_coords(x):
    return Finv @ x

# check the 112 D8 roots are roots of the D8 system with correct Cartan matrix
C = np.array([[2*(d8_simple[i] @ d8_simple[j]) for j in range(8)] for i in range(8)])
print("D8 Cartan matrix:\n", C)

# Now the branching: E8 248 = adjoint. Weights of adjoint = 240 roots + 8 zeros.
# Restrict each weight to D8 coordinates, then decompose into D8 irreps by
# Weyl character / weight multiplicity counting is heavy; instead use the
# known decomposition structure: count how many weights land on D8 roots vs not.
d8_weights = set()
for r in R:
    c = np.round(to_d8_coords(r), 10)
    d8_weights.add(tuple(c))

# the 112 D8 roots in D8 coords:
d8_root_coords = set()
for r in d8_roots:
    d8_root_coords.add(tuple(np.round(to_d8_coords(r), 10)))

on_roots = sum(1 for w in d8_weights if w in d8_root_coords or tuple(-np.array(w)) in d8_root_coords)
print("distinct restricted weights:", len(d8_weights))
print("weights landing on D8 roots:", on_roots)
print("weights NOT on D8 roots:", len(d8_weights) - on_roots)
# 120 = 112 roots + 8 Cartan (zeros). zeros count as 1 distinct weight.
# So expect: 112 on-roots + 8 zero-restrictions = 120, and 128 spinor weights.
zero_wts = sum(1 for w in d8_weights if np.allclose(w, 0, atol=1e-9))
print("weights restricting to 0 (Cartan of D8):", zero_wts)
