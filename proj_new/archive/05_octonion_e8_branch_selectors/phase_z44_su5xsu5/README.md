# Phase Z44: E8 > SU(5)_A x SU(5)_B, tested as a hypothesis to break

**Status: CLOSED, negative, L1. Does not escape the Z6-Z42 obstruction;
quantitatively worse (larger residual freedom, no natural generation
count). No update to project-level files.**

## Why this phase exists

O2 swept the six maximal subalgebras of E8 as a cheap dimension/shape
filter and flagged SU(5)_A x SU(5)_B as "worth heavy followup" because
it has bifundamental pieces and both factors contain SU(3) candidates.
That filter is not a result -- it only tells you what's worth the
Z39-Z43-grade computation. This phase is that computation, scoped
exactly as instructed: treat SU(5)xSU(5) as a hypothesis to break, not
a conclusion already reached.

## What was actually computed (all L1 -- checked in code, not asserted)

1. `scripts/z44_branching.py` -- exact branching E8 > SU(5)_A x
   SU(5)_B (Slansky Table 24), then SU(5)_A > SU(3)xSU(2)xU(1)
   (Georgi-Glashow) applied to every piece, SU(5)_B left untouched.
   Every dimension claim verified by direct arithmetic.
2. `scripts/z44_structure_check.py` -- the load-bearing test. Builds
   the SM generators as literal Kronecker products g_A (x) I_10 on
   the (5_A,10bar_B)-type pieces and checks, to machine precision,
   whether the family block is ever touched. Result: max deviation
   from a pure Kronecker (tensor-product) structure is exactly 0.0.
   This is a direct computational answer to "plethysm or bare
   product?" -- not an assertion by analogy.
3. `scripts/z44_freedom_count.py` -- commutant dimension of the SM
   generators on the family block, same solver methodology as Z21
   (build generators, vectorize commutator, take nullspace). The
   solver was cross-checked against Z21's own known answer (commutant
   = 1 for irreducible SU(3)_f) before being trusted on the new case.
   Result for Z44 as scoped (SU(5)_B left ungauged, per this phase's
   own brief): commutant dimension 200. **[Z44-R1 correction]** This
   is not directly comparable to Z21's 1, because Z21 assumes the
   family group is already gauged. Under the fair, equal-footing
   comparison (SU(5)_B also fully gauged), the commutant is 2 — see
   `scripts/z44_audit_commutant_recheck.py` and the R1 note below.
4. `scripts/z44_comparison.py` -- direct comparison table against
   Z21, Z39, Z42, Z43, and the final verdict.

## Headline result

SU(5)_A x SU(5)_B is a product-type (Levi-type) maximal subalgebra of
E8, not a tensor (Cauchy-plethysm) embedding like Z43's SU(9) case.
Task 3 confirms this operationally: the family block is carried along
as a rigid, untouched Kronecker factor for every SM piece, to machine
precision. It is mechanism-identical in kind to E6 x SU(3)_f
(Z6-Z42), and its residual "which direction is a generation" freedom,
**as scoped in this phase (SU(5)_B left ungauged)**, is 200 complex
dimensions. **[Z44-R1 correction, see below]** Comparing that 200
directly to SU(3)_f's gauged commutant of 1 (Z21) is not a fair
comparison -- Z21's family group is gauged, this phase's SU(5)_B was
not. Under the equal-footing comparison (SU(5)_B also fully gauged),
the commutant is 2, not 200 -- still larger than Z21's 1, but by a
factor of 2, not 200. Either way, no natural "3" appears anywhere in
the untouched 10bar_B/5bar_B block. Picking three generations out of
it would need an extra, unmotivated choice -- flagged under Rule 1 in
`audit_report.md`.

**[Z44-R1, added after initial closure]** The original "200x larger"
comparison above compared SU(5)_B ungauged (this phase's setup)
against Z21's gauged SU(3)_f -- an apples-to-oranges comparison. See
`interpretation.md` and `audit_report.md` for the corrected,
equal-footing number (commutant = 2) and the mathematical reason for
the change. The qualitative verdict (product-type, non-plethysm, no
natural 3, Rule 1 violation) is unchanged.

See `interpretation.md` for the full discussion and
`audit_report.md` for the Rule 1/Rule 4 bookkeeping.
