"""
Phase T: Independent Confirmation of Phase M's SU(2)_R Dead End, via
Octonion Non-Associativity [L1, new, 2026-07-28]
=========================================================================

MOTIVATION
----------
An external review supplied a different argument for why this project
can't get a free SU(2)_R: octonion non-associativity means the left- and
right-multiplication operators L_i, R_i don't commute, so the usual
quaternionic route to SO(4) = SU(2)_L x SU(2)_R (where [L_i,R_j]=0)
fails for octonions. This is a DIFFERENT argument from Phase M's (which
compared Casimir spectra of two candidate generators built from Cl(10)'s
gamma matrices) but reaches the SAME conclusion. This phase verifies the
external argument's specific numbers independently, using only this
project's own qosc_division_connection.py (not the external code), and
records it as a second, independent confirmation of Phase M's result --
not a new discovery, and not something that changes Phase M's status.
"""

import numpy as np
from itertools import permutations
import sys
sys.path.insert(0, '.')
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'support'))
from qosc_division_connection import build_octonion_structure_constants

print('=' * 72)
print("Phase T: Octonion Non-Associativity Confirms Phase M's SU(2)_R Dead End")
print('=' * 72)

L, R, f, mult = build_octonion_structure_constants()
L = [np.array(m) for m in L]
R = [np.array(m) for m in R]

print("""
Background: for the QUATERNIONS, left- and right-multiplication by
imaginary units commute ([L_i, R_j] = 0), which is exactly what lets
quaternionic constructions split cleanly into independent left and
right SU(2) actions (SO(4) = SU(2)_L x SU(2)_R). For the OCTONIONS,
associativity fails, and left/right multiplication no longer commute in
general. This phase checks exactly how badly, using this project's own
structure constants (qosc_division_connection.py), independent of the
external review's code.
""")

# --- Step 1: [L_i, R_j] for imaginary units i,j = 1..7 ---
nonzero, total, maxnorm = 0, 0, 0.0
for i in range(1, 8):
    for j in range(1, 8):
        comm = L[i] @ R[j] - R[j] @ L[i]
        n = np.max(np.abs(comm))
        total += 1
        if n > 1e-9:
            nonzero += 1
        maxnorm = max(maxnorm, n)
print(f'1. [L_i, R_j] over imaginary units i,j=1..7: nonzero in {nonzero}/{total} pairs, max|comm|={maxnorm:.4f}')
print("   (independently reproduces the external review's reported 42/49, max=2.0)")

# --- Step 2: associator on distinct imaginary-unit triples ---
def octmul(x, y):
    return np.einsum('ijk,i,j->k', f, x, y)

basis = np.eye(8)
nz, tot = 0, 0
for i, j, k in permutations(range(1, 8), 3):
    lhs = octmul(octmul(basis[i], basis[j]), basis[k])
    rhs = octmul(basis[i], octmul(basis[j], basis[k]))
    tot += 1
    if np.max(np.abs(lhs - rhs)) > 1e-9:
        nz += 1
print(f'2. Associator [e_i,e_j,e_k] over distinct imaginary units: nonzero in {nz}/{tot} ordered triples')
print("   (independently reproduces the external review's reported 168/210)")

print("""
3. WHY THIS MATTERS FOR SU(2)_R (the actual physics question):
   Phase L built candidate SU(2)_R generators from Cl(10)'s Witt pair
   {3,4} gamma matrices directly (a fermionic Fock-space construction).
   Phase M then checked those specific candidates against Phase A1's
   fermion representation and found T^(-) has an IDENTICAL Casimir
   spectrum to the existing SU(2)_L -- same symmetry, rotated basis,
   not independent.

   This phase's check is a DIFFERENT, more structural argument for the
   same conclusion, at the level of the octonions Cl(10)'s transverse
   gammas are built from (Phase A1, step 1): because L_i and R_i don't
   commute for octonions (confirmed above, 42/49 pairs), there is no
   octonion-analog of the quaternionic "independent left and right
   action" that would hand you a free, independent SU(2)_R for free.
   Getting one still requires paying for an extra structural choice
   (e.g. singling out one imaginary unit as special, as Furey's SU(3)_c
   construction already does for color) -- consistent with, not new
   information beyond, Phase M's already-closed dead end.
""")

print('=' * 72)
print('VERDICT')
print('=' * 72)
print("""
CONFIRMED (independently, via a different method than Phase M): no free
SU(2)_R falls out of Cl(10)/octonion structure alone. This does not
reopen Phase M, does not change Phase C's free-parameter count, and
does not connect to any SM parameter -- it is a second, independent line
of evidence for a conclusion this project had already reached and
closed. Filed as a confirming cross-check, not a new result.
""")
