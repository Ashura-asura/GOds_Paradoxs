"""
Phase Z22, Step 3 -- psi_3 as an inner automorphism.

Cl(8) = Mat(16,C) is a simple algebra, so by Skolem-Noether EVERY
algebra automorphism is inner: there exists an invertible U8 with
psi_3(M) = U8 M U8^-1 for all M in Cl(8). Rather than symbolically
track psi_3 through every product of Witt generators (error-prone), we
SOLVE for U8 directly from its known action on the 8 Clifford
generators, then apply it to anything -- fermion states, idempotents,
whatever -- by direct conjugation. Same SVD-nullspace method this
project's own solve_charge_conjugation() already uses for J.

NOTE ON A BUG CAUGHT DURING THIS PHASE: an earlier version of this
script took nv = vh[-1,:] as the nullspace vector and got a U8 that
satisfied "M @ vec(U8) ~ 0" (small singular value) but FAILED the
direct defining equation U8@E[a] == psi3(E[a])@U8 by a large margin
(~1.7, not noise). Root cause: for numpy's complex SVD (M = u @ diag(s)
@ vh), the right null vector is the last COLUMN of V = vh.conj().T,
i.e. vh[-1,:].conj() -- not vh[-1,:]. This project's own
solve_charge_conjugation() already has this conjugate; this script
originally didn't. Caught by checking the direct equation, not just
trusting a small singular value -- the general lesson (don't trust "SVD
says it's ~0" without a direct residual check) is now applied below.
"""
import numpy as np
from gresnigt_algebra import build_cl8_generators
from gresnigt_generations import build_psi3_images

N8 = 16


def solve_psi3_inner_automorphism(E8, psi3_e8):
    """Solve U8 @ E8[a] = psi3_e8[a] @ U8 for all a=0..7, via SVD nullspace."""
    N = N8
    ncols = N * N
    M = np.zeros((8 * N * N, ncols), dtype=complex)
    for k in range(ncols):
        i, j = divmod(k, N)
        Eij = np.zeros((N, N), dtype=complex)
        Eij[i, j] = 1.0
        out = np.concatenate([(Eij @ E8[a] - psi3_e8[a] @ Eij).flatten() for a in range(8)])
        M[:, k] = out
    u, s, vh = np.linalg.svd(M)
    n_null = int(np.sum(s < 1e-8 * s[0]))
    nv = vh[-1, :].conj()  # FIX: complex conjugate, matching solve_charge_conjugation's convention
    U8 = nv.reshape(N, N)
    U8 = U8 / np.sqrt(np.trace(U8.conj().T @ U8) / N)
    return U8, s, n_null


if __name__ == "__main__":
    E8 = build_cl8_generators()
    psi3_e8 = build_psi3_images(E8)

    U8, singvals, n_null = solve_psi3_inner_automorphism(E8, psi3_e8)
    print(f"[Check] SVD nullspace dimension for psi_3's inner-automorphism unitary U8: {n_null} (expect 1)")
    print(f"[Check] smallest 5 singular values: {singvals[-5:]}")

    # Direct defining-equation check (not just the SVD residual) -- this is
    # the check that caught the conjugate bug in the first place.
    max_err = 0.0
    for a in range(8):
        lhs = U8 @ E8[a]
        rhs = psi3_e8[a] @ U8
        max_err = max(max_err, np.max(np.abs(lhs - rhs)))
    print(f"[Check] U8 @ E_a == psi_3(E_a) @ U8, direct, all 8 generators: max err = {max_err:.3e}")

    unitary_err = np.max(np.abs(U8.conj().T @ U8 - np.eye(N8)))
    print(f"[Check] U8 exactly unitary: max err = {unitary_err:.3e}")

    U8_cubed = U8 @ U8 @ U8
    ratios = np.diag(U8_cubed) / U8_cubed[0, 0]
    diag_spread = np.max(np.abs(ratios - 1.0))
    offdiag_max = np.max(np.abs(U8_cubed - np.diag(np.diag(U8_cubed))))
    print(f"[Check] U8^3 proportional to I_16 (psi_3^3 = Id): "
          f"diag-ratio spread {diag_spread:.3e}, off-diagonal magnitude {offdiag_max:.3e}")

    np.save("U8_psi3.npy", U8)
    print("[Saved] U8_psi3.npy")
