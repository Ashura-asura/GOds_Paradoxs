"""
Phase Z11 (this session) -- Z10's own "next step": Z6-Z9 (and Z10) all
fixed ONE internal Higgs direction per channel (M10[0]=G[0], one M120
triple, one M126 ONB component) and never checked whether "Y_gen only
survives as c*I_3 (or 0 for M120)" holds across the *whole* internal
moduli space of each channel, or was special to the one direction
tested. This phase sweeps:

  - M10:  all 10 gamma directions G[0..9], plus 5 random real unit
          linear combinations (points on the internal S^9)
  - M120: 15 of the 120 antisymmetric triples, plus 5 random real
          linear combinations of triples
  - M126: 15 of the 126 orthonormal self-dual components, plus 5
          random complex linear combinations within the self-dual
          subspace

using the corrected (Z10) real-structure-aware ansatz throughout --
no artificial Hermitian(Y_gen) constraint.
"""
import os
import sys
import itertools
import numpy as np
from numpy import kron

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from z2_hilbert_space import build_su3f_generators  # noqa: E402
from phase_z10_real_structure_ansatz import (  # noqa: E402
    load_gammas, build_C_mat, gamma_prod, run_channel,
)

N = 32


def texture_is_scalar_identity(null_basis, tol=1e-3):
    """True if every vector in the null space is (a real combo of) c*I_3, c complex."""
    if null_basis.shape[1] == 0:
        return True  # trivially, nothing survives (M120 case)
    for kk in range(null_basis.shape[1]):
        vec = null_basis[:, kk]
        re = vec[:9].reshape(3, 3)
        im = vec[9:].reshape(3, 3)
        M = re + 1j * im
        off_diag = M - np.diag(np.diag(M))
        if np.max(np.abs(off_diag)) > tol:
            return False
        d = np.diag(M)
        if np.max(np.abs(d - d[0])) > tol:
            return False
    return True


def summarize(name, Y_H, sym_sign, su3f, expected_dim):
    surv, null_basis = run_channel(name, Y_H, sym_sign, su3f, False)
    scalar_ok = texture_is_scalar_identity(null_basis)
    status = 'OK' if (surv == expected_dim and scalar_ok) else 'MISMATCH'
    print(f'  >>> {name}: surviving={surv} (expected {expected_dim}), '
          f'texture=scalar*I3: {scalar_ok}  [{status}]')
    return status == 'OK'


def run():
    G = load_gammas()
    Gamma_F = (1j ** 5) * G[0] @ G[1] @ G[2] @ G[3] @ G[4] @ G[5] @ G[6] @ G[7] @ G[8] @ G[9]
    w, v = np.linalg.eigh(Gamma_F)
    V = v[:, w.real > 0]
    C_mat = build_C_mat(G)
    su3f = build_su3f_generators()
    rng = np.random.default_rng(42)

    all_ok = True

    print('=' * 70)
    print('M10 sweep -- all 10 gamma directions')
    print('=' * 70)
    for a in range(10):
        Y_H = V.conj().T @ (C_mat @ G[a]) @ V
        ok = summarize(f'M10[{a}]', Y_H, 1, su3f, 2)
        all_ok &= ok

    print()
    print('M10 sweep -- 5 random real unit directions on internal S^9')
    for r in range(5):
        n = rng.normal(size=10)
        n = n / np.linalg.norm(n)
        Y_H = V.conj().T @ (C_mat @ sum(n[a] * G[a] for a in range(10))) @ V
        ok = summarize(f'M10[random_{r}]', Y_H, 1, su3f, 2)
        all_ok &= ok

    print()
    print('=' * 70)
    print('M120 sweep -- 15 of 120 antisymmetric triples')
    print('=' * 70)
    triples = list(itertools.combinations(range(10), 3))
    rng.shuffle(triples)
    for t in triples[:15]:
        Y_H = V.conj().T @ (C_mat @ gamma_prod(G, t)) @ V
        ok = summarize(f'M120{t}', Y_H, -1, su3f, 0)
        all_ok &= ok

    print()
    print('M120 sweep -- 5 random real linear combinations of triples')
    for r in range(5):
        coeffs = rng.normal(size=15)
        combo = sum(c * gamma_prod(G, t) for c, t in zip(coeffs, triples[:15]))
        Y_H = V.conj().T @ (C_mat @ combo) @ V
        ok = summarize(f'M120[random_{r}]', Y_H, -1, su3f, 0)
        all_ok &= ok

    print()
    print('=' * 70)
    print('M126 sweep -- 15 of 126 self-dual ONB components')
    print('=' * 70)
    n, k = 10, 5
    forms5 = list(itertools.combinations(range(n), k))
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
    # self-dual subspace = column span of Usvd[:, :126] (top singular vectors, s=1)
    sd_dim = int(np.sum(ssvd > 0.5))
    print(f'(self-dual subspace dimension: {sd_dim})')
    idxs = list(range(sd_dim))
    rng.shuffle(idxs)
    for kk in idxs[:15]:
        Y_H = (V.conj().T @ (C_mat @ sum(Usvd[mm, kk] * gamma5_list[mm] for mm in range(n5))) @ V) / np.sqrt(2)
        ok = summarize(f'M126[onb_{kk}]', Y_H, 1, su3f, 2)
        all_ok &= ok

    print()
    print('M126 sweep -- 5 random complex linear combinations within self-dual subspace')
    for r in range(5):
        coeffs = rng.normal(size=sd_dim) + 1j * rng.normal(size=sd_dim)
        coeffs = coeffs / np.linalg.norm(coeffs)
        combo_vec = Usvd[:, :sd_dim] @ coeffs
        Y_H = (V.conj().T @ (C_mat @ sum(combo_vec[mm] * gamma5_list[mm] for mm in range(n5))) @ V) / np.sqrt(2)
        ok = summarize(f'M126[random_{r}]', Y_H, 1, su3f, 2)
        all_ok &= ok

    print()
    print('=' * 70)
    print('OVERALL:', 'ALL DIRECTIONS CONSISTENT' if all_ok else 'MISMATCH FOUND -- SEE ABOVE')
    print('=' * 70)


if __name__ == '__main__':
    run()
