"""
Phase Z17 (this session) -- tests the one genuinely new candidate from
the fund+adjoint cross-coupling idea: does forcing a fundamental flavon
phi to align with one eigendirection of the adjoint flavon Phi (via the
renormalizable portal term kappa*phi^dag Phi phi, which the theory needs
no NEW representation to write down -- both fields are already flavons
this project has separately motivated, B-3 and Z15) produce a residual
symmetry / order-one constraint genuinely different from Z15 (U(1)xU(1))
and Z16 (SO(3))?

VACUUM: Phi = diag(a,b,c), a+b+c=0, a,b,c generically distinct (Z15's
own hierarchical adjoint vacuum). The portal term phi^dag Phi phi =
sum_i |phi_i|^2 * (Phi)_ii, extremized at fixed |phi|^2 by putting all of
phi into a single eigendirection of Phi (whichever extremizes, by sign of
kappa) -- phi = v*e_i* for some i*.

STABILIZER (verified separately, phase_z17 console check): the pair
(Phi diag distinct, phi=v*e_0) is stabilized by exactly the 1-parameter
family diag(0,theta,-theta) -- a single U(1), NOT the U(1)xU(1) Z15 found
for Phi alone (fixing phi's specific eigen-index removes one of the two
Cartan directions).
"""
import os
import sys
import numpy as np
from numpy import kron

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from z2_hilbert_space import order_one_commutator  # noqa: E402
from phase_z10_real_structure_ansatz import (  # noqa: E402
    load_gammas, build_C_mat, embed_doubled, gamma_prod, E_gen, P,
    sym_constraint_real, realify, BASIS_IDX, run_channel as run_channel_full8,
)


def run_channel_u1(name, Y_H, sym_sign, G_u1):
    Constraint_real = sym_constraint_real(sym_sign)
    GtG = Constraint_real.T @ Constraint_real

    a_HF = kron(np.eye(32, dtype=complex), G_u1)
    beta_prime = P @ np.eye(32, dtype=complex).conjugate() @ np.linalg.inv(P)
    Jb_HF = kron(beta_prime, G_u1.conjugate())
    imgs = []
    for (p, q) in BASIS_IDX:
        Ygen_pq = E_gen(p, q)
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
    print(f'--- {name} (single U(1), aligned fund+adjoint vacuum) ---')
    print('surviving real dim:', surviving, f'  (= {surviving/2:.1f} complex)')
    print('smallest eigenvalues:', np.round(w_eig[:8], 4))
    null_basis = v_eig[:, w_eig < 1e-6 * max(w_eig)]
    for kk in range(null_basis.shape[1]):
        vec = null_basis[:, kk]
        re = vec[:9].reshape(3, 3)
        im = vec[9:].reshape(3, 3)
        if np.max(np.abs(re)) > 1e-6 or np.max(np.abs(im)) > 1e-6:
            print(f'  null vec {kk}: Re=\n{np.round(re,3)}\n  Im=\n{np.round(im,3)}')
    return surviving, null_basis


def run():
    G = load_gammas()
    Gamma_F = (1j ** 5) * G[0] @ G[1] @ G[2] @ G[3] @ G[4] @ G[5] @ G[6] @ G[7] @ G[8] @ G[9]
    w, v = np.linalg.eigh(Gamma_F)
    V = v[:, w.real > 0]
    C_mat = build_C_mat(G)

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
        for ii in range(n):
            for jj in range(ii + 1, n):
                if tup[ii] > tup[jj]:
                    parity *= -1
        return parity

    Hodge = np.zeros((n5, n5))
    for ii, fi in enumerate(forms5):
        for jj, fj in enumerate(forms5):
            val = eps_sign(tuple(fj) + tuple(fi))
            if val != 0:
                Hodge[ii, jj] = float(val)
    P_sd = (np.eye(n5) - 1j * Hodge) / 2
    gamma5_list = [gamma_prod(G, t) for t in forms5]
    Usvd, ssvd, Vhsvd = np.linalg.svd(P_sd)
    Y126 = (V.conj().T @ (C_mat @ sum(Usvd[kk, 0] * gamma5_list[kk] for kk in range(n5))) @ V) / np.sqrt(2)

    G_u1 = np.diag([0, 1, -1]).astype(complex)

    print('=' * 70)
    print('SINGLE U(1): diag(0,1,-1), residual of aligned fund+adjoint vacuum')
    print('=' * 70)
    r10, n10 = run_channel_u1('M10', Y10, 1, G_u1)
    r120, n120 = run_channel_u1('M120', Y120, -1, G_u1)
    r126, n126 = run_channel_u1('M126', Y126, 1, G_u1)

    print()
    print('=' * 70)
    print('SUMMARY: full-8 (Z13) vs Cartan U(1)^2 (Z15) vs SO(3) (Z16) vs single U(1) (this phase)')
    print('=' * 70)
    print(f'{"channel":8s} {"full-8":8s} {"U(1)^2":8s} {"SO(3)":8s} {"U(1)":8s}')
    print(f'{"M10":8s} {"1":8s} {"3":8s} {"1":8s} {r10/2:<8.1f}')
    print(f'{"M120":8s} {"0":8s} {"?":8s} {"0":8s} {r120/2:<8.1f}')
    print(f'{"M126":8s} {"1":8s} {"3":8s} {"1":8s} {r126/2:<8.1f}')


if __name__ == '__main__':
    run()
