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

# A2 pair found earlier
b1 = np.array([-1., -1., 0, 0, 0, 0, 0, 0])
b2 = np.array([1., 0, -1., 0, 0, 0, 0, 0])

# orthonormal basis of the A2 plane (in R^8):
u1 = b1 / np.linalg.norm(b1)
u2 = b2 - (b2 @ u1) * u1
u2 = u2 / np.linalg.norm(u2)
P = np.outer(u1, u1) + np.outer(u2, u2)   # projector onto A2 plane

norms = {}
for x in R:
    xA2 = P @ x
    k = round(xA2 @ xA2, 6)
    norms[k] = norms.get(k, 0) + 1

print("distribution of |A2-projection|^2 over the 240 E8 roots:")
for k in sorted(norms):
    print(f"  |xA2|^2 = {k}: {norms[k]} roots")

print()
print("Expected: 72 at 0 (E6 roots), 6 at 2 (A2 roots, length^2=2),")
print("162 at 2/3 = 0.666667 (weights of 27x3 + 27barx3bar, A2 weight length^2 = 2/3)")
# A2 fundamental weight length^2: for roots of length^2 = 2, fundamental weight
# has |w|^2 = 2/3 * ... check: w1 = (2u1 - u2)/sqrt... compute directly:
w_check = np.round(np.array([2. / 3]), 3)
total = sum(norms.values())
print("total:", total)
