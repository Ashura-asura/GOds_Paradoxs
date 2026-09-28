# Item 1 / R1 — Intrinsic Cl(10) spectral triple (heat-kernel a4 → g1:g2:g3)

## Result: NOT ATTEMPTED, explicitly scoped BLOCKED — needs real NCG tooling

This is the project's own headline open question (`docs/solution.md`,
closing section), and this session's honest assessment is that it should
stay open rather than get a manufactured attempt.

**What the item actually requires:** a genuine noncommutative-geometry
(Chamseddine-Connes spectral-action) construction — not just a Dirac-like
matrix, but a full finite spectral triple (A, H, D_F) satisfying Connes'
axioms (order-one condition, KO-dimension, a real structure J, first-order
condition on D_F), built from Cl(10)'s own Witt-pair data rather than
imported from CCvS. The heat-kernel coefficient a4 that would fix
g1:g2:g3 is a Seeley-DeWitt asymptotic expansion coefficient of the full
(finite ⊗ continuum) Dirac operator — a substantial computation even with
the right machinery, and one this project has never attempted from
scratch.

**Why this session did not attempt it:** the available tooling is numpy/
sympy only (no GAP/HAP for this particular item — GAP doesn't do
spectral geometry either — and no dedicated NCG package such as the
`NCAlgebra`/`Mathematica NCG` toolchains researchers in this area
actually use). Building a candidate D_F and computing a4 by hand risks
exactly the failure mode Phase V flagged for item 15 before real tooling
existed: producing unverified arithmetic dressed up as a computed result.
Rule 2 (no reverse-engineering) and Rule 9 (discriminating power) both
argue against a hand-built D_F tuned, even unconsciously, to land near
the known g1:g2:g3 ratios.

**What a real attempt would need, concretely** (left as the actual next
step, not done here):
1. A finite Hilbert space built from Phase A1's 32-dim Fock space (or a
   chirally-doubled version of it) with a genuine real structure J and
   grading gamma, checked against Connes' table of KO-dimensions — this
   alone is nontrivial and has not been done in this project.
2. A candidate D_F (the "finite Dirac operator," analogous to CCvS's
   Yukawa-coupling matrix) built ONLY from Cl(10)'s own algebraic data
   (no imported CCvS coefficients) — this is exactly the "6-or-3 free
   Yukawa parameters" Phase X located; any D_F that fixes a specific
   point in that space needs an independent justification for why THAT
   point, not a nearby one (Rule 9).
3. The actual Seeley-DeWitt a4 coefficient computation for the resulting
   operator, which requires symbolic heat-kernel machinery this project
   does not have.

**Rule 9 pass/fail test, restated for whenever this is attempted (per
solution.md's own framing):** does the resulting D_F pick a specific
point inside Phase X's 6- (or 3-) dimensional invariant space through an
independently-justified mechanism, or does it just relocate the same
free parameters into a differently-named coefficient — the way Phase F's
messenger fix and the existing `new_test_intrinsic_dirac_root_coupling.py`
addendum both ended up doing? Any future attempt should be checked
against this before being written up as a result.

## Net impact

None — this is a scoping statement, not a result. Recorded per Rule 5
(document what wasn't done, not just what was) so a future session with
real NCG tooling knows exactly what's missing rather than re-discovering
it.
