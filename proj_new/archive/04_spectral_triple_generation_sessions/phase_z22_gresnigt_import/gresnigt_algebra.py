"""
Phase Z22, Step 1 — independent reproduction of Gresnigt's Cl(8)/Cl(10)
+ S3 construction (arXiv:2604.24795, building on arXiv:2601.07857).

Purpose: this project's Rule 4 (adversarial audit always on) applies to
external literature exactly as much as to this project's own phases.
The paper's Yukawa-degeneracy result was already independently checked
numerically (eigenvalues of Mbar). This file goes one level deeper:
build the ACTUAL algebra from the paper's equations (1)-(14), from
scratch, in this project's own numerical conventions, and verify the
structural claims that Z22's real question depends on:

  (a) the S3 relations (psi_3^3 = Id, eps^2 = Id, eps psi_3 = psi_3^2 eps)
  (b) that the three generation subspaces S1, S2=psi_3(S1), S3=psi_3^2(S1)
      are linearly independent
  (c) that they are NOT mutually orthogonal under the Hilbert-Schmidt
      pairing (this is the entire source of the non-trivial texture,
      and the entire reason this structure is NOT the trivial C^32 (x)
      C^3 tensor factor this project's own H_F has used since Phase Z2)

Nothing here is fitted. Every matrix is built directly from the paper's
stated formulas, eq. (1)-(41). If a claim fails to reproduce, that is
reported, not hidden.
"""
import numpy as np
from numpy import kron, eye

s1 = np.array([[0, 1], [1, 0]], dtype=complex)
s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
s3 = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def kron4(a, b, c, d):
    return kron(kron(kron(a, b), c), d)


# ---- Cl(8) generators, eq (1) ----
def build_cl8_generators():
    e1 = 1j * kron4(s1, s1, s1, s1)
    e2 = 1j * kron4(s1, s1, s3, I2)
    e3 = -1j * kron4(s1, s1, s1, s3)
    e4 = -1j * kron4(s1, s3, I2, I2)
    e5 = -1j * kron4(s1, s1, s1, s2)
    e6 = -1j * kron4(s1, s2, I2, I2)
    e7 = 1j * kron4(s1, s1, s2, I2)
    e8 = 1j * kron4(s2, I2, I2, I2)
    return [e1, e2, e3, e4, e5, e6, e7, e8]


def check_clifford_algebra(E, tol=1e-9):
    """{e_i,e_j} = 2 delta_ij * I (Euclidean Clifford, since e_i^2 should be -I per e_i = i*(real orthogonal tensor)... check directly)."""
    n = len(E)
    N = E[0].shape[0]
    Iden = np.eye(N, dtype=complex)
    max_err = 0.0
    for i in range(n):
        for j in range(n):
            anticomm = E[i] @ E[j] + E[j] @ E[i]
            target = 2 * Iden if i == j else np.zeros((N, N), dtype=complex)
            # sign convention: check against +2*delta and -2*delta, report whichever matches
            err_plus = np.max(np.abs(anticomm - target))
            max_err = max(max_err, err_plus if i == j else min(err_plus, np.max(np.abs(anticomm + target))))
    return max_err


def build_omega8(E):
    w = E[0]
    for k in range(1, 8):
        w = w @ E[k]
    return w


def build_witt(E):
    """a_j, a_j^dagger, j=1..4, eq (2)."""
    a = []
    ad = []
    for j in range(4):
        aj = 0.5 * (-E[j] + 1j * E[j + 4])
        adj = 0.5 * (E[j] + 1j * E[j + 4])
        a.append(aj)
        ad.append(adj)
    return a, ad


def check_car(a, ad, tol=1e-9):
    """{a_i,a_j}=0, {ad_i,ad_j}=0, {a_i,ad_j}=delta_ij, eq (3)."""
    n = len(a)
    N = a[0].shape[0]
    max_err = 0.0
    for i in range(n):
        for j in range(n):
            e1 = np.max(np.abs(a[i] @ a[j] + a[j] @ a[i]))
            e2 = np.max(np.abs(ad[i] @ ad[j] + ad[j] @ ad[i]))
            target = np.eye(N, dtype=complex) if i == j else np.zeros((N, N), dtype=complex)
            e3 = np.max(np.abs(a[i] @ ad[j] + ad[j] @ a[i] - target))
            max_err = max(max_err, e1, e2, e3)
    return max_err


if __name__ == "__main__":
    E8 = build_cl8_generators()
    print("[Check] Cl(8) generators built:", len(E8), "matrices of shape", E8[0].shape)
    err = check_clifford_algebra(E8)
    print(f"[Check] Clifford anticommutation relation max error: {err:.3e}")

    a, ad = build_witt(E8)
    err_car = check_car(a, ad)
    print(f"[Check] Witt basis CAR relations max error: {err_car:.3e}")

    w8 = build_omega8(E8)
    print(f"[Check] omega_8 built, is it +-I (pseudoscalar)? max|w8^2 - I| = "
          f"{np.max(np.abs(w8 @ w8 - np.eye(16))):.3e}, "
          f"max|w8^2 + I| = {np.max(np.abs(w8 @ w8 + np.eye(16))):.3e}")
