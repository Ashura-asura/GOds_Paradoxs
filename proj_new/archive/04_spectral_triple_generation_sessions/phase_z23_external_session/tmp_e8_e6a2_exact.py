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
print("E8 roots:", len(R))

# Bourbaki simple roots in e-basis (exact):
def alpha_bourbaki():
    # alpha1 = 1/2(e1 + e8 - e2 - ... - e7)
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

def matvec(m, v):  # v in e-basis -> coefficients in alpha-basis (alpha rows of m)
    # solve  sum_j c_j * alpha_j = v   by inverting m (exact Gaussian elimination)
    import copy
    n = len(m)
    M = [row[:] + [v[i]] for i, row in enumerate(m)]
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]

# A2 pair (e-basis):
b1 = [Fraction(-1), Fraction(-1)] + [Fraction(0)] * 6
b2 = [Fraction(1)] + [Fraction(0)] * 6 + [Fraction(-1)]

def is_root(c, Rset):
    # check c (alpha-basis coeffs) represents one of the 240 roots:
    # reconstruct e-vector and check in R set
    ev = [sum(c[i] * A[i][j] for i in range(8)) for j in range(8)]
    return any(all(ev[k] == r[k] for k in range(8)) for r in R)

c1 = matvec(A, b1)
c2 = matvec(A, b2)
print("b1 coeffs:", c1, "is root:", is_root(c1, R))
print("b2 coeffs:", c2, "is root:", is_root(c2, R))

# E6 simple roots from the earlier search (e-basis), exact:
e6_simples = [
    [0, 0, 0, Fraction(-1), 1, 0, 0, 0],
    [0, 0, 0, 0, 0, Fraction(-1), 1, 0],
    [Fraction(-1,2), Fraction(1,2), Fraction(-1,2), Fraction(1,2), Fraction(-1,2), Fraction(1,2), Fraction(1,2), Fraction(-1,2)],
    [Fraction(-1,2), Fraction(1,2), Fraction(-1,2), Fraction(1,2), Fraction(1,2), Fraction(-1,2), Fraction(-1,2), Fraction(1,2)],
    [Fraction(1,2), Fraction(-1,2), Fraction(1,2), Fraction(-1,2), Fraction(-1,2), Fraction(1,2), Fraction(-1,2), Fraction(1,2)],
    [Fraction(1,2), Fraction(-1,2), Fraction(1,2), Fraction(1,2), Fraction(1,2), Fraction(1,2), Fraction(1,2), Fraction(-1,2)],
]
print("\nE6 simple roots (alpha-basis), verifying each is an E8 root:")
for s in e6_simples:
    cs = matvec(A, s)
    print("   ", [int(x) for x in cs] if all(x.denominator == 1 for x in cs) else cs, "is root:", is_root(cs, R))

print("\nAll 8 roots for closure:")
print("E6s1:", [int(x) for x in matvec(A, e6_simples[0])])
print("E6s2:", [int(x) for x in matvec(A, e6_simples[1])])
print("E6s3:", [int(x) for x in matvec(A, e6_simples[2])])
print("E6s4:", [int(x) for x in matvec(A, e6_simples[3])])
print("E6s5:", [int(x) for x in matvec(A, e6_simples[4])])
print("E6s6:", [int(x) for x in matvec(A, e6_simples[5])])
print("A2s1:", [int(x) for x in c1])
print("A2s2:", [int(x) for x in c2])
