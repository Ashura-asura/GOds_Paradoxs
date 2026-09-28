"""
Phase Z3 (proposed extension of Z2, this session) — Task: does letting the
gauge-action element `a` include a genuine SU(3)_f generation-mixing piece
(rather than assuming, as Z2 Task 5 did, that "a is generation-trivial
because SU(3)_f is not part of the gauge algebra") let the order-one
condition relate different generation-pair blocks M_kl of D_F?

Ground-rules bookkeeping (per GROUND_RULES.md):
- Rule 1 at risk: a clean-looking cancellation/non-cancellation is not
  evidence without the mechanism shown. Both the tensor-algebra derivation
  and the direct 96x96 numerical check are given below, not just one.
- Rule 2 at risk: nothing here is reverse-engineered to match a known
  Yukawa hierarchy. No SM mass/mixing value is referenced anywhere.
- Rule 9 (discriminating power): if turning on the family generator
  produces a constraint, the immediately following question is whether
  it comes at zero net cost (a real reduction) or requires new
  unobserved physics (family gauge bosons) that reintroduces at least as
  much freedom elsewhere -- addressed explicitly in the verdict section,
  not left implicit.
- Builds directly on the repo's own Phase Z2 objects (cl10_gamma_J.py,
  z2_hilbert_space.py) -- same Gamma_F/J_F/gamma matrices, not a
  reimplementation with different conventions. build_su3f_generators()
  already existed in z2_hilbert_space.py but was never plugged into `a`
  for the order-one test -- confirmed by grep before writing this file.
"""
import sys, os
import numpy as np
from numpy import kron

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from cl10_gamma_J import build_cl10_gammas, solve_charge_conjugation
from z2_hilbert_space import (
    I3, N_GEN, E_kl, order_one_commutator, build_su3f_generators,
    build_sm_generators_on_cl10,
)

rng = np.random.default_rng(2)


def make_JbJ_general(C_F, beta, B_gen):
    """
    J (beta (x) B_gen) J^-1 for J = (C_F (x) I_3) . conj(.), with beta a
    32x32 Cl(10)-factor operator and B_gen a 3x3 generation-factor
    operator (NOT assumed proportional to I_3, unlike Z2 Task 5).
    Derivation: J is antiunitary, J = U.K (K = complex conjugation),
    U = C_F (x) I_3. For an operator X on H_F, J X J^-1 = U . Xbar . U^-1
    (Xbar = entrywise complex conjugate of X as a matrix). For
    X = beta (x) B_gen, Xbar = beta.conj() (x) B_gen.conj(), and
    U Xbar U^-1 = (C_F beta.conj() C_F^-1) (x) (I_3 B_gen.conj() I_3)
                = beta' (x) B_gen.conj().
    """
    beta_prime = C_F @ beta.conjugate() @ np.linalg.inv(C_F)
    return kron(beta_prime, B_gen.conjugate())


def run():
    G = build_cl10_gammas()
    sm = build_sm_generators_on_cl10(G)
    su3f = build_su3f_generators()  # 8 Gell-Mann/2, already in the repo, unused for `a` until now
    C_plus, resid_c, is_unitary, n_null = solve_charge_conjugation(G, +1)
    print(f"charge-conjugation solve: residual={resid_c:.2e} unitary={is_unitary} n_null={n_null}")

    T_fam_a = su3f[0]   # a genuine family generator, NOT proportional to I_3
    T_fam_b = su3f[2]   # a different one, for beta's generation factor

    # --- Test A: PURE family gauge action, internal (Cl(10)) factor trivial ---
    # a = I_32 (x) T_fam_a   (isolates the effect of the family generator alone)
    alpha_A = np.eye(32, dtype=complex)
    beta_A = np.eye(32, dtype=complex)
    a_HF_A = kron(alpha_A, T_fam_a)
    Jb_HF_A = make_JbJ_general(C_plus, beta_A, T_fam_b)

    M1 = rng.normal(size=(32, 32)) + 1j * rng.normal(size=(32, 32))
    M2 = rng.normal(size=(32, 32)) + 1j * rng.normal(size=(32, 32))
    D_F_two = kron(M1, E_kl(0, 1)) + kron(M2, E_kl(1, 2))

    full_A = order_one_commutator(D_F_two, a_HF_A, Jb_HF_A)

    # does the (0,1) generation-index sector alone, from M1's contribution,
    # still land purely in the (0,1) sector, or does it leak into (0,2)/(1,1)/etc.?
    def block_norms(op96):
        norms = np.zeros((N_GEN, N_GEN))
        for k in range(N_GEN):
            for l in range(N_GEN):
                block = op96[k*32:(k+1)*32, l*32:(l+1)*32]
                norms[k, l] = np.linalg.norm(block)
        return norms

    print("\n=== Test A: pure family-gauge action (alpha=beta=I_32) ===")
    print("Block-norm matrix of [[D_F,a],JbJ^-1] (rows/cols = generation index k,l):")
    print(np.round(block_norms(full_A), 4))
    print("(Z2's own result predicts this should be exactly zero everywhere, since a")
    print(" and JbJ^-1 were always generation-trivial there. Nonzero off-(input)-block")
    print(" entries here would mean SU(3)_f DOES let the order-one condition see")
    print(" cross-generation structure.)")

    # --- Test B: combine internal SM generator with family generator ---
    alpha_B = sm['Tx'] + 0.3 * sm['lam3']
    beta_B = sm['Y'] - 0.2 * sm['Tz']
    a_HF_B = kron(alpha_B, T_fam_a)
    Jb_HF_B = make_JbJ_general(C_plus, beta_B, T_fam_b)
    full_B = order_one_commutator(D_F_two, a_HF_B, Jb_HF_B)
    print("\n=== Test B: SM generator (x) family generator ===")
    print("Block-norm matrix:")
    print(np.round(block_norms(full_B), 4))

    return full_A, full_B


if __name__ == "__main__":
    run()
