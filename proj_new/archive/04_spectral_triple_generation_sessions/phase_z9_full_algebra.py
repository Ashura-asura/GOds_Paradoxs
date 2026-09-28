"""
Phase Z9 (this session) -- Reproducible script for RESULT_phase_z9.md.

Extends Z8 from one su(3)_F generator pair to the full 8x8=64-pair
algebra, accumulating the order-one constraint as a real 18x18 Gram
matrix (to avoid the memory blow-up of a naive stacked-SVD over all
64 pairs at once) and reading off the joint kernel.
"""
import os
import sys
import numpy as np
from numpy import kron

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from z2_hilbert_space import order_one_commutator, build_su3f_generators  # noqa: E402

N = 32
I16 = np.eye(16, dtype=complex)
P = np.block([[np.zeros((16, 16)), I16], [I16, np.zeros((16, 16))]])


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
    return C_mat / np.max(np.abs(C_mat))


def embed_doubled(Y):
    return np.block([[np.zeros((16, 16)), Y], [Y.conj().T, np.zeros((16, 16))]])


def make_JbJ_general(U0, beta, B_gen):
    beta_prime = U0 @ beta.conjugate() @ np.linalg.inv(U0)
    return kron(beta_prime, B_gen.conjugate())


def E_gen(i, j):
    e = np.zeros((3, 3), dtype=complex)
    e[i, j] = 1.0
    return e


BASIS_IDX = [(i, j) for i in range(3) for j in range(3)]


def realify(Cmat):
    re = np.real(Cmat)
    im = np.imag(Cmat)
    return np.vstack([np.hstack([re, -im]), np.hstack([im, re])])


def herm_constraint_real():
    rows = []
    for a in range(3):
        for b in range(3):
            idx_ab = BASIS_IDX.index((a, b))
            idx_ba = BASIS_IDX.index((b, a))
            r1 = np.zeros(9)
            r1[idx_ab] += 1
            r1[idx_ba] -= 1
            rows.append(np.concatenate([r1, np.zeros(9)]))
            r2 = np.zeros(9)
            r2[idx_ab] += 1
            r2[idx_ba] += 1
            rows.append(np.concatenate([np.zeros(9), r2]))
    return np.array(rows)


def sym_constraint_real(sign=1):
    # sign=+1 -> symmetric (M10, M126); sign=-1 -> antisymmetric (M120)
    rows = []
    for a in range(3):
        for b in range(3):
            idx_ab = BASIS_IDX.index((a, b))
            idx_ba = BASIS_IDX.index((b, a))
            r1 = np.zeros(9)
            r1[idx_ab] += 1
            r1[idx_ba] -= sign
            rows.append(np.concatenate([r1, np.zeros(9)]))
            r2 = np.zeros(9)
            r2[idx_ab] += 1
            r2[idx_ba] -= sign
            rows.append(np.concatenate([np.zeros(9), r2]))
    return np.array(rows)


def gamma_prod(G, indices):
    from itertools import permutations
    import math
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


def run_channel(name, Y_H, sym_sign, A32_cache, su3f, Herm_real):
    A32 = embed_doubled(Y_H)
    Constraint_real = sym_constraint_real(sym_sign)
    GtG = Herm_real.T @ Herm_real + Constraint_real.T @ Constraint_real
    for i in range(8):
        for j in range(8):
            a_HF = kron(np.eye(32, dtype=complex), su3f[i])
            Jb_HF = make_JbJ_general(P, np.eye(32, dtype=complex), su3f[j])
            imgs = []
            for (p, q) in BASIS_IDX:
                D_F_pq = kron(A32, E_gen(p, q))
                Lpq = order_one_commutator(D_F_pq, a_HF, Jb_HF)
                imgs.append(Lpq.flatten())
            L = np.array(imgs).T
            Lr = realify(L)
            GtG += Lr.T @ Lr
    rank = np.linalg.matrix_rank(GtG, tol=1e-6)
    w_eig, v_eig = np.linalg.eigh(GtG)
    print(f'--- {name} ---')
    print('surviving real dim:', 18 - rank)
    print('smallest eigenvalues:', np.round(w_eig[:6], 6))
    null_basis = v_eig[:, w_eig < 1e-6 * max(w_eig)]
    for kk in range(null_basis.shape[1]):
        vec = null_basis[:, kk]
        print('Re:')
        print(np.round(vec[:9].reshape(3, 3), 3))


def run():
    G = load_gammas()
    Gamma_F = (1j ** 5) * G[0] @ G[1] @ G[2] @ G[3] @ G[4] @ G[5] @ G[6] @ G[7] @ G[8] @ G[9]
    w, v = np.linalg.eigh(Gamma_F)
    V = v[:, w.real > 0]
    C_mat = build_C_mat(G)
    su3f = build_su3f_generators()
    Herm_real = herm_constraint_real()

    Y10 = V.conj().T @ (C_mat @ G[0]) @ V
    run_channel('M10 (symmetric)', Y10, 1, None, su3f, Herm_real)

    Y120 = V.conj().T @ (C_mat @ gamma_prod(G, (0, 1, 2))) @ V
    run_channel('M120 (antisymmetric)', Y120, -1, None, su3f, Herm_real)

    from itertools import combinations
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
    Y126 = (V.conj().T @ (C_mat @ sum(Usvd[kk, 0] * gamma5_list[kk] for kk in range(n5))) @ V) / np.sqrt(2)
    run_channel('M126 (symmetric, complex)', Y126, 1, None, su3f, Herm_real)


if __name__ == '__main__':
    run()
