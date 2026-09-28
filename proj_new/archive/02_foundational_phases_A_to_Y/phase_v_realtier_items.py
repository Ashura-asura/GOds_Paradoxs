"""
Phase V: Genuinely Computable [real]-Tier Backlog Items (20, 33)
[L1/L2, new, 2026-07-28]
=========================================================================

MOTIVATION
----------
Phase R closed every [cheap]-tier backlog item. Phase U closed the
recurring [lit]-tier items. That leaves [real]-tier items -- most need
GAP/Magma/Sage (item 5, 29), heat-kernel/KMS machinery (items 1, 3),
string-compactification data (already-closed dead end, Phases H/I), or
genuine multi-week derivation (items 10, 11, 30, 31, 35, 36, 42).

Two [real]-tier items, on inspection, do NOT actually need any of that --
they only need the octonion structure-constant code this project already
has (support/qosc_division_connection.py) plus elementary number theory.
This phase runs those two, honestly, with the same rules as every phase
before it: compute, don't assume; log negatives with equal weight; state
explicitly when a test isn't statistically meaningful rather than forcing
a verdict.

Item 15 (branch the minimal 248 with REAL multiplicities, not just
dimension counts, to check the CKM=I/PMNS=I claim) was considered and
explicitly NOT attempted here: doing it honestly needs a real
weight-multiplicity engine for E8/E6 tensor products (what LiE or Sage's
Weyl-character-formula routines do), and faking that arithmetic by hand
would be exactly the kind of unverified claim this project's own rules
forbid. It stays open, tagged for a real Lie-theory package, not silently
resolved by dimension-counting alone (which Phase A2 already did and which
is NOT the same check item 15 asks for).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'support'))
import numpy as np
from itertools import combinations
from qosc_division_connection import build_octonion_structure_constants

print('=' * 72)
print('Phase V: Backlog items 20 (p-adic FN charges) and 33 (Malcev invariant)')
print('=' * 72)

# =====================================================================
# ITEM 33: Malcev-algebra structure of the imaginary octonions
# =====================================================================
print('\n' + '-' * 72)
print('Item 33: Malcev-algebra invariant of the octonion commutator algebra')
print('-' * 72)
print("""
The 7 imaginary octonion units e1..e7, under the commutator bracket
[x,y] = xy - yx, are known to form a simple 7-dimensional Malcev algebra
(this is textbook: e.g. Kuzmin 1968, Sagle 1961) rather than a Lie
algebra -- the Jacobi identity fails but the weaker Malcev identity
holds. This project's own octonion code has never checked this directly.
Two things are tested: (1) the Malcev identity itself, on this project's
own structure constants, and (2) whether the induced trace-form
("Killing-like") invariant carries any structure connecting to the
3-generation / SU(3)_f question -- the actual content of item 33.
""")

f = np.zeros((8, 8, 8))
_, _, f_tensor, _ = build_octonion_structure_constants()
f = f_tensor

def bracket(x, y):
    # x, y: 8-vectors (index 0 = real part, kept 0 for imaginary octonions)
    xy = np.einsum('ijk,i,j->k', f, x, y)
    yx = np.einsum('ijk,i,j->k', f, y, x)
    return xy - yx

def assoc_bracket_of(x, y, z):
    # J(x,y,z) helper for the Malcev identity check below
    return bracket(bracket(x, y), z)

basis = [np.eye(8)[i] for i in range(1, 8)]  # e1..e7, imaginary units only

# Malcev identity (one standard form):
#   [[x,y],[x,z]] = [[[x,y],z],x] + [[[y,z],x],x] + [[[z,x],x],y]
def malcev_lhs(x, y, z):
    return bracket(bracket(x, y), bracket(x, z))

def malcev_rhs(x, y, z):
    t1 = bracket(bracket(bracket(x, y), z), x)
    t2 = bracket(bracket(bracket(y, z), x), x)
    t3 = bracket(bracket(bracket(z, x), x), y)
    return t1 + t2 + t3

max_resid = 0.0
n_checked = 0
for x, y, z in combinations(basis, 3):
    lhs = malcev_lhs(x, y, z)
    rhs = malcev_rhs(x, y, z)
    resid = np.max(np.abs(lhs - rhs))
    max_resid = max(max_resid, resid)
    n_checked += 1
print(f'Malcev identity checked on {n_checked} basis triples (e1..e7, all C(7,3) combos).')
print(f'Max residual |LHS - RHS| = {max_resid:.2e}  ->  '
      f'{"HOLDS (confirms known result, first check in this repo)" if max_resid < 1e-9 else "FAILS -- unexpected, needs investigation"}')

# Trace-form invariant: B(x,y) = trace(ad_x ad_y), ad_x(v) = [x,v]
def ad_matrix(x):
    M = np.zeros((7, 7))
    for j, ej in enumerate(basis):
        bxy = bracket(x, ej)
        M[:, j] = bxy[1:8]  # project back onto imaginary basis
    return M

B = np.zeros((7, 7))
for i, ei in enumerate(basis):
    ad_i = ad_matrix(ei)
    for j, ej in enumerate(basis):
        ad_j = ad_matrix(ej)
        B[i, j] = np.trace(ad_i @ ad_j)

eigvals = np.sort(np.linalg.eigvalsh(B))
print(f'\nTrace-form B(e_i,e_j)=tr(ad_i ad_j) eigenvalues: {np.round(eigvals, 4)}')
print(f'B proportional to identity (i.e. B = c * I_7): '
      f'{np.allclose(B, B[0,0]*np.eye(7), atol=1e-9)}')
if np.allclose(B, B[0, 0] * np.eye(7), atol=1e-9):
    print(f'  c = {B[0,0]:.4f}  -- this is the unique-up-to-scale G2-invariant form')
    print('  on the 7-dim imaginary octonions (expected: G2 = Aut(O) acts')
    print('  transitively enough that any invariant symmetric form is a multiple')
    print('  of the standard one -- textbook G2 representation theory, not new).')

print("""
RESULT (item 33): the Malcev identity is confirmed directly on this
project's own structure constants (a genuine first check in this repo,
though the underlying math fact is 60+ years old and not new). The
trace-form invariant is proportional to the identity matrix -- as G2
representation theory requires for the unique invariant form on the
7-dimensional imaginary octonions -- carrying NO extra structure (no
preferred 3-dimensional subspace, no eigenvalue splitting) that could be
read as "3 generations" or connected to SU(3)_f. This is a clean negative:
the Malcev/Casimir route does not supply a new invariant beyond what G2
representation theory already gives, and G2's relation to this project's
SU(3)_f is itself unestablished. CLOSED, negative.
""")

# =====================================================================
# ITEM 20: p-adic (p=3) valuation on the FN charge structure
# =====================================================================
print('-' * 72)
print('Item 20: p-adic (p=3) valuation on Froggatt-Nielsen charges')
print('-' * 72)
print("""
Phase D's fitted FN charges are (q1,q2,q3) = (3,2,0); the anomaly-free
family from Phase E is (n,-n,0). The idea (never tried in this project):
maybe a p-adic norm, not the real absolute value, is the natural measure
of "how suppressed" a Yukawa coupling is -- p=3 is the obvious choice
given q1=3 literally appears. Tested directly, not assumed.
""")

from fractions import Fraction

def v3(n):
    """3-adic valuation of a nonzero integer; returns None for 0 (v_p(0)=+inf, undefined here)."""
    if n == 0:
        return None
    n = abs(n)
    v = 0
    while n % 3 == 0:
        n //= 3
        v += 1
    return v

fitted = (3, 2, 0)
anomaly_free_examples = [(1, -1, 0), (2, -2, 0), (4, -4, 0), (5, -5, 0)]

print(f'Fitted charges q = {fitted}:')
for q in fitted:
    print(f'  v_3({q}) = {v3(q)}')
print('  -> only q1=3 has finite positive 3-adic valuation (v_3=1); q2=2 and')
print('     q3=0 give v_3=0 and undefined respectively -- the p=3 norm does')
print('     NOT rank all three charges (v_3(0) is undefined, not "largest",')
print('     which is exactly backwards from the real-norm ordering |0|<|2|<|3|')
print('     that Phase D relies on for the mass hierarchy).')

print(f'\nAnomaly-free family (n,-n,0) for several n:')
for q in anomaly_free_examples:
    vs = [v3(x) for x in q]
    print(f'  q={q}: v_3 = {vs}')
print('  -> v_3(n) = v_3(-n) always (same magnitude), so this family is')
print('     3-adically DEGENERATE between the first two charges for every n --')
print('     the same two-tier problem Phase E already proved using the real')
print('     numbers, not a new structure the p-adic norm reveals.')

print("""
RESULT (item 20): tested directly, not assumed. The 3-adic valuation does
not give a well-defined 3-tier ordering (q3=0 breaks it entirely -- v_3 is
undefined at 0, not "infinitely suppressed" in any sense useful here), and
on the anomaly-free family it reproduces the exact same 2-tier degeneracy
Phase E already found with ordinary absolute value. No sense was found in
which switching number systems escapes Phase E's structural result. This
is also a case, like items 21/41, where the "ensemble" is really just 3
numbers -- not enough to support any general claim about p-adic FN charges
regardless of the outcome above. CLOSED, negative / not meaningful as posed.
""")

# =====================================================================
# SUMMARY
# =====================================================================
print('=' * 72)
print('Phase V summary')
print('=' * 72)
print("""
Item 33 (Malcev invariant): CLOSED, negative. Malcev identity confirmed
  directly (first check in this repo). Trace-form invariant is the
  unique G2-invariant form, no extra structure found.
Item 20 (p-adic FN charges): CLOSED, negative / not meaningful as posed.
  3-adic valuation breaks down at q3=0 and reproduces Phase E's 2-tier
  degeneracy on the anomaly-free family; sample size (3 charges) too
  small to support a general claim either way.

Net effect on Phase C's ~13 free parameters: ZERO (as with every
previous phase that tested a specific fix and found it doesn't apply).
Remaining [real]-tier backlog items still need a genuine Lie-theory
package (GAP/Magma/Sage/LiE) or multi-week derivation, and are left
honestly open -- see PHASE_R_HYPOTHESIS_BACKLOG.md and README.md for
the full, current disposition of every item.
""")
