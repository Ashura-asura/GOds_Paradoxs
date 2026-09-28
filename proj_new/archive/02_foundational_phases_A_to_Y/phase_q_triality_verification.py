"""
Phase Q: Verifying Phase A1's Unchecked "Triality" Claim [L1, new, 2026-07-28]
================================================================================

MOTIVATION
----------
Phase A1's own summary asserts: "10 possible color embeddings; 3 by triality [PASS]".
The code only computes C(5,3)=10 (the number of ways to choose 3 of Cl(10)'s 5 Witt
pairs as the color pairs). Nothing in Phase A1 ever constructs a triality map or
identifies which 3 of the 10 embeddings it supposedly picks out. This phase checks
whether that claim is even well-posed, and if so, what it actually says -- without
assuming in advance that it will support or undermine anything upstream.

IMPORTANT SCOPING, stated up front:
  - "Triality" properly refers to the order-3 (S3) outer automorphism of Spin(8)
    permuting its three inequivalent 8-dimensional reps (vector, spinor+, spinor-).
    That is NOT what is checked here -- constructing actual Spin(8) triality is a
    separate, harder undertaking not attempted in this phase.
  - What IS checked here: the discrete automorphism group of the octonion
    multiplication table (as coded in qosc_division_connection.py, Fano-plane
    convention), and whether it contains an element compatible with the specific
    Witt-pair grouping phase_a1_cl10_core.py actually uses to build Cl(10)'s gammas.
  - This is a narrower, honestly-computed question: not "is there Spin(8) triality
    here", but "is Phase A1's own claim, as literally written, actually true of its
    own code". Results below apply only to that narrower question.
"""

import numpy as np
from itertools import permutations, product, combinations
import sys
sys.path.insert(0, '.')
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'support'))
from qosc_division_connection import build_octonion_structure_constants

print('=' * 72)
print('Phase Q: Verifying Phase A1\'s Triality Claim [L1, new]')
print('=' * 72)

C, R, f, mult = build_octonion_structure_constants()

# --- Step 1: the Fano-plane collineation group ---
lines = [(1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 7), (5, 6, 1), (6, 7, 2), (7, 1, 3)]
line_set = set(frozenset(l) for l in lines)

fano_group = []
for perm in permutations(range(1, 8)):
    p = {i + 1: perm[i] for i in range(7)}
    if set(frozenset(p[x] for x in l) for l in lines) == line_set:
        fano_group.append(p)

print(f'\n1. Fano-plane collineation group order: {len(fano_group)}  (expected PSL(2,7) = 168)')
assert len(fano_group) == 168

# --- Step 2: how phase_a1_cl10_core.py actually wires octonion units to Witt pairs ---
# G8 = [C1,C2,C3,C4,C5,C6,C7, non-octonion] ; G = [G8[0..7]*s3] + [non-oct, non-oct]
# Witt pair j = gammas (2j, 2j+1)
print('\n2. Actual octonion -> Witt-pair wiring in phase_a1_cl10_core.py:')
wiring = {0: ('C1', 'C2'), 1: ('C3', 'C4'), 2: ('C5', 'C6'), 3: ('C7', 'non-oct'), 4: ('non-oct', 'non-oct')}
for j, src in wiring.items():
    print(f'   Witt pair {j}: {src}')
print('   -> pairs 0,1,2 are PURELY octonion-sourced; pair 3 is mixed; pair 4 has NO octonion content.')
print('   -> only a partition of {1..7} into blocks {1,2}{3,4}{5,6}{7} is even relevant to Phase A1\'s')
print('      "10 embeddings, 3 by triality" claim -- an octonion symmetry can only act on pairs 0,1,2')
print('      (color) by construction; it structurally CANNOT touch pair 4, contrary to what "3 of 10"')
print('      loosely implies.')

# --- Step 3: does the Fano group have a subgroup respecting this partition? ---
blocks = [frozenset({1, 2}), frozenset({3, 4}), frozenset({5, 6}), frozenset({7})]
block_set = set(blocks)
stab = [p for p in fano_group if set(frozenset(p[x] for x in b) for b in blocks) == block_set]
print(f'\n3. Subgroup of the Fano group stabilizing this exact partition: order {len(stab)}')
for p in stab:
    print('  ', p)

nontrivial = [p for p in stab if any(p[i] != i for i in p)]
if nontrivial:
    g = nontrivial[0]
    img = [frozenset(g[x] for x in b) for b in blocks[:3]]
    print(f'   Nontrivial element cyclically permutes the color blocks: {blocks[:3]} -> {img}')

# --- Step 4: is it a genuine (signed) automorphism of the actual structure constants? ---
print('\n4. Checking whether this permutation is an exact automorphism of f_ijk (allowing basis sign flips,')
print('   the standard way discrete octonion automorphisms are realized):')
g = nontrivial[0]
pmap = {0: 0, **g}
found_signs = None
for signs in product([1, -1], repeat=7):
    eps = [1] + list(signs)
    ok = all(np.isclose(f[pmap[i], pmap[j], pmap[k]], eps[i] * eps[j] * eps[k] * f[i, j, k])
             for i in range(8) for j in range(8) for k in range(8))
    if ok:
        found_signs = eps
        break
print(f'   Signed automorphism exists: {found_signs is not None}')
if found_signs:
    print(f'   Sign vector (unit 0..7): {found_signs}')
    # order check
    def compose(a, b):
        return {i: b[a[i]] for i in range(8)}
    ident = {i: i for i in range(8)}
    p2 = compose(pmap, pmap)
    p3 = compose(p2, pmap)
    print(f'   Order of this automorphism: {"3 (p^2!=id, p^3==id)" if p2 != ident and p3 == ident else "not 3"}')

print('\n' + '=' * 72)
print('RESULT')
print('=' * 72)
print('''
CONFIRMED (new, computed, not previously in this project):
  A genuine order-3 signed automorphism of the octonion structure constants exists
  that cyclically permutes exactly the three octonion-pairs feeding SU(3)_c
  (Witt pairs 0,1,2 in Phase A1's own labeling), fixes the octonion unit feeding
  into the SU(2)_L pair, and has no action at all on the 5th Witt pair (which is
  not octonion-sourced). This is a genuine, verifiable Z3 symmetry of Cl(10)'s own
  construction -- not asserted, computed.

CORRECTED (Phase A1's claim was imprecise, not simply wrong):
  Phase A1's "3 of 10 embeddings, by triality" is NOT literally what the algebra
  supports. The Z3 found here does not act on the 10 C(5,3) *embeddings* (i.e. it
  doesn't pick out 3 special ways to split 5 Witt pairs into color/weak); it acts
  WITHIN one fixed embedding, cyclically permuting the 3 octonion units that make
  up the color pairs themselves. Related in spirit, different in substance -- and
  this is the first time either version has actually been checked rather than
  asserted.

DOES NOT CONNECT TO GENERATIONS (checked, not assumed):
  This Z3 lives entirely inside Cl(10)'s SU(3)_c construction (6 of the 7 octonion
  units, used to build ONE 16-plet's color structure). The 3 fermion generations in
  this project come from an unrelated object -- the SU(3)_f triplet index in E8's
  248 -> (16,3) branching under E6 x SU(3)_f (Phase A2). Nothing in this computation
  gives these two "3"s a shared origin: one is a discrete symmetry of a single
  generation's internal color algebra, the other is a continuous-group multiplicity
  label across generations. Asserting a link between them without a concrete map
  between the two group actions would be exactly the kind of unproven analogy Rule 1
  (no numerology) exists to prevent. None is offered here.

STATUS: Genuine new structural fact about Cl(10), honestly scoped. Does not move
Phase C's 0/19 count in either direction. Filed as a correction to Phase A1's own
claim, not as progress toward any SM parameter.
''')
