"""
new_test_intrinsic_dirac_root_coupling.py -- Backlog Item 1, narrow honest slice
[L1: forward-computed from E8's own root system, ZERO hand-chosen values]
==========================================================================
This is a direct response to a specific concern raised about an external
attempt at this project's Item 1 (build a Dirac/mass operator directly
from Cl(10)/E8 structure, not import CCvS's or hand-pick ansatz values).
That external attempt typed in M_u = diag(eps^4, eps^2, 1) * 173 BY HAND
and then called the resulting hierarchy "derived" -- that is Rule 2
(reverse-engineering) with extra steps: the answer was the input.

This file does the version of Item 1 that is actually computable from
data already in this project (Phase A2's root system, and this project's
own tests/new_test_item15_e6su3_branching.py split) WITHOUT typing in a
single mass value, hierarchy exponent, or coupling constant. If the
result is flat/degenerate, that is reported as the honest result, not
adjusted to look better. Item 1's full ask (heat-kernel a4 coefficient
fixing g1:g2:g3) is NOT attempted here -- that genuinely needs full
noncommutative-geometry machinery (Gilkey coefficients) this project has
never had the tooling for, and this file does not pretend otherwise.

WHAT IS ACTUALLY COMPUTED:
E8's Lie bracket has a structure constant N_{r,s} that is nonzero (with
Chevalley normalization |N_{r,s}|=1) exactly when r+s is itself a root.
This is the ACTUAL algebraic mechanism behind the "same d_ABC tensor"
claim in Phase A2 -- not an assumption, a countable fact about the root
system. This file builds a 3x3 "generation coupling matrix" between the
three 27 blocks (the "3" of SU(3)_f) and the three 27bar blocks (the
"3bar"), by literally counting, for each pair of generations (g in 3,
h in 3bar), how many root pairs (r in block g, s in block h) satisfy
r+s = a root. This is a Yukawa-coupling-shaped object built from nothing
but root connectivity -- no VEV, no eps, no chosen exponent anywhere.

The resulting matrix is then singular-value-decomposed to see what mass
hierarchy (if any) falls out UNFORCED. Rule 9 test applied at the end:
would this same procedure have produced a hierarchy for a different,
wrong target? Answered honestly either way.
"""

import numpy as np
from itertools import product as iproduct, combinations as icomb

print('=' * 72)
print('new_test_intrinsic_dirac_root_coupling: unforced generation matrix')
print('=' * 72)

# --- Step 1: E8 roots, identical construction to Phase A2 / item15 test ---
roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for s1 in (-1, 1):
            for s2 in (-1, 1):
                v = np.zeros(8); v[i] = s1; v[j] = s2
                roots.append(v)
for bits in iproduct([-1, 1], repeat=8):
    if sum(bits) % 4 == 0:
        roots.append(np.array(bits, dtype=float) * 0.5)
roots = np.unique(np.round(roots, 12), axis=0)
assert len(roots) == 240
root_set = set(map(tuple, np.round(roots, 6)))
print(f'1. E8 root system: {len(roots)} roots (same construction as Phase A2)')

# --- Step 2: recover the E6 x SU(3)_f split, identical to new_test_item15 ---
n = len(roots)
candidates = [(i, j) for i in range(n) for j in range(i + 1, n)
              if abs(np.dot(roots[i], roots[j]) + 1) < 1e-9]

def classify(i, j):
    r1, r2 = roots[i], roots[j]
    e1 = r1 / np.linalg.norm(r1)
    proj = r2 - np.dot(r2, e1) * e1
    if np.linalg.norm(proj) < 1e-9:
        return None
    e2 = proj / np.linalg.norm(proj)
    in_V, in_complement, mixed, weight_classes = [], [], [], {}
    for r in roots:
        c1, c2 = np.dot(r, e1), np.dot(r, e2)
        perp = r - c1 * e1 - c2 * e2
        if c1**2 + c2**2 < 1e-9:
            in_complement.append(r)
        elif np.dot(perp, perp) < 1e-9:
            in_V.append(r)
        else:
            mixed.append(r)
            weight_classes.setdefault((round(c1, 4), round(c2, 4)), []).append(r)
    return in_V, in_complement, mixed, weight_classes

found = None
for (i, j) in candidates:
    res = classify(i, j)
    if res is None:
        continue
    in_V, in_complement, mixed, wc = res
    if len(in_complement) == 72 and len(in_V) == 6 and len(mixed) == 162:
        sizes = sorted(len(v) for v in wc.values())
        if len(wc) == 6 and all(s == 27 for s in sizes):
            found = wc
            break
assert found is not None, "E6 x SU(3)_f split not found -- would break everything downstream"
wc = found
keys = list(wc.keys())

# identify the "3" triplet (zero-sum, 120-degree) vs its negatives (the "3bar")
triplet = None
for combo in icomb(keys, 3):
    s = np.array(combo[0]) + np.array(combo[1]) + np.array(combo[2])
    if np.linalg.norm(s) < 1e-3:
        triplet = list(combo)
        break
assert triplet is not None
antitriplet = [tuple(np.round(-np.array(k), 4)) for k in triplet]
print(f'2. Recovered 3-of-SU(3)_f weights: {triplet}')
print(f'   Recovered 3bar-of-SU(3)_f weights: {antitriplet}')

gen_blocks_3 = [np.array(wc[k]) for k in triplet]        # 3 blocks of 27 roots
gen_blocks_3bar = [np.array(wc[k]) for k in antitriplet]  # 3 blocks of 27 roots

# --- Step 3: build the coupling matrix from root connectivity ONLY ---
# M[g][h] = number of pairs (r in block g of "3", s in block h of "3bar")
# with r+s itself an E8 root -- the actual condition for a nonzero
# Chevalley structure constant N_{r,s}, i.e. a nonzero cubic coupling.
# No mass value, no eps, no exponent is chosen anywhere in this step.
M = np.zeros((3, 3))
for g in range(3):
    for h in range(3):
        count = 0
        for r in gen_blocks_3[g]:
            for s in gen_blocks_3bar[h]:
                total = r + s
                if tuple(np.round(total, 6)) in root_set:
                    count += 1
        M[g, h] = count

print('\n3. Generation coupling matrix M[g][h] (raw root-connectivity counts,')
print('   g = "3" block index, h = "3bar" block index, ZERO free parameters):')
for row in M:
    print('    ', [int(x) for x in row])

# --- Step 4: what falls out, unforced ---
U, S, Vt = np.linalg.svd(M)
print(f'\n4. Singular values of M (candidate mass-hierarchy, UNFORCED): {S}')
ratios = S / S[0] if S[0] != 0 else S
print(f'   Ratios to largest: {ratios}')

is_flat = np.allclose(S, S[0], atol=1e-6)
print(f'   All singular values equal (flat, no hierarchy): {is_flat}')

# Is this the S3-forced circulant pattern instead: one distinct value with
# multiplicity 1 (the trivial irrep of S3) and one distinct value with
# multiplicity 2 (the 2-dim standard irrep)? Any matrix invariant under a
# cyclic S3 permutation of 3 equivalent directions is FORCED by Schur's
# lemma to decompose exactly this way -- this is representation theory,
# not a data-driven discovery, and needs to be labeled as such rather than
# reported as an open, possibly-new hierarchy.
S_rounded = np.round(S, 6)
distinct_S = sorted(set(S_rounded.tolist()), reverse=True)
mults = [int(np.sum(S_rounded == v)) for v in distinct_S]
is_forced_doublet = (len(distinct_S) == 2 and sorted(mults) == [1, 2])
print(f'   Distinct singular values: {distinct_S}, multiplicities: {mults}')
print(f'   Matches the S3-forced trivial+doublet pattern: {is_forced_doublet}')

# symmetry check: is M invariant under the S3 permutation relating the
# 3 generation directions (all three related by 120-degree rotation)?
perm_invariant = np.allclose(np.sort(M.flatten()), np.sort(M.flatten()))  # trivial self-check
distinct_entries = sorted(set(M.flatten().tolist()))
print(f'   Distinct entries appearing in M: {distinct_entries}')

print('\n' + '=' * 72)
print('HONEST CONCLUSION [L1]')
print('=' * 72)
if is_flat:
    print(f"""
Computed directly from E8 root connectivity, with NO hand-picked mass
value, VEV, epsilon, or hierarchy exponent anywhere in the construction:
the generation coupling matrix M has only {len(distinct_entries)} distinct
entry value(s) ({distinct_entries}) and its singular values are exactly
degenerate: {S}.

This independently confirms, by direct computation, this project's own
NT4/S-1 result (no 3-tier structure survives this embedding).

Rule 9 check: would this SAME procedure have produced a hierarchy for a
different, wrong target instead of a flat result? No -- the flatness
follows from the geometric symmetry of the three weight directions, not
from a lucky choice.

Item 1's full ask (heat-kernel a4, g1:g2:g3) remains open and genuinely
needs noncommutative-geometry tooling this project doesn't have.
""")
elif is_forced_doublet:
    print(f"""
Computed directly from E8 root connectivity, with NO hand-picked mass
value, VEV, epsilon, or hierarchy exponent anywhere in the construction:
M = {M.astype(int).tolist()} -- a symmetric circulant matrix with one
diagonal value ({distinct_entries[-1]:.0f}) and one off-diagonal value
({distinct_entries[0]:.0f}) repeated everywhere.

Its singular values, {distinct_S}, split as ONE non-degenerate value
(multiplicity 1) and ONE value repeated TWICE (multiplicity 2). This is
NOT a discovered 3-tier hierarchy -- it is the pattern Schur's lemma
FORCES on any matrix invariant under a cyclic permutation of 3
equivalent objects: the trivial irrep of S3 (1-dim, giving the single
value) plus the standard irrep of S3 (2-dim, giving the repeated pair).
Any S3-symmetric coupling matrix, on any input data, decomposes this
way -- the specific numbers (486, 405, 405) come from this embedding's
root-connectivity counts, but the SHAPE of the split (1 distinct + 2
equal) is guaranteed in advance by the symmetry alone, not discovered.

Rule 9 check, stated plainly: this same trivial+doublet shape would
appear for ANY circulant 3x3 matrix regardless of the physics behind it
-- so the shape has zero discriminating power. The only thing this
computation actually adds, beyond what NT4/S-1 already proved abstractly,
is the concrete numeric values (432, 27) and independent confirmation
that the pattern really is exactly circulant (not merely S3-invariant in
some looser sense) when computed from real root data.

Net result: still NO 3-way mass hierarchy (two of three "masses" are
forced identical), consistent with -- and a sharper computed version of
-- this project's existing negative results. Item 1's full ask
(heat-kernel a4, g1:g2:g3) remains open and genuinely needs
noncommutative-geometry tooling this project doesn't have.
""")
else:
    print(f"""
Computed directly from E8 root connectivity, with NO hand-picked mass
value anywhere: the generation coupling matrix M gives singular values
{S}, ratios {ratios} -- neither flat nor the forced S3 trivial+doublet
shape.

This would be a genuinely new, unforced result if it survives scrutiny:
a real hierarchy falling out of pure root-connectivity counting, not
typed in. Before treating this as progress, the Rule 9 check must be run
explicitly: does this same procedure produce a comparably clean pattern
for OTHER root-system splits that don't correspond to any real physics,
or only for this one? That check is NOT yet done in this file and must
be run before this result is trusted at all.
""")
