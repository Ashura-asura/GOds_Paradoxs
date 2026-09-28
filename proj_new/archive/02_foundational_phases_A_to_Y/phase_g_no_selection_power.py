"""
Phase G: Does the Messenger-Matter Fix Have Any Selection Power? [L1, NEW]
======================================================================
Ground rules: 1-8 strictly enforced.

Phase F showed: a single vector-like (16_M, 16bar_M) messenger pair
with solved-for charges restores U(1)_F anomaly-freedom for the
FITTED charges q=(3,2,0), at the cost of a new mass scale and an
unfixed representation choice.

THIS PHASE ASKS THE OBVIOUS FOLLOW-UP, DIRECTLY (not assumed):
does that construction actually prefer or constrain q=(3,2,0) in any
way -- or would it rescue literally any candidate charge assignment
equally well? If the latter, the "fix" has zero selection power: it
can never be evidence for, or a step toward deriving, any particular
set of charges.

METHOD: for every integer FN-charge triple (q1, q2, q3) satisfying
the Phase E hierarchy requirement (3 distinct pairwise gaps, i.e. 3
distinct Yukawa suppression tiers -- the same requirement Phase E
used to rule out the anomaly-free family (n,-n,0)), solve for a single
messenger pair (x, y) using EXACTLY Phase F's algebra, generalized
from q=(3,2,0) to arbitrary q. Check how often an integer solution
exists.

This project's own convention (Phase D onward) normalizes one
generation's FN charge to 0, i.e. triples of the form (q1, q2, 0).
That convention is tested first, since it is the one actually used
to produce q=(3,2,0).
"""

import itertools
import math

print('=' * 72)
print('Phase G: Does Messenger-Matter Anomaly-Fixing Select Anything?')
print('=' * 72)


def messenger_fix_exists(q):
    """Exactly Phase F's algebra (single vector-like 16_M+16bar_M pair),
    generalized from the specific triple (3,2,0) to arbitrary integer q."""
    lin_deficit = sum(q)
    cubic_deficit = sum(qi ** 3 for qi in q)
    s = -lin_deficit
    if s == 0:
        return (cubic_deficit == 0), None
    xy = (s ** 2 - (-cubic_deficit) / s) / 3
    disc = s ** 2 - 4 * xy
    if disc < 0 or disc != round(disc):
        return False, None
    root = math.isqrt(round(disc))
    if root * root != round(disc):
        return False, None
    if not float(xy).is_integer():
        return False, None
    x, y = (s + root) / 2, (s - root) / 2
    if not (float(x).is_integer() and float(y).is_integer()):
        return False, None
    return True, (int(x), int(y))


# =====================================================================
# 1. This project's actual convention: one charge normalized to 0
# =====================================================================
print("\n--- Test 1: charges of the form (q1, q2, 0) [this project's convention] ---")
rng = range(-8, 9)
total, fixable, examples = 0, 0, []
for q1, q2 in itertools.product(rng, rng):
    qs = sorted([q1, q2, 0], reverse=True)
    if len(set(qs)) < 3:
        continue
    gaps = {abs(qs[0] - qs[1]), abs(qs[1] - qs[2]), abs(qs[0] - qs[2])}
    if len(gaps) < 3:
        continue
    total += 1
    ok, sol = messenger_fix_exists(tuple(qs))
    if ok:
        fixable += 1
        if len(examples) < 5:
            examples.append((tuple(qs), sol))

print(f"Hierarchy-compatible triples (q3=0) tested: {total}")
print(f"Fixable by a single messenger pair: {fixable}  ({fixable/total:.3f})")
print(f"Sample: {examples}")

# ALGEBRAIC EXPLANATION (why this is 100%, not a coincidence):
# With q3=0: s = -(q1+q2), and using q1^3+q2^3 = (q1+q2)(q1^2-q1q2+q2^2),
# the quantity 'xy' solved for algebraically simplifies to EXACTLY q1*q2.
# Then x,y solve t^2 + (q1+q2) t + q1 q2 = (t+q1)(t+q2) = 0, i.e.
#   (x, y) = (-q1, -q2)  -- an EXACT IDENTITY, true for every q1, q2.
print(
    "\nALGEBRAIC IDENTITY: with q3=0 the solved messenger charges are always\n"
    "exactly (x, y) = (-q1, -q2). This is not special to q=(3,2,0) -- it is\n"
    "an identity that holds for every integer (q1, q2). Phase F's 'genuine,\n"
    "verified construction' therefore verifies something that is true of\n"
    "EVERY candidate charge assignment, not a property that favors (3,2,0)."
)

# =====================================================================
# 2. Sanity check: without the zero-normalization, is it still trivial?
# =====================================================================
print("\n--- Test 2: fully general triples with NO zero charge (sanity check) ---")
rng2 = range(-6, 7)
total2, fixable2 = 0, 0
for q1, q2, q3 in itertools.product(rng2, rng2, rng2):
    qs = sorted([q1, q2, q3], reverse=True)
    if len(set(qs)) < 3 or 0 in qs:
        continue
    gaps = {abs(qs[0] - qs[1]), abs(qs[1] - qs[2]), abs(qs[0] - qs[2])}
    if len(gaps) < 3:
        continue
    total2 += 1
    ok, _ = messenger_fix_exists(tuple(qs))
    if ok:
        fixable2 += 1

print(f"Triples with NO zero charge tested: {total2}")
print(f"Fixable by single pair: {fixable2}  ({fixable2/total2:.3f})")
print(
    "Only a minority are fixable once the zero-normalization is dropped --\n"
    "confirming the 100% result above is a special consequence of always\n"
    "normalizing one charge to 0, which is exactly this project's own\n"
    "convention. In other words: the one case that matters here is the\n"
    "one with zero selection power."
)

# =====================================================================
# SUMMARY
# =====================================================================
print('\n' + '=' * 72)
print('PHASE G RESULT')
print('=' * 72)
print('''
  RESULT (L1, verified by direct computation, not assumed):
  Under this project's own charge-normalization convention, the
  single-messenger-pair anomaly fix used in Phase F works for
  literally every hierarchy-compatible FN charge triple -- 100% of
  208 triples tested, by an exact algebraic identity, not a
  coincidence tied to q=(3,2,0).

  CONSEQUENCE: the messenger-matter mechanism has ZERO selection
  power. It cannot be used to derive, favor, or even partially narrow
  down the FN charges -- it can be invoked to "rescue" any candidate
  assignment after the fact, including ones that do not match
  observation at all. This is a stronger and more decisive negative
  result than Phase F's "consistency without reduction": Phase F
  showed the fix doesn't reduce the parameter count; Phase G shows
  the fix doesn't even discriminate between candidate parameter
  values, so it cannot be a step toward deriving them either.

  WHAT WOULD ACTUALLY BE NEEDED (and is NOT supplied by this
  framework): the literature claims that a FULLER Green-Schwarz
  construction -- tying the anomalous U(1) to a genuine string-derived
  modulus/dilaton with fixed quantized couplings -- can reduce charge
  freedom to as few as 3 integers. That mechanism relies on
  string-compactification-specific data (modular weights, fixed
  normalization of the anomalous U(1) against the string coupling)
  that has no counterpart in the Cl(10)xE8 algebraic core. Importing
  it would mean grafting on a separate, unrelated string model, not
  deriving anything from this framework's own structure.

  This closes the messenger/anomaly-cancellation line of attack for
  this project: not merely "insufficient," but demonstrably without
  predictive content, tested directly rather than assumed.
''')
