"""
Phase Z2 core construction, Tasks 1 / 4 / 5 / 6:
  - explicit H_F = C^32 (x) C^3 (Task 1)
  - SM gauge generators on H_F, extended trivially on generation index
  - the generation-block factorization of the order-one condition
    (Task 4/5/6's actual new content)

Built entirely on top of what already exists in this repo:
  - phases/phase_a1_cl10_core.py's exact gamma-matrix / Witt-pair recipe
    (re-imported via cl10_gamma_J, not re-derived with different
    conventions)
  - support/cl10_gamma_J.py's Gamma_F and J_F (Task 2/3, unmodified here)

No SM Yukawa values are inserted anywhere below. No vacuum/VEV direction
is chosen. No S3 or other external flavor symmetry is added. The only
new ingredient is the generation index itself (C^3) and its SU(3)_f
generators (standard Gell-Mann matrices), both of which are structural
bookkeeping, not fitted numbers.
"""
import numpy as np
from numpy import kron, eye

from cl10_gamma_J import build_cl10_gammas, build_gamma_F, solve_charge_conjugation

N_CL = 32
N_GEN = 3
I3 = np.eye(N_GEN, dtype=complex)


def build_generation_basis():
    """Standard orthonormal C^3 basis; nothing to derive, just definitional."""
    return [np.eye(N_GEN, dtype=complex)[:, i] for i in range(N_GEN)]


def build_su3f_generators():
    """8 standard Gell-Mann matrices / 2 (Hermitian, traceless, su(3) algebra)."""
    GM = [
        np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex),
        np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex),
        (1 / np.sqrt(3)) * np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex),
    ]
    return [g / 2 for g in GM]


def build_sm_generators_on_cl10(G):
    """Phase A1's own SU(3)_c x SU(2)_L x U(1)_Y generators, 32x32, unchanged recipe."""
    ops = [(-G[2 * j] + 1j * G[2 * j + 1]) / 2 for j in range(5)]
    dops = [o.conj().T for o in ops]
    Nc = [d @ o for o, d in zip(ops, dops)]
    lam3 = dops[0] @ ops[0] - dops[1] @ ops[1]
    lam8 = (dops[0] @ ops[0] + dops[1] @ ops[1] - 2 * dops[2] @ ops[2]) / np.sqrt(3)
    Tp = dops[3] @ ops[4]
    Tm = dops[4] @ ops[3]
    Tx = (Tp + Tm) / 2
    Ty = (Tp - Tm) / (2j)
    Tz = (Nc[3] - Nc[4]) / 2
    Y_hyper = (2 * (Nc[0] + Nc[1] + Nc[2]) / 3) - (Nc[3] + Nc[4])
    return {'lam3': lam3, 'lam8': lam8, 'Tx': Tx, 'Ty': Ty, 'Tz': Tz, 'Y': Y_hyper}


def extend_to_HF(op_32):
    """a -> a (x) I_3 : trivial extension of a Cl(10)-factor operator to H_F."""
    return kron(op_32, I3)


def make_J_of_HF(C_F):
    """
    J on H_F = C^32 (x) C^3, antiunitary: J(v) = (C_F (x) I_3) . conj(v).
    Generation-trivial by construction: no flavor charge-conjugation
    structure is assumed or invented; SU(3)_f is a spectator to J.
    """
    U = kron(C_F, I3)

    def J(v):
        return U @ v.conjugate()

    return U, J


def E_kl(k, l):
    """3x3 generation matrix unit."""
    e = np.zeros((N_GEN, N_GEN), dtype=complex)
    e[k, l] = 1.0
    return e


def order_one_commutator(D_F, a_HF, Jb_HF):
    """[[D_F,a],JbJ^-1] on the full 96-dim H_F, no shortcuts."""
    inner = D_F @ a_HF - a_HF @ D_F
    return inner @ Jb_HF - Jb_HF @ inner


def predicted_block_commutator(M_kl, alpha, beta_prime):
    """
    The claimed closed form for a single generation-pair block turned on:
    [[M_kl,alpha],beta_prime], living purely in the 32-dim Cl(10) factor.
    """
    inner = M_kl @ alpha - alpha @ M_kl
    return inner @ beta_prime - beta_prime @ inner
