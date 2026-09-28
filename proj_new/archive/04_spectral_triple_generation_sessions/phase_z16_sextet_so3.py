"""
Phase Z16 (this session) -- tests the "stated reason it would net differently"
Z15's own writeup asked for, rather than trying the next flavon
representation in line.

MOTIVATION (hand-derived, checked below):
A flavon in the SEXTET (6 = Sym^2(3)) of SU(3)_f, phi_ij (complex
symmetric 3x3), has renormalizable potential V = -m^2 I1 + lam1 I1^2 +
lam2 I2, where I1=tr(phi^dag phi), I2=tr((phi^dag phi)^2) -- exactly 2
invariants at quartic order, same count as the adjoint case Z15 tested.
BUT: writing M=phi^dag phi with eigenvalues x_k>=0 (k=1,2,3), V(x) =
-m^2*S + lam1*S^2 + lam2*sum(x_k^2), S=sum(x_k). For lam2>0 (needed for
stability), sum(x_k^2) >= S^2/3 at fixed S with equality iff x1=x2=x3 --
so the GLOBAL minimum over the full stable region of (lam1,lam2) is
*always* at x1=x2=x3 (the democratic point), not a direction that has to
be separately picked by extra couplings the way Z15's adjoint case
needed. This is the structurally different reason: the residual
symmetry is forced generically, not chosen.

At x1=x2=x3=x, phi's Takagi form is D=sqrt(x)*I -- i.e. phi is
proportional to the identity in some SU(3)-rotated basis, phi = v*U*U^T
for the unconstrained U in the earlier orbit language. The stabilizer of
D=v*I under phi -> U D U^T is {U : U U^T = I} = SO(3) (real orthogonal,
det 1) -- verified by direct linearization: for D=v*I, HD+DH* = 0 becomes
H+H*=0 i.e. H purely imaginary+Hermitian => H = i*(real antisymmetric),
i.e. H in the span of the 3 imaginary Gell-Mann generators (lambda2,
lambda5,lambda7) -- confirmed by direct commutator check to close into
su(2)=so(3) (see console check run separately).

THIS FILE: run the same order-one-condition machinery Z15 used
(order_one_commutator, on Phase X's actual M10/M120/M126 CG tensors via
the Z6-Z13 chirality-flipping D_F bridge), restricted to these 3 SO(3)
generators instead of the 2 Cartan ones.
"""
import os
import sys
import numpy as np
from numpy import kron

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from z2_hilbert_space import order_one_commutator, build_su3f_generators  # noqa: E402
from phase_z10_real_structure_ansatz import (  # noqa: E402
    load_gammas, build_C_mat, embed_doubled, gamma_prod, E_gen, P,
    sym_constraint_real, realify, BASIS_IDX, run_channel as run_channel_full8,
)

SO3_IDX = [1, 4, 6]  # su3f indices of the 3 imaginary Gell-Mann generators (lambda2,5,7)


def run_channel_so3(name, Y_H, sym_sign, su3f):
    """Same method as Z15's run_channel_cartan_only, restricted to the
    3-generator SO(3) subalgebra instead of the 2-generator Cartan."""
    Constraint_real = sym_constraint_real(sym_sign)
    GtG = Constraint_real.T @ Constraint_real

    for i in SO3_IDX:
        for j in SO3_IDX:
            a_HF = kron(np.eye(32, dtype=complex), su3f[i])
            beta_prime = P @ np.eye(32, dtype=complex).conjugate() @ np.linalg.inv(P)
            Jb_HF = kron(beta_prime, su3f[j].conjugate())
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
    print(f'--- {name} (SO(3)-only, 3 generators, 9 pairs) ---')
    print('surviving real dim:', surviving, f'  (= {surviving/2:.0f} complex)')
    print('smallest eigenvalues:', np.round(w_eig[:6], 4))
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
    su3f = build_su3f_generators()

    # sanity: confirm SO3_IDX really closes into so(3) (independent of the
    # earlier interactive check)
    g = [su3f[i] for i in SO3_IDX]
    c01 = g[0] @ g[1] - g[1] @ g[0]
    print('closure check [g0,g1] - 0.5i*g2 (should be ~0):',
          np.max(np.abs(c01 - 0.5j * g[2])))

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

    print()
    print('=' * 70)
    print('SANITY: full 8-gen su(3)_F (should reproduce Z9/Z10/Z13 exactly)')
    print('=' * 70)
    r10_full, _ = run_channel_full8('M10', Y10, 1, su3f, False)
    r120_full, _ = run_channel_full8('M120', Y120, -1, su3f, False)
    r126_full, _ = run_channel_full8('M126', Y126, 1, su3f, False)

    print()
    print('=' * 70)
    print('SO(3)-only residual (democratic sextet-flavon vacuum)')
    print('=' * 70)
    r10_so3, n10 = run_channel_so3('M10', Y10, 1, su3f)
    r120_so3, n120 = run_channel_so3('M120', Y120, -1, su3f)
    r126_so3, n126 = run_channel_so3('M126', Y126, 1, su3f)

    print()
    print('=' * 70)
    print('SUMMARY: full su(3)_F  vs  Cartan (Z15)  vs  SO(3) (this phase)')
    print('=' * 70)
    print(f'{"channel":8s} {"full-8":8s} {"Cartan-4(cplx)":16s} {"SO3(cplx)":10s}')
    print(f'{"M10":8s} {r10_full:<8d} {"3 (Z15)":16s} {r10_so3/2:<10.0f}')
    print(f'{"M120":8s} {r120_full:<8d} {"?":16s} {r120_so3/2:<10.0f}')
    print(f'{"M126":8s} {r126_full:<8d} {"3 (Z15)":16s} {r126_so3/2:<10.0f}')


if __name__ == '__main__':
    run()
