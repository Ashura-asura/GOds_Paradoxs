# RESULT: Phase Y — Hodge-star self-duality split (2026-07-28)

**Task context:** POST_AUDIT_RESEARCH_PHASE_PROMPT, Task 6, Priority 2
("Invariant multiplicity completion — complete Phase X").

**What was attempted:** Phase X's own text flagged one concrete, well-
defined open item — the 10-vs-126 split within Sym^2(16) was correct by
dimension count (136 = 10+126) but only L2 (cited from the literature),
because the naive "subtract the 10's weight table" test could not rule
out that the 10's weight points were shared with part of the 126 (they
are — the raw multiplicity at (1,0,0,0,0) is >1 before subtraction).

**What was done:** built the 126's own weight table independently, from
the abstract definition (self-dual half of Lambda^5(vector-10) under the
Hodge star), using a from-scratch numerical linear-algebra construction
(Plücker coordinates for the change of basis, a purely combinatorial
Hodge star on the real coordinate basis, transported into the weight
basis, block-diagonalized per weight). See
`phases/phase_y_hodge_star_self_duality.py` for the full, runnable
computation and inline documentation.

**Result:** the self-dual (+i eigenvalue) half of Lambda^5(vector-10)
matches Phase X's residual (Sym^2(16) minus the vector-10's weight
table) exactly, weight-by-weight, dimension 126 on both sides. The
anti-self-dual (-i) half does not match (as expected — only one
chirality of 126 couples to a given chirality of 16). All internal
consistency checks (Hodge star squares to -1, no leakage between weight
blocks, eigenvalues exactly ±i) hold to floating-point machine precision
(~1e-15).

**Status:** L1, per the same "two independent constructions agree
exactly" bar Phase X already used for the 120 piece — with the honest
caveat that this is a *numerical* (NumPy) computation, not a symbolic
one; the precision achieved is far below any threshold that could flip
an integer multiplicity, but a symbolic/exact-arithmetic rerun is the
natural hardening step if bulletproof certainty is ever required.

**Effect on the project's conclusions: none.** This closes a
documentation gap (a claim that was correct but only cited, not
independently derived), not a physics gap. Per Rule 9, applied
explicitly: this mechanism answers "which SO(10) irrep is which," not
"what selects a specific point in the remaining 6- or 3-dimensional
Yukawa freedom." It does not reduce the free-parameter count and was
never expected to — see `docs/POST_AUDIT_TARGET.md` for why Priority 2
was scoped, from the start, as a completeness check rather than a
parameter-reduction mechanism.
