"""
Phase Z8 (this session) -- Reproducible script for RESULT_phase_z8.md.

Treats the generation-space Yukawa matrix Y_gen (3x3 complex) as the
unknown, and linearizes the order-one condition in Y_gen to find
exactly how many parameters survive, cross-checked two independent
ways (complex kernel via SVD, and a from-scratch real-coordinate
version with explicit Hermitian/Symmetric constraints).
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
    top = np.hstack([re, -im])
    bot = np.hstack([im, re])
    return np.vstack([top, bot])


def herm_constraint_real():
    rows = []
    for a in range(3):
        for b in range(3):
            idx_ab = BASIS_IDX.index((a, b))
            idx_ba = BASIS_IDX.index((b, a))
            row_re9 = np.zeros(9)
            row_re9[idx_ab] += 1
            row_re9[idx_ba] -= 1
            rows.append(np.concatenate([row_re9, np.zeros(9)]))
            row_im9 = np.zeros(9)
            row_im9[idx_ab] += 1
            row_im9[idx_ba] += 1
            rows.append(np.concatenate([np.zeros(9), row_im9]))
    return np.array(rows)


def sym_constraint_real():
    rows = []
    for a in range(3):
        for b in range(3):
            idx_ab = BASIS_IDX.index((a, b))
            idx_ba = BASIS_IDX.index((b, a))
            row_re9 = np.zeros(9)
            row_re9[idx_ab] += 1
            row_re9[idx_ba] -= 1
            rows.append(np.concatenate([row_re9, np.zeros(9)]))
            row_im9 = np.zeros(9)
            row_im9[idx_ab] += 1
            row_im9[idx_ba] -= 1
            rows.append(np.concatenate([np.zeros(9), row_im9]))
    return np.array(rows)


def real_dim(Amat):
    if Amat.shape[0] == 0:
        return 18
    rank = np.linalg.matrix_rank(Amat, tol=1e-8)
    return 18 - rank


def run():
    G = load_gammas()
    Gamma_F = (1j ** 5) * G[0] @ G[1] @ G[2] @ G[3] @ G[4] @ G[5] @ G[6] @ G[7] @ G[8] @ G[9]
    w, v = np.linalg.eigh(Gamma_F)
    V = v[:, w.real > 0]
    C_mat = build_C_mat(G)

    Y_H = V.conj().T @ (C_mat @ G[0]) @ V
    A32 = embed_doubled(Y_H)
    print('A32 (internal direction, doubled) Hermitian?', np.allclose(A32, A32.conj().T))

    su3f = build_su3f_generators()
    a_HF = kron(np.eye(32, dtype=complex), su3f[0])
    Jb_HF = make_JbJ_general(P, np.eye(32, dtype=complex), su3f[2])

    # complex kernel (method 1)
    order_one_imgs = []
    for (i, j) in BASIS_IDX:
        D_F_ij = kron(A32, E_gen(i, j))
        Lij = order_one_commutator(D_F_ij, a_HF, Jb_HF)
        order_one_imgs.append(Lij.flatten())
    L_oo = np.array(order_one_imgs).T
    rank = np.linalg.matrix_rank(L_oo, tol=1e-8)
    print('\n[Method 1] rank of order-one map on general complex Y_gen (of 9):', rank)
    print('[Method 1] complex kernel dimension:', 9 - rank)

    Usvd, ssvd, Vhsvd = np.linalg.svd(L_oo)
    null_basis = Vhsvd.conj().T[:, rank:]
    print('[Method 1] kernel basis (as 3x3 Y_gen matrices):')
    for kk in range(null_basis.shape[1]):
        print(np.round(null_basis[:, kk].reshape(3, 3), 3))

    # real cross-check (method 2)
    L_oo_real = realify(L_oo)
    Herm_real = herm_constraint_real()
    Sym_real = sym_constraint_real()

    print('\n[Method 2, real coordinates]')
    print('real dim after order-one alone:', real_dim(L_oo_real))
    print('real dim after order-one + Hermitian:', real_dim(np.vstack([L_oo_real, Herm_real])))
    print('real dim after order-one + Symmetric:', real_dim(np.vstack([L_oo_real, Sym_real])))
    print('real dim after order-one + Hermitian + Symmetric:',
          real_dim(np.vstack([L_oo_real, Herm_real, Sym_real])))
    print('\nreference -- Symmetric alone (expect 12 = 6 complex):', real_dim(Sym_real))
    print('reference -- Hermitian alone (expect 9):', real_dim(Herm_real))

    # explicit surviving texture
    K1 = np.diag([0.707, 0.707, 0])
    K2 = np.diag([0, 0, 1.0])
    K3 = np.array([[0, -1, 0], [0, 0, 0], [0, 0, 0]], dtype=float)
    K4 = np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]], dtype=float)
    Ygen_texture = 1.0 * K1 + 1.0 * K2 + 1.0 * (K3 - K4)
    print('\nExplicit surviving texture (c1=c2=c3=1):')
    print(Ygen_texture)
    print('symmetric?', np.allclose(Ygen_texture, Ygen_texture.T))


if __name__ == '__main__':
    run()
