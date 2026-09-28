# RESULT: Phase Y2 — exact-arithmetic hardening of Phase Y (2026-08-01)

**Task context:** Phase Y's own honest caveat, restated in `README.md`'s
Phase Y row: the Hodge-star self-duality split (126 = self-dual half of
Lambda^5(vector-10)) was proved to ~1e-15 with NumPy floating point, and
"a symbolic/exact-arithmetic rerun is the natural hardening step if
bulletproof certainty is ever required." This is that rerun. It is not
one of Phase X's "one real open problem" (the intrinsic spectral triple,
which still needs Seeley-DeWitt tooling this project doesn't have) — it
closes a smaller, precisely-scoped documentation/rigor gap that was
sitting on the open-items list.

**What was done:** `phase_y2_hodge_star_exact_symbolic.py` re-derives
Phase Y's result with every number an exact sympy `Integer`, `Rational`,
or Gaussian-rational expression — no floating point anywhere. Key
simplification (justified in the file's own docstring, not asserted):
dropping Phase Y's `1/sqrt(2)` ladder-vector normalization is exact-
arithmetic-compatible because every weight-letter basis vector is a
wedge of exactly 5 ladder vectors, so the dropped factor is the same
`(1/sqrt(2))^5` on every entry of the change-of-basis matrix `M`, and it
cancels exactly in `M @ M^{-1}`. That turns every ladder-vector
coordinate into a Gaussian integer (0, 1, i, -i), which is what makes an
*exact* 252-dimensional computation tractable at all. A second key
identity — `Lambda^5(V^{-1}) = (Lambda^5 V)^{-1}` — avoids ever inverting
a 252x252 matrix: `M` and `M^{-1}` are both built the same way (5x5
minors), from `V` and `V^{-1}` respectively, and `V^{-1}` is a trivial
exact inverse of 5 independent 2x2 blocks (sympy-computed, cross-checked
against sympy's own general 10x10 inverse).

**Result:** all 122 distinct SO(10) weights in the 252-dimensional
Lambda^5(vector-10) were diagonalized under the Hodge star exactly
(sympy symbolic `eigenvals`, no tolerance, no rounding). Every single
eigenvalue found was exactly `+I` or `-I` — not close to it, equal to
it. The resulting weight table for the `+i` (self-dual) eigenspace
matches Phase X's residual (Sym^2(16) minus one copy of the vector-10's
weight table) exactly, key by key, using sympy's exact rational
equality. The `-i` (anti-self-dual) eigenspace does *not* match the
residual — exactly the asymmetry Phase Y already found and expected
(only one chirality of 126 couples to a given chirality of 16).

**Status:** L1, now unconditionally — the "numerical, not symbolic"
caveat Phase Y carried is closed. Confirms Phase Y's finding with zero
floating-point operations anywhere in the computation.

**Effect on the project's conclusions: none**, exactly as Phase Y itself
predicted this hardening step would have. Per Rule 9: this answers
"which representation is which" (10 vs. 126 inside Sym^2(16)), not "what
selects the free parameters within it." The 6 (symmetric channel) / 3
(antisymmetric channel) complex Yukawa freedom from Phase X stands
completely unchanged. This is a rigor upgrade to an already-correct
result, not a new physics result, and Rule 1 (no numerology) is
satisfied the same way Phase X/Y already satisfied it: every weight
match here follows from a stated, checked mechanism (exact linear
algebra of an exact Hodge-star operator), not from a suggestive
coincidence.

**What this does NOT do:** it does not touch the project's actual "one
real open problem" (`audit report/OPEN_PROBLEMS_AFTER_AUDIT.md`) — the
intrinsic Cl(10)xE8 spectral triple, which needs Seeley-DeWitt
heat-kernel tooling this project has never had access to. That remains
open. It also does not revisit Item 15, Item 6, or Item 7 from that same
file's secondary-open-threads list; those still need LiE/Sage/GAP-class
tooling not present in this environment. Only the item explicitly
flagged as "no new packages needed, just more work" and already
substantially completed by Phase Y — its own stated hardening step — was
in scope here.
