from fractions import Fraction
from itertools import product

def e8_roots_exact():
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (-1, 1):
                for sj in (-1, 1):
                    v = [Fraction(0)] * 8
                    v[i], v[j] = Fraction(si), Fraction(sj)
                    roots.append(v)
    for signs in product([-1, 1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append([Fraction(s) / 2 for s in signs])
    return roots

R = e8_roots_exact()
Rset = {tuple(r) for r in R}

def alpha_bourbaki():
    a1 = [Fraction(0)] * 8
    a1[0], a1[7] = Fraction(1, 2), Fraction(1, 2)
    for i in range(1, 7):
        a1[i] = -Fraction(1, 2)
    a2 = [Fraction(0)] * 8
    a2[0], a2[1] = Fraction(1), Fraction(1)
    A = [a1, a2]
    for i in range(1, 7):
        v = [Fraction(0)] * 8
        v[i - 1], v[i] = -Fraction(1), Fraction(1)
        A.append(v)
    return A

A = alpha_bourbaki()

import numpy as np
A_float = np.array([[float(x) for x in row] for row in A])
A_inv = np.linalg.inv(A_float)

def to_alpha(v):  # exact e-basis vector -> alpha-basis coefficients (exact ints if integral)
    vf = np.array([float(x) for x in v])
    c = vf @ A_inv
    c_rounded = np.rint(c).astype(int)
    # verify exactly
    check = [sum(Fraction(int(c_rounded[i])) * A[i][j] for i in range(8)) for j in range(8)]
    assert all(check[j] == v[j] for j in range(8)), f"conversion failed for {v}"
    return c_rounded

def is_root_e(c):
    ev = [sum(Fraction(int(c[i])) * A[i][j] for i in range(8)) for j in range(8)]
    return tuple(ev) in Rset

# A2 pair (e-basis):
b1 = [Fraction(-1), Fraction(-1)] + [Fraction(0)] * 6
b2 = [Fraction(1), Fraction(0), Fraction(-1)] + [Fraction(0)] * 5
c1, c2 = to_alpha(b1), to_alpha(b2)
print("A2s1 (b1):", c1.tolist(), "is root:", is_root_e(c1))
print("A2s2 (b2):", c2.tolist(), "is root:", is_root_e(c2))

e6_simples = [
    [0, 0, 0, Fraction(-1), 1, 0, 0, 0],
    [0, 0, 0, 0, 0, Fraction(-1), 1, 0],
    [Fraction(-1,2), Fraction(1,2), Fraction(-1,2), Fraction(1,2), Fraction(-1,2), Fraction(1,2), Fraction(1,2), Fraction(-1,2)],
    [Fraction(-1,2), Fraction(1,2), Fraction(-1,2), Fraction(1,2), Fraction(1,2), Fraction(-1,2), Fraction(-1,2), Fraction(1,2)],
    [Fraction(1,2), Fraction(-1,2), Fraction(1,2), Fraction(-1,2), Fraction(-1,2), Fraction(1,2), Fraction(-1,2), Fraction(1,2)],
    [Fraction(1,2), Fraction(-1,2), Fraction(1,2), Fraction(1,2), Fraction(1,2), Fraction(1,2), Fraction(1,2), Fraction(-1,2)],
]
print("\nE6 simple roots in alpha-basis:")
cs = []
for s in e6_simples:
    c = to_alpha(s)
    cs.append(c)
    print("   ", c.tolist(), "is root:", is_root_e(c))
