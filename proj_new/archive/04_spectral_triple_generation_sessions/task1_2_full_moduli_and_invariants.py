"""
Tasks 1-2 (moduli-to-selection phase): full moduli dimension count for
Y_10 + Y_120 + Y_126 simultaneously under a single U(3) family rotation,
and checks on invariant-potential extremization.
"""
import numpy as np


def random_sym():
    A = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
    return (A + A.T) / 2


def random_antisym():
    A = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
    return (A - A.T) / 2


def basis_u3():
    basis = []
    for k in range(3):
        M = np.zeros((3, 3), dtype=complex)
        M[k, k] = 1j
        basis.append(M)
    for k in range(3):
        for l in range(k + 1, 3):
            M = np.zeros((3, 3), dtype=complex)
            M[k, l] = 1
            M[l, k] = -1
            basis.append(M)
    for k in range(3):
        for l in range(k + 1, 3):
            M = np.zeros((3, 3), dtype=complex)
            M[k, l] = 1j
            M[l, k] = 1j
            basis.append(M)
    return basis


if __name__ == "__main__":
    np.random.seed(1)

    dim_sym, dim_anti = 6, 3
    dimC_total = dim_sym + dim_anti + dim_sym
    dimR_total = 2 * dimC_total
    dimR_U3 = 9

    print(f"complex dim (Y10+Y120+Y126) = {dimC_total}, real dim = {dimR_total}")

    Y10, Y120, Y126 = random_sym(), random_antisym(), random_sym()
    B = basis_u3()

    rows = []
    for X in B:
        v = []
        for Y in (Y10, Y120, Y126):
            v.append((X.T @ Y + Y @ X).flatten())
        rows.append(np.concatenate(v))
    Mstack = np.array(rows).T
    rank = np.linalg.matrix_rank(Mstack, tol=1e-8)
    nullity = len(B) - rank
    phys_dim = dimR_total - (dimR_U3 - nullity)
    print(f"stabilizer nullity = {nullity}, physical real dim = {phys_dim}")

    # det(Y) invariance check under SU(3)_f congruence
    U = np.linalg.qr(np.random.randn(3, 3) + 1j * np.random.randn(3, 3))[0]
    U = U / (np.linalg.det(U)) ** (1 / 3)
    print("det(Y10) before/after SU(3) congruence:",
          np.round(np.linalg.det(Y10), 6),
          np.round(np.linalg.det(U.T @ Y10 @ U), 6))
