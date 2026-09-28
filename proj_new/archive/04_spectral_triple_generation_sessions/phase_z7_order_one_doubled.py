"""
Phase Z7 (this session) -- Reproducible script for RESULT_phase_z7.md.

Re-runs Z3's Test A (pure family-gauge action) using Z6's validated
doubled D_F blocks (built from actual M10[0] and an M120 triple)
instead of Z3's generic random matrices, and additionally checks
whether the induced commutator itself still respects the grading.
"""
import os
import sys
import numpy as np
from numpy import kron
from itertools import permutations
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from z2_hilbert_space import N_GEN, E_kl, order_one_commutator, build_su3f_generators  # noqa: E402

N = 32
I16 = np.eye(16, dtype=complex)
P = np.block([[np.zeros((16, 16)), I16], [I16, np.zeros((16, 16))]])
EPS32 = np.block([[I16, np.zeros((16, 16))], [np.zeros((16, 16)), -I16]])


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


def embed_doubled(Y):
    return np.block([[np.zeros((16, 16)), Y], [Y.conj().T, np.zeros((16, 16))]])


def make_JbJ_general(U0, beta, B_gen):
    beta_prime = U0 @ beta.conjugate() @ np.linalg.inv(U0)
    return kron(beta_prime, B_gen.conjugate())


def block_norms(op96):
    norms = np.zeros((N_GEN, N_GEN))
    for k in range(N_GEN):
        for l in range(N_GEN):
            block = op96[k * 32:(k + 1) * 32, l * 32:(l + 1) * 32]
            norms[k, l] = np.linalg.norm(block)
    return norms


def run():
    G = load_gammas()
    Gamma_F = (1j ** 5) * G[0] @ G[1] @ G[2] @ G[3] @ G[4] @ G[5] @ G[6] @ G[7] @ G[8] @ G[9]
    w, v = np.linalg.eigh(Gamma_F)
    V = v[:, w.real > 0]
    C_mat = build_C_mat(G)

    Y10 = V.conj().T @ (C_mat @ G[0]) @ V
    Y120 = V.conj().T @ (C_mat @ gamma_prod(G, (0, 1, 2))) @ V

    D32_1 = embed_doubled(Y10)
    D32_2 = embed_doubled(Y120)
    D_F_two = kron(D32_1, E_kl(0, 1)) + kron(D32_2, E_kl(1, 2))

    su3f = build_su3f_generators()
    T_fam_a = su3f[0]
    T_fam_b = su3f[2]

    alpha_A = np.eye(32, dtype=complex)
    beta_A = np.eye(32, dtype=complex)
    a_HF_A = kron(alpha_A, T_fam_a)
    Jb_HF_A = make_JbJ_general(P, beta_A, T_fam_b)

    full_A = order_one_commutator(D_F_two, a_HF_A, Jb_HF_A)

    print('=== Z7 Test A: pure family-gauge action, physical D_F (M10[0], M120 triple) ===')
    print('Block-norm matrix of [[D_F,a],J0bJ0^-1] (generation indices k,l):')
    print(np.round(block_norms(full_A), 4))

    eps96 = kron(EPS32, np.eye(N_GEN, dtype=complex))
    anti96 = eps96 @ full_A + full_A @ eps96
    print()
    print('||{eps96, full_A}|| (0 => result stays chirality-flipping):', np.linalg.norm(anti96))
    print('||full_A|| overall:', np.linalg.norm(full_A))

    # --- Addendum: Hermiticity check (D_F_two as built above is NOT Hermitian --
    # inherited unmodified from Z2/Z3's own skeleton, which never added the
    # generation-conjugate partners E(1,0), E(2,1)) ---
    print()
    print('--- Addendum: Hermiticity check ---')
    print('||D_F_two - D_F_two^dagger|| (expect nonzero, inherited bug):',
          np.linalg.norm(D_F_two - D_F_two.conj().T))
    print('||full_A - full_A^dagger|| (expect nonzero):',
          np.linalg.norm(full_A - full_A.conj().T))

    D_F_herm = (kron(D32_1, E_kl(0, 1)) + kron(D32_1.conj().T, E_kl(1, 0))
                + kron(D32_2, E_kl(1, 2)) + kron(D32_2.conj().T, E_kl(2, 1)))
    full_A_herm = order_one_commutator(D_F_herm, a_HF_A, Jb_HF_A)
    print()
    print('Fixed (Hermitian) D_F_herm:')
    print('||D_F_herm - D_F_herm^dagger|| (expect 0):',
          np.linalg.norm(D_F_herm - D_F_herm.conj().T))
    print('||full_A_herm - full_A_herm^dagger|| (expect 0):',
          np.linalg.norm(full_A_herm - full_A_herm.conj().T))
    anti96_herm = eps96 @ full_A_herm + full_A_herm @ eps96
    print('||{eps96, full_A_herm}|| (grading, expect 0):', np.linalg.norm(anti96_herm))
    print('Block-norm matrix (Hermitian D_F):')
    print(np.round(block_norms(full_A_herm), 4))


if __name__ == '__main__':
    run()
