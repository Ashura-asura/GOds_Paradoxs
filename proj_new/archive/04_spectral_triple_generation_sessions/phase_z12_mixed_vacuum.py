"""
Phase Z12 (this session) -- Z11's first flagged next step: every phase
through Z11 turned on ONE channel's Higgs direction at a time. A
realistic symmetry-breaking vacuum has multiple channels nonzero
simultaneously (this project's own earlier phases motivate needing
both M10 and M126 VEVs, e.g. for the seesaw / GUT-breaking pattern).
Because the order-one commutator is LINEAR in D_F, and D_F is linear
in each channel's contribution, turning on two channels at once does
NOT just give the direct sum of the two single-channel constraints --
it gives the joint kernel of the SUM of their commutator images, which
could be larger (cross-channel cancellation: an otherwise-forbidden
texture in one channel compensated by a matching texture in the
other) or identical (no new freedom) to the direct sum. This has to be
checked directly, not assumed either way.

M120 is excluded from the mix here since it separately couples to an
antisymmetric Y_gen (a different real-parameter space entirely, sits
in orthogonal constraint rows already), and it was already shown
forced to zero in isolation across the whole moduli space (Z11) -- the
question worth asking is specifically whether the two SYMMETRIC
channels (10, 126), which live in the same Sym^2(3) representation,
can hide each other's would-be-forbidden components.
"""
import os
import sys
import numpy as np
from numpy import kron

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from z2_hilbert_space import order_one_commutator, build_su3f_generators  # noqa: E402
from phase_z10_real_structure_ansatz import (  # noqa: E402
    load_gammas, build_C_mat, embed_doubled, gamma_prod, E_gen, P,
    sym_constraint_real, realify, BASIS_IDX,
)


def run():
    G = load_gammas()
    Gamma_F = (1j ** 5) * G[0] @ G[1] @ G[2] @ G[3] @ G[4] @ G[5] @ G[6] @ G[7] @ G[8] @ G[9]
    w, v = np.linalg.eigh(Gamma_F)
    V = v[:, w.real > 0]
    C_mat = build_C_mat(G)
    su3f = build_su3f_generators()

    Y10_H = V.conj().T @ (C_mat @ G[0]) @ V

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
    Y126_H = (V.conj().T @ (C_mat @ sum(Usvd[kk, 0] * gamma5_list[kk] for kk in range(n5))) @ V) / np.sqrt(2)

    # Build the joint 36-real-parameter linear map: columns 0..17 are
    # d/d(Y_gen10 real coords), columns 18..35 are d/d(Y_gen126 real coords).
    # Both channels are symmetric -> same sym_constraint_real(1), block-diagonal.
    Constraint10 = sym_constraint_real(1)   # 18x18 acting on first 18 real coords
    Constraint126 = sym_constraint_real(1)  # 18x18 acting on last 18 real coords
    Z18 = np.zeros((18, 18))
    ConstraintJoint = np.block([[Constraint10, Z18], [Z18, Constraint126]])  # (36x36-ish, but rows=36,cols=36? actually rows=36
    GtG = ConstraintJoint.T @ ConstraintJoint

    for i in range(8):
        for j in range(8):
            a_HF = kron(np.eye(32, dtype=complex), su3f[i])
            beta_prime = P @ np.eye(32, dtype=complex).conjugate() @ np.linalg.inv(P)
            Jb_HF = kron(beta_prime, su3f[j].conjugate())

            cols = []
            for (p, q) in BASIS_IDX:  # channel 10 columns
                Y_full_pq = kron(Y10_H, E_gen(p, q))
                D_F_pq = embed_doubled(Y_full_pq)
                Lpq = order_one_commutator(D_F_pq, a_HF, Jb_HF)
                cols.append(Lpq.flatten())
            for (p, q) in BASIS_IDX:  # channel 126 columns
                Y_full_pq = kron(Y126_H, E_gen(p, q))
                D_F_pq = embed_doubled(Y_full_pq)
                Lpq = order_one_commutator(D_F_pq, a_HF, Jb_HF)
                cols.append(Lpq.flatten())

            L = np.array(cols).T  # complex, shape (9216, 18)
            Lr = realify(L)  # real, shape (18432, 36)
            GtG += Lr.T @ Lr

    rank = np.linalg.matrix_rank(GtG, tol=1e-6)
    w_eig, v_eig = np.linalg.eigh(GtG)
    surviving = 36 - rank
    print('=== Mixed vacuum: M10 + M126 simultaneously nonzero ===')
    print('joint surviving real dim:', surviving, '(direct-sum expectation: 2+2=4)')
    print('smallest eigenvalues:', np.round(w_eig[:8], 6))
    null_basis = v_eig[:, w_eig < 1e-6 * max(w_eig)]
    for kk in range(null_basis.shape[1]):
        vec = null_basis[:, kk]
        re10 = vec[:9].reshape(3, 3)
        im10 = vec[9:18].reshape(3, 3)
        re126 = vec[18:27].reshape(3, 3)
        im126 = vec[27:36].reshape(3, 3)
        print(f'-- null vector {kk} --')
        print('Y_gen10 Re:', np.round(re10, 3).tolist(), ' Im:', np.round(im10, 3).tolist())
        print('Y_gen126 Re:', np.round(re126, 3).tolist(), ' Im:', np.round(im126, 3).tolist())
        cross = (np.max(np.abs(re10)) > 1e-3 or np.max(np.abs(im10)) > 1e-3) and \
                (np.max(np.abs(re126)) > 1e-3 or np.max(np.abs(im126)) > 1e-3)
        print('  nonzero in BOTH channels simultaneously (genuine cross-channel mode)?', cross)


if __name__ == '__main__':
    run()
