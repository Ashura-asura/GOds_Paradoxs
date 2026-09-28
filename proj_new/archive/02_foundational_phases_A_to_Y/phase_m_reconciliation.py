"""
Phase M: Does Phase L's SU(2)_LxSU(2)_R Actually Coexist With Phase A1's
Charge Assignment on the SAME 16-plet? [L1, NEW]
======================================================================
Direct test: Phase A1 built SU(2)_L from NUMBER-CONSERVING bilinears
(a_3^dagger a_4, etc) on Witt pair {3,4} -- by construction these
commute with total fermion number N_tot, so they act entirely WITHIN
one fixed chiral 16-plet (or its complement 16bar). Phase L built a
second, independent su(2) (T^-, candidate SU(2)_R) from raw GAMMA
MATRIX bilinears on the same pair. Gamma matrices mix creation and
annihilation operators -- so it is NOT obvious T^- conserves fermion
number. If it doesn't, T^- does not act as a symmetry within a single
16 the way CCvS's SU(2)_R must; it would instead connect the 16 to its
conjugate 16bar. Checked directly, not assumed either way.
"""
import numpy as np

print('=' * 72)
print('Phase M: Fermion-number conservation of Phase L\'s SU(2)_L / SU(2)_R')
print('=' * 72)

import sys
sys.path.insert(0, '.')
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'support'))
from qosc_division_connection import build_octonion_structure_constants

C, _, _, _ = build_octonion_structure_constants()
s1 = np.array([[0, 1], [1, 0]], dtype=complex)
s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
s3 = np.array([[1, 0], [0, -1]], dtype=complex)
I8 = np.eye(8, dtype=complex)
I16 = np.eye(16, dtype=complex)
G8 = [np.kron(s1, C[i]) for i in range(1, 8)] + [1j * np.kron(s2, I8)]
gammas = [np.kron(G8[i], s3) for i in range(8)] + [
    np.kron(I16, 1j * np.array([[0, 1], [1, 0]], dtype=complex)),
    np.kron(I16, 1j * np.array([[0, -1j], [1j, 0]], dtype=complex)),
]

# Phase A1's Fock operators (exact reproduction)
ops = [(-gammas[2*j] + 1j * gammas[2*j+1]) / 2 for j in range(5)]
dops = [o.conj().T for o in ops]
Nc = [d @ o for o, d in zip(ops, dops)]
N_tot = sum(Nc)

def comm(A, B):
    return A @ B - B @ A

# Phase A1's SU(2)_L (number-conserving, built from pair {3,4})
Tp_A1 = dops[3] @ ops[4]
Tm_A1 = dops[4] @ ops[3]
Tz_A1 = (Nc[3] - Nc[4]) / 2

# Phase L's SO(4) self-dual/anti-self-dual construction (same pair, gamma indices 6-9)
idx = [6, 7, 8, 9]
g = [gammas[i] for i in idx]
M = {}
for a in range(4):
    for b in range(a+1, 4):
        M[(a, b)] = (1j/4) * comm(g[a], g[b])
D1, D2, D3 = M[(2,3)], -M[(1,3)], M[(1,2)]
M0 = [M[(0,1)], M[(0,2)], M[(0,3)]]
Tplus  = [0.5*(M0[i] + [D1,D2,D3][i]) for i in range(3)]
Tminus = [0.5*(M0[i] - [D1,D2,D3][i]) for i in range(3)]

print("\nCHECK 1: does Phase A1's SU(2)_L (Tz_A1) commute with N_tot "
      "(i.e. stay within one fixed-chirality 16)?")
print(f"  [Tz_A1, N_tot] = 0 : "
      f"{np.allclose(comm(Tz_A1, N_tot), 0, atol=1e-8)}  (expected: True, by construction)")

print("\nCHECK 2: does Phase L's T^(+) (candidate SU(2)_L replacement) "
      "commute with N_tot?")
for i, name in enumerate(['T+_x','T+_y','T+_z']):
    ok = np.allclose(comm(Tplus[i], N_tot), 0, atol=1e-8)
    print(f"  [{name}, N_tot] = 0 : {ok}")

print("\nCHECK 3: does Phase L's T^(-) (candidate SU(2)_R) "
      "commute with N_tot?")
for i, name in enumerate(['T-_x','T-_y','T-_z']):
    ok = np.allclose(comm(Tminus[i], N_tot), 0, atol=1e-8)
    print(f"  [{name}, N_tot] = 0 : {ok}")

print("\nCHECK 4: is Phase A1's Tz_A1 proportional to Phase L's T+_z "
      "(i.e. is 'SU(2)_L' the same generator under both constructions)?")
# Compare on the pair-{3,4} subspace only (project out other Fock sectors implicitly
# since both are built purely from that pair's own gamma content)
ratio_test = Tz_A1 - Tplus[2]
print(f"  Tz_A1 - T+_z == 0 : {np.allclose(ratio_test, 0, atol=1e-8)}")
diff_norm = np.linalg.norm(Tz_A1 - Tplus[2])
sum_norm = np.linalg.norm(Tz_A1 + Tplus[2])
print(f"  ||Tz_A1 - T+_z|| = {diff_norm:.4f},  ||Tz_A1 + T+_z|| = {sum_norm:.4f}"
      f"  (both nonzero => not simply equal or opposite)")

print("\nCHECK 5: is Phase A1's Tz_A1 related to Phase L's T^(-)_z instead "
      "(the number-conserving candidate)?")
diff2 = np.linalg.norm(Tz_A1 - Tminus[2])
sum2 = np.linalg.norm(Tz_A1 + Tminus[2])
print(f"  ||Tz_A1 - T-_z|| = {diff2:.4f},  ||Tz_A1 + T-_z|| = {sum2:.4f}")

print("\nCHECK 6: eigenvalue spectrum comparison on the 4-dim pair-{3,4} "
      "occupation subspace (restrict to states differing only in b3,b4, "
      "holding color bits fixed at 0,0,0, i.e. the leptonic sector)")
# Build |00000>: unique state annihilated by all a_i
import itertools
# Find the vacuum: annihilated by all ops
dim = 32
vac_candidates = []
# vacuum is joint kernel of all annihilation ops
A = np.vstack(ops)
# find null space
u, s, vh = np.linalg.svd(A)
null_mask = s < 1e-8
# ops is 5*32 x 32; take right null vectors where singular value ~0
# Simplify: find eigenvector of N_tot with eigenvalue 0
evals, evecs = np.linalg.eigh(N_tot)
vac_idx = np.argmin(np.abs(evals))
vac = evecs[:, vac_idx]
print(f"  N_tot eigenvalue of chosen vacuum state: {evals[vac_idx]:.4f}")

# Build the 4 leptonic states (b0=b1=b2=0, b3,b4 vary) by applying dops[3],dops[4]
state_00 = vac
state_10 = dops[3] @ vac
state_01 = dops[4] @ vac
state_11 = dops[3] @ dops[4] @ vac
states = {'|00000>': state_00, '|00010>(b3=1)': state_10,
          '|00001>(b4=1)': state_01, '|00011>(b3=b4=1)': state_11}

print(f"\n  {'state':22s} {'Tz_A1':>10s} {'T+_z':>10s} {'T-_z':>10s}")
for name, st in states.items():
    n = st / (np.linalg.norm(st) + 1e-12)
    tzA1 = np.real(n.conj() @ Tz_A1 @ n)
    tpz  = np.real(n.conj() @ Tplus[2] @ n)
    tmz  = np.real(n.conj() @ Tminus[2] @ n)
    print(f"  {name:22s} {tzA1:10.3f} {tpz:10.3f} {tmz:10.3f}")

print("""
HONEST INTERPRETATION:
""")

print('=' * 72)
print('CHECK 7 (the real question): same generator, or same REPRESENTATION')
print('in a rotated basis, or a genuinely different symmetry?')
print('=' * 72)
Tx_A1 = (Tp_A1 + Tm_A1) / 2
Ty_A1 = (Tp_A1 - Tm_A1) / (2j)
Casimir_A1 = Tx_A1 @ Tx_A1 + Ty_A1 @ Ty_A1 + Tz_A1 @ Tz_A1
Casimir_minus = sum(Tminus[i] @ Tminus[i] for i in range(3))
Casimir_plus = sum(Tplus[i] @ Tplus[i] for i in range(3))

print(f"Casimir_A1 == Casimir(T^-) as operators (same rep, rotated basis) : "
      f"{np.allclose(Casimir_A1, Casimir_minus, atol=1e-6)}")
print(f"Casimir_A1 == Casimir(T^+) as operators : "
      f"{np.allclose(Casimir_A1, Casimir_plus, atol=1e-6)}")

ev_A1 = np.sort(np.round(np.linalg.eigvalsh(Casimir_A1), 4))
ev_minus = np.sort(np.round(np.linalg.eigvalsh(Casimir_minus), 4))
print(f"\nCasimir_A1 eigenvalue spectrum (32-dim):    {np.unique(ev_A1)}")
print(f"Casimir(T^-) eigenvalue spectrum (32-dim):  {np.unique(ev_minus)}")
print(f"Same eigenvalue content -> same total representation structure: "
      f"{np.allclose(ev_A1, ev_minus, atol=1e-4)}")

print('=' * 72)
print('HONEST CONCLUSION -- this CORRECTS Phase L, does not just extend it')
print('=' * 72)
print("""
Phase L confirmed the ABSTRACT group theory: Cl(10)'s Witt pair {3,4}
supports two mutually-commuting su(2) algebras via the SO(4) self-
dual/anti-self-dual split. That computation was correct and stands.

But reconciling it with Phase A1's actual fermion representation
(this phase) shows something Phase L did not check and got wrong by
omission: the two su(2)'s are NOT both usable as independent physical
symmetries of a single 16-plet.
  - T^(+) does not fully commute with total fermion number N_tot --
    it mixes states across different N_tot sectors, so it cannot act
    as an internal symmetry within one fixed-chirality 16 at all.
  - T^(-) DOES commute with N_tot (good), but its Casimir operator is
    IDENTICAL, eigenvalue-for-eigenvalue, to Phase A1's original
    SU(2)_L Casimir. That means T^(-) is not a new, independent
    SU(2)_R -- it is the SAME physical SU(2)_L symmetry, written in a
    rotated generator basis.

CORRECTED STATUS: Cl(10) x E8, in this specific fermionic
representation, does NOT contain a genuine second, independent SU(2)
next to SU(2)_L. The SO(4)=SU(2)xSU(2) decomposition is real algebra,
but it does not produce two DISTINGUISHABLE physical symmetries when
applied to the actual 16-plet -- one candidate collapses onto the
already-known SU(2)_L, the other isn't even a valid symmetry of a
single 16. Phase J's SU(2)_R compatibility question, which Phase L
reported as "resolved," is REOPENED as unresolved -- and this
particular route (self-dual/anti-self-dual split of Cl(10)'s own
pair {3,4}) is now a checked, closed dead end for it, not an open
possibility. RESEARCH_ROADMAP.md and solution.md are being corrected
to reflect this, not just appended to.
""")
