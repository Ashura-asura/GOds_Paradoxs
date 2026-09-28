"""
Phase Z5 (this session) -- Reproducible script for RESULT_phase_z5.md.

Checks, in order:
1. Whether C_mat @ G[a] has any component connecting the Gamma_F=+1 and
   Gamma_F=-1 eigenspaces (it should not, if the earlier Z4 finding is
   structural rather than an embedding artifact).
2. Why: whether C_mat itself commutes or anticommutes with Gamma_F.
3. Whether C_mat is the unique SO(10)-covariant charge-conjugation
   intertwiner, and whether it coincides with the repo's own
   C_plus/C_minus candidates (support/cl10_gamma_J.py).
4. Whether the same chirality-preserving mechanism holds for M120
   (3-gamma antisymmetrized) and M126 (5-gamma self-dual), not just M10.

Reuses gamma_i.npy (session_new_files/) and the exact C_mat construction
from vertex_terms_resolved/build_and_test.py -- no new conventions.
"""
import os
import numpy as np
from itertools import combinations, permutations
import math

N = 32


def load_gammas():
    return [np.load(os.path.join(os.path.dirname(__file__), f'gamma_{i}.npy'))
            for i in range(10)]


def build_C_mat(G):
    I32 = np.eye(N, dtype=complex)
    A_stack = []
    for a in range(10):
        A = np.kron(G[a].T, I32) + np.kron(I32, G[a].T)
        A_stack.append(A)
    A_stack = np.vstack(A_stack)
    U, s, Vh = np.linalg.svd(A_stack, full_matrices=False)
    C_mat = Vh[-1].reshape(32, 32)
    C_mat = C_mat / np.max(np.abs(C_mat))
    return C_mat, s


def gamma_prod(G, indices):
    k = len(indices)
    I32 = np.eye(N, dtype=complex)
    if k == 0:
        return I32
    result = np.zeros((N, N), dtype=complex)
    idx_list = list(indices)
    for perm in permutations(idx_list):
        sign = 1
        for i in range(k):
            for j in range(i + 1, k):
                if idx_list.index(perm[i]) > idx_list.index(perm[j]):
                    sign *= -1
        prod = I32
        for ii in perm:
            prod = prod @ G[ii]
        result = result + sign * prod
    return result / math.factorial(k)


def run():
    G = load_gammas()
    Gamma_F = (1j ** 5) * G[0] @ G[1] @ G[2] @ G[3] @ G[4] @ G[5] @ G[6] @ G[7] @ G[8] @ G[9]
    w, v = np.linalg.eigh(Gamma_F)
    V = v[:, w.real > 0]   # +1 eigenspace
    Wc = v[:, w.real < 0]  # -1 eigenspace

    C_mat, s = build_C_mat(G)
    print('A_stack smallest singular values (nullity check):', s[-3:])

    CG0 = C_mat @ G[0]
    VV = V.conj().T @ CG0 @ V
    VW = V.conj().T @ CG0 @ Wc
    WV = Wc.conj().T @ CG0 @ V
    WW = Wc.conj().T @ CG0 @ Wc
    print('\n[M10 check] norm VV:', np.linalg.norm(VV), ' VW:', np.linalg.norm(VW),
          ' WV:', np.linalg.norm(WV), ' WW:', np.linalg.norm(WW))

    comm = Gamma_F @ C_mat - C_mat @ Gamma_F
    anti = Gamma_F @ C_mat + C_mat @ Gamma_F
    print('\n||[Gamma_F, C_mat]||:', np.linalg.norm(comm))
    print('||{Gamma_F, C_mat}||:', np.linalg.norm(anti))

    idx3 = list(combinations(range(10), 3))
    max_off_120, max_diag_120 = 0, 0
    for t in idx3[:20]:
        g3 = gamma_prod(G, t)
        CG = C_mat @ g3
        max_diag_120 = max(max_diag_120, np.linalg.norm(V.conj().T @ CG @ V))
        max_off_120 = max(max_off_120, np.linalg.norm(Wc.conj().T @ CG @ V))
    print('\n[M120 sample] max diag block:', max_diag_120, ' max off-diag block:', max_off_120)

    n, k = 10, 5
    forms5 = list(combinations(range(n), k))
    n5 = len(forms5)

    def eps_sign(tup):
        if len(set(tup)) != n:
            return 0
        parity = 1
        for i in range(n):
            for j in range(i + 1, n):
                if tup[i] > tup[j]:
                    parity *= -1
        return parity

    Hodge = np.zeros((n5, n5))
    for i, fi in enumerate(forms5):
        for j, fj in enumerate(forms5):
            val = eps_sign(tuple(fj) + tuple(fi))
            if val != 0:
                Hodge[i, j] = float(val)
    P_sd = (np.eye(n5) - 1j * Hodge) / 2
    gamma5_list = [gamma_prod(G, t) for t in forms5]
    Usvd, ssvd, Vhsvd = np.linalg.svd(P_sd)
    onb = Usvd[:, :5]
    max_off_126, max_diag_126 = 0, 0
    for jj in range(5):
        g5 = sum(onb[kk, jj] * gamma5_list[kk] for kk in range(n5))
        CG = C_mat @ g5
        max_diag_126 = max(max_diag_126, np.linalg.norm(V.conj().T @ CG @ V))
        max_off_126 = max(max_off_126, np.linalg.norm(Wc.conj().T @ CG @ V))
    print('\n[M126 sample] max diag block:', max_diag_126, ' max off-diag block:', max_off_126)


if __name__ == '__main__':
    run()
