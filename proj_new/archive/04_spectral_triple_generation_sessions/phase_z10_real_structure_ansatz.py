"""
Phase Z10 (this session) -- resolves the modeling caveat flagged at the
end of Z8 and repeated at the end of Z9: was "Hermitian(Y_gen) ansatz
+ D_F(Y_gen) = A32 (x) Y_gen" the right way to embed a Majorana-type
Yukawa coupling in the doubled H_F, or does a construction that uses
the off-diagonal real-structure block directly (rather than tensoring
onto the already-doubled, already-Hermitian A32) treat "symmetric but
not Hermitian" Y_gen differently?

## Why the old ansatz forces Y_gen Hermitian (not a free choice)

D_F(Y_gen) = A32 (x) Y_gen, with A32 = [[0,Y_H],[Y_H^dagger,0]] a 32x32
*already-Hermitian* block matrix (outer block index = doubled copy,
16-dim internal index within each block). Expanding the Kronecker
product block-by-block (mixed-product identity, careful about index
order -- outer block index stays outermost):

    A32 (x) Y_gen = [[ 0 (x) Y_gen,        Y_H (x) Y_gen      ],
                     [ Y_H^dagger (x) Y_gen,   0 (x) Y_gen    ]]
                  = [[ 0,               Y_H (x) Y_gen         ],
                     [ Y_H^dagger (x) Y_gen,     0            ]]

For this to have the correct Hermitian off-diagonal-block form
[[0,X],[X^dagger,0]], the (2,1) block must equal the dagger of the
(1,2) block:

    Y_H^dagger (x) Y_gen  =?=  (Y_H (x) Y_gen)^dagger = Y_H^dagger (x) Y_gen^dagger

Since Y_H^dagger != 0, this forces Y_gen = Y_gen^dagger. So Z8/Z9's
"Hermitian(Y_gen)" requirement was never an independent modeling
choice layered on top of a free ansatz -- it was already baked in by
writing D_F(Y_gen) as a literal Kronecker product with the *doubled*
A32, rather than doubling Y_H (x) Y_gen directly.

## The real-structure-aware alternative

Build the off-diagonal Yukawa block first, in the un-doubled 48-dim
generation-and-internal space, and only then double it the standard
NCG way:

    Y_full(Y_gen) = Y_H (x) Y_gen                      (48 x 48, generically NOT Hermitian)
    D_F_alt(Y_gen) = [[0, Y_full], [Y_full^dagger, 0]]  (96 x 96, Hermitian for ANY Y_gen)

This is Hermitian by construction for every complex Y_gen -- no
Hermiticity constraint on Y_gen is needed or assumed. The only
constraint retained is the one with actual group-theoretic motivation:
Y_gen symmetric (10, 126 channels) or antisymmetric (120 channel),
inherited from the CG-tensor symmetry of the SO(10) channel, same as
Z6 established for Y_H itself.

Everything else (a_HF, J0 b J0^-1, the su(3)_F generator loop, the
Gram-matrix accumulation method) is reused unchanged from Z9 -- this
isolates the ONE thing being tested: does dropping the artificial
Hermitian(Y_gen) constraint change the surviving-parameter count?
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
    """Standard NCG doubling: [[0,Y],[Y^dagger,0]]. Hermitian for ANY Y."""
    n = Y.shape[0]
    return np.block([[np.zeros((n, n)), Y], [Y.conj().T, np.zeros((n, n))]])


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


def run_channel(name, Y_H, sym_sign, su3f, impose_hermitian):
    """
    impose_hermitian=True  reproduces Z9 exactly (old ansatz, D_F = A32 (x) Y_gen).
    impose_hermitian=False is the new real-structure-aware ansatz
                            (D_F = [[0, Y_H (x) Y_gen], [(Y_H (x) Y_gen)^dagger, 0]]).
    """
    Constraint_real = sym_constraint_real(sym_sign)
    GtG = Constraint_real.T @ Constraint_real
    if impose_hermitian:
        Herm_real = herm_constraint_real()
        GtG = GtG + Herm_real.T @ Herm_real

    for i in range(8):
        for j in range(8):
            a_HF = kron(np.eye(32, dtype=complex), su3f[i])
            Jb_HF = make_JbJ_general(P, np.eye(32, dtype=complex), su3f[j])
            imgs = []
            for (p, q) in BASIS_IDX:
                Ygen_pq = E_gen(p, q)
                if impose_hermitian:
                    # old ansatz: D_F = A32 (x) Y_gen, A32 = embed_doubled(Y_H)
                    A32 = embed_doubled(Y_H)
                    D_F_pq = kron(A32, Ygen_pq)
                else:
                    # new ansatz: double the (Y_H (x) Y_gen) block directly
                    Y_full_pq = kron(Y_H, Ygen_pq)
                    D_F_pq = embed_doubled(Y_full_pq)
                Lpq = order_one_commutator(D_F_pq, a_HF, Jb_HF)
                imgs.append(Lpq.flatten())
            L = np.array(imgs).T
            Lr = realify(L)
            GtG += Lr.T @ Lr

    rank = np.linalg.matrix_rank(GtG, tol=1e-6)
    w_eig, v_eig = np.linalg.eigh(GtG)
    surviving = 18 - rank
    print(f'--- {name} (impose_hermitian={impose_hermitian}) ---')
    print('surviving real dim:', surviving)
    print('smallest eigenvalues:', np.round(w_eig[:6], 6))
    null_basis = v_eig[:, w_eig < 1e-6 * max(w_eig)]
    for kk in range(null_basis.shape[1]):
        vec = null_basis[:, kk]
        re = vec[:9].reshape(3, 3)
        im = vec[9:].reshape(3, 3)
        print('Re:')
        print(np.round(re, 4))
        if np.max(np.abs(im)) > 1e-8:
            print('Im:')
            print(np.round(im, 4))
    return surviving, null_basis


def run():
    G = load_gammas()
    Gamma_F = (1j ** 5) * G[0] @ G[1] @ G[2] @ G[3] @ G[4] @ G[5] @ G[6] @ G[7] @ G[8] @ G[9]
    w, v = np.linalg.eigh(Gamma_F)
    V = v[:, w.real > 0]
    C_mat = build_C_mat(G)
    su3f = build_su3f_generators()

    Y10 = V.conj().T @ (C_mat @ G[0]) @ V

    Y120 = V.conj().T @ (C_mat @ gamma_prod(G, (0, 1, 2))) @ V

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

    print('=' * 70)
    print('REPRODUCE Z9 EXACTLY FIRST (impose_hermitian=True) -- sanity check')
    print('=' * 70)
    r10_old, _ = run_channel('M10 (symmetric)', Y10, 1, su3f, True)
    r120_old, _ = run_channel('M120 (antisymmetric)', Y120, -1, su3f, True)
    r126_old, _ = run_channel('M126 (symmetric, complex)', Y126, 1, su3f, True)

    print()
    print('=' * 70)
    print('NEW: real-structure-aware ansatz (impose_hermitian=False)')
    print('=' * 70)
    r10_new, n10_new = run_channel('M10 (symmetric)', Y10, 1, su3f, False)
    r120_new, n120_new = run_channel('M120 (antisymmetric)', Y120, -1, su3f, False)
    r126_new, n126_new = run_channel('M126 (symmetric, complex)', Y126, 1, su3f, False)

    print()
    print('=' * 70)
    print('SUMMARY')
    print('=' * 70)
    print(f'{"channel":10s} {"old (Hermitian(Y_gen))":25s} {"new (real-structure-aware)":25s}')
    print(f'{"M10":10s} {r10_old:<25d} {r10_new:<25d}')
    print(f'{"M120":10s} {r120_old:<25d} {r120_new:<25d}')
    print(f'{"M126":10s} {r126_old:<25d} {r126_new:<25d}')


if __name__ == '__main__':
    run()
