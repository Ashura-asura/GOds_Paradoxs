"""
Phase Z4 (proposed, this session) -- Task: Z3 showed the order-one
condition, with a genuine su(3)_f generator in `a`, makes all 9
generation-pair blocks of [[D_F,a],JbJ^-1] nonzero, using GENERIC random
32x32 matrices M1, M2 as the input D_F blocks. Phase X separately proved
that the only PHYSICAL direction in that 32x32 (in fact 16x16 chiral)
space, per generation pair, is a single fixed CG tensor T_H (unique up
to overall complex scale, for a chosen Higgs channel H) -- everything
orthogonal to T_H in that 32x32 space is not a Yukawa coupling at all,
it's gauge-non-invariant and physically absent.

This file asks the concrete question flagged as open in
`session_new_files/RESULT_phase_z3.md` and `docs/POST_AUDIT_TARGET.md`:
does Z3's cross-block effect survive when D_F's blocks are restricted to
the actual physical direction T_H (scalar * T_H, matching Phase X).

Method:
  1. Reuse `vertex_terms_resolved/build_and_test.py`'s own CG
     construction verbatim (same gamma matrices, same C, same V) to get
     M10 -- 10 16x16 matrices, the CG tensor for the vector-10 Higgs
     channel. Pick T = M10[0] as *a* fixed physical direction (Phase X's
     claim is this is unique up to scale for a fixed Higgs VEV
     component; which of the 10 components is picked is a VEV choice,
     external input, same status as every other VEV in this project).
  2. Embed T into the 32-dim Cl(10) factor via V (T_32 = V @ T @ V^dag,
     supported only on the left-chiral 16-dim subspace -- the same
     subspace convention `build_and_test.py` already uses for M10).
  3. Build D_F_phys with blocks (0,1) and (1,2) set to Y01*T_32 and
     Y12*T_32 (Y01, Y12 independent complex scalars -- literally the two
     free Yukawa parameters Phase X says survive), all OTHER blocks
     zero, exactly mirroring Z3's D_F_two construction but replacing
     "random 32x32 matrix" with "scalar times the one physical
     direction."
  4. Run the identical Test A / Test B order-one commutator Z3 already
     ran, on D_F_phys instead of D_F_two, and check TWO things:
       (a) do the same generation-pair blocks go nonzero (does the
           qualitative Z3 effect survive at all on physical input)?
       (b) for the blocks that go nonzero, does the RESULT lie inside
           the physical direction T_32 (a projection test: is the
           induced block proportional to T_32, i.e. does it look like
           it produces MORE terms of the same physical form, or does it
           produce something in the 32x32 space that has no physical
           interpretation as a Yukawa coupling at all)?

Explicitly flagged, per Rule 3 (honest labeling):
  - This is L2, not L1. The chirality-grading convention for D_F used
    by Z2/Z3 (does D_F anticommute with Gamma_F, the standard NCG axiom
    for a Dirac operator?) was never checked against M10's own
    same-chirality-block convention in this file or in Z2/Z3 -- flagged
    explicitly in the written verdict below, not glossed over.
  - Picking T = M10[0] (rather than a specific linear combination
    matching a real GUT-breaking VEV direction) is itself a choice, not
    derived -- consistent with every VEV in this project being an
    external input (docs/POST_AUDIT_TARGET.md section B).
"""
import sys, os
import numpy as np
from numpy import kron
from itertools import combinations, permutations
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from cl10_gamma_J import build_cl10_gammas, solve_charge_conjugation
from z2_hilbert_space import (
    N_GEN, E_kl, order_one_commutator, build_su3f_generators,
    build_sm_generators_on_cl10,
)

np.set_printoptions(precision=4, suppress=True, linewidth=140)


def build_M10():
    """Verbatim method from vertex_terms_resolved/build_and_test.py."""
    G = [np.load(os.path.join(os.path.dirname(__file__), f'gamma_{i}.npy')) for i in range(10)]
    I32 = np.eye(32, dtype=complex)
    data = np.load(os.path.join(os.path.dirname(__file__), 'so10_generators.npz'))
    P_L = data['P_L']

    w, v = np.linalg.eigh(P_L @ P_L.conj().T)
    idx = np.argsort(-w.real)[:16]
    V = v[:, idx]

    A_stack = []
    for a in range(10):
        A = np.kron(G[a].T, I32) + np.kron(I32, G[a].T)
        A_stack.append(A)
    A_stack = np.vstack(A_stack)
    U, s, Vh = np.linalg.svd(A_stack, full_matrices=False)
    C_mat = Vh[-1].reshape(32, 32)
    C_mat = C_mat / np.max(np.abs(C_mat))

    M10 = [V.conj().T @ (C_mat @ G[a]) @ V for a in range(10)]
    return M10, V


def run():
    G = build_cl10_gammas()
    sm = build_sm_generators_on_cl10(G)
    su3f = build_su3f_generators()
    C_plus, resid_c, is_unitary, n_null = solve_charge_conjugation(G, +1)
    print(f"charge-conjugation solve: residual={resid_c:.2e} unitary={is_unitary} n_null={n_null}")

    M10, V = build_M10()
    T16 = M10[0]  # ONE physical direction (VEV component 0), Phase X's fixed tensor
    T32 = V @ T16 @ V.conj().T  # embed into full 32-dim factor, left-chiral block only
    print(f"\n|T16| = {np.linalg.norm(T16):.4f}, |T32| = {np.linalg.norm(T32):.4f} "
          f"(should match -- V is an isometry)")

    def make_JbJ_general(C_F, beta, B_gen):
        beta_prime = C_F @ beta.conjugate() @ np.linalg.inv(C_F)
        return kron(beta_prime, B_gen.conjugate())

    def block_norms(op96):
        norms = np.zeros((N_GEN, N_GEN))
        for k in range(N_GEN):
            for l in range(N_GEN):
                block = op96[k*32:(k+1)*32, l*32:(l+1)*32]
                norms[k, l] = np.linalg.norm(block)
        return norms

    def projection_fraction(op96, T):
        """For each nonzero block, what fraction of its norm lies along T
        (physical) vs orthogonal to T (unphysical)?"""
        Tn = T / np.linalg.norm(T)
        out = np.zeros((N_GEN, N_GEN))
        for k in range(N_GEN):
            for l in range(N_GEN):
                block = op96[k*32:(k+1)*32, l*32:(l+1)*32]
                nrm = np.linalg.norm(block)
                if nrm < 1e-10:
                    out[k, l] = np.nan
                    continue
                coeff = np.vdot(Tn, block)  # projection onto T direction
                out[k, l] = np.abs(coeff) / nrm  # 1.0 = purely physical, 0 = purely orthogonal
        return out

    T_fam_a = su3f[0]
    T_fam_b = su3f[2]

    # --- physical D_F: blocks (0,1),(1,2) are scalar * T32, everything else 0 ---
    Y01, Y12 = 1.3 + 0.4j, -0.7 + 0.9j  # arbitrary nonzero scalars, not fitted to anything
    D_F_phys = kron(Y01 * T32, E_kl(0, 1)) + kron(Y12 * T32, E_kl(1, 2))

    print("\n=== Test A (physical input): pure family-gauge action ===")
    alpha_A = np.eye(32, dtype=complex)
    beta_A = np.eye(32, dtype=complex)
    a_HF_A = kron(alpha_A, T_fam_a)
    Jb_HF_A = make_JbJ_general(C_plus, beta_A, T_fam_b)
    full_A = order_one_commutator(D_F_phys, a_HF_A, Jb_HF_A)
    bn_A = block_norms(full_A)
    print("Block-norm matrix:")
    print(np.round(bn_A, 4))
    print("Fraction of each nonzero block's norm along the PHYSICAL direction T32")
    print("(1.0 = purely physical / another valid Yukawa term; 0.0 = purely")
    print(" unphysical, no Yukawa interpretation; NaN = block is exactly zero):")
    print(np.round(projection_fraction(full_A, T32), 4))

    print("\n=== Test B (physical input): SM generator (x) family generator ===")
    alpha_B = sm['Tx'] + 0.3 * sm['lam3']
    beta_B = sm['Y'] - 0.2 * sm['Tz']
    a_HF_B = kron(alpha_B, T_fam_a)
    Jb_HF_B = make_JbJ_general(C_plus, beta_B, T_fam_b)
    full_B = order_one_commutator(D_F_phys, a_HF_B, Jb_HF_B)
    bn_B = block_norms(full_B)
    print("Block-norm matrix:")
    print(np.round(bn_B, 4))
    print("Fraction along physical direction T32:")
    print(np.round(projection_fraction(full_B, T32), 4))

    return bn_A, bn_B


if __name__ == "__main__":
    run()
