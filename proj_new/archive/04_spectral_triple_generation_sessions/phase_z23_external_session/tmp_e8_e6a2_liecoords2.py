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

# Correct Bourbaki E8 simple roots:
#   alpha1 = 1/2(e1 + e8 - e2 - e3 - e4 - e5 - e6 - e7)
#   alpha2 = e1 + e2
#   alpha3 = e2 - e1
#   alpha4 = e3 - e2
#   alpha5 = e4 - e3
#   alpha6 = e5 - e4
#   alpha7 = e6 - e5
#   alpha8 = e7 - e6
alphas = []
v = np.zeros(8); v[0], v[7] = 0.5, 0.5
for i in range(1, 7):
    v[i] = -0.5
alphas.append(v.copy())
alphas.append(np.array([1., 1., 0, 0, 0, 0, 0, 0]))
for i in range(1, 7):
    v = np.zeros(8); v[i - 1], v[i] = -1, 1
    alphas.append(v)
A = np.array(alphas)
# alpha1 . alpha3 check: (1/2)(e1+e8-e2-...-e7).(e2-e1) = 1/2[(-1) - (-1)] hmm
# verify each alpha is a root and pairings
print("alpha norms^2:", [round(a @ a, 4) for a in A])
# inner products alpha1 . alpha3 and alpha1 . alpha4:
print("a1.a3 =", round(A[0] @ A[2], 4), " a1.a4 =", round(A[0] @ A[3], 4))
C = np.array([[2 * A[i] @ A[j] / (A[j] @ A[j]) for j in range(8)] for i in range(8)])
C = np.rint(C).astype(int)
print("Cartan (Bourbaki numbering):")
print(C)
expected = np.zeros((8, 8), dtype=int)
for i in range(8):
    expected[i, i] = 2
for (i, j) in [(0, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]:
    expected[i, j] = expected[j, i] = -1
print("expected (fork at node 4):\n", expected)
print("correct:", np.array_equal(C, expected))


# LiE numbering: chain 1-3-4-5-6-7-8, node 2 attached to 3.
# Bourbaki:    chain 1-3-4-5-6-7-8, node 2 attached to 4.
# So LiE node k maps to Bourbaki node: LiE(3)->Bour(4), LiE(4)->Bour(5), ...,
# LiE(8)->Bour(3).  liE2Bour = [1,2,4,5,6,7,8,3]
liE2Bour = [1, 2, 4, 5, 6, 7, 8, 3]  # 0-indexed: [0,1,3,4,5,6,7,2]

# The A2 pair from brute force (e-basis):
b1 = np.array([-1., -1., 0, 0, 0, 0, 0, 0])
b2 = np.array([1., 0, -1., 0, 0, 0, 0, 0])
M = np.linalg.inv(A)  # e-coord -> Bourbaki-coord
c1 = b1 @ M
c2 = b2 @ M
print("\nb1 in Bourbaki coords:", np.round(c1, 6))
print("b2 in Bourbaki coords:", np.round(c2, 6))
# in LiE coords: reorder (LiE node i -> Bourbaki liE2Bour[i])
def to_lie(c):
    return [c[liE2Bour[i] - 1] for i in range(8)]
print("b1 in LiE coords:", to_lie(np.round(c1, 6)))
print("b2 in LiE coords:", to_lie(np.round(c2, 6)))

# E6 simple roots from tmp_e8_e6_check2 in e-basis, convert to LiE coords
e6_simples = [
    [0, 0, 0, -1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, -1, 1, 0],
    [-0.5, 0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5],
    [-0.5, 0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5],
    [0.5, -0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5],
    [0.5, -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -0.5],
]
print("\nE6 simple roots in LiE coords:")
for s in e6_simples:
    cb = np.array(s) @ M
    print("   ", to_lie(np.round(cb, 6)))
