# Z44 Audit Report

## Rule 4 (adversarial audit always on) -- bugs caught during this phase

Two bugs were caught during the O2 filter script (prior phase, same
session) before they contaminated the O2 conclusions:

1. The "single-factor" branch label for SO(16)/SU(9) accidentally
   contained the literal substring "bifundamental" inside the phrase
   "no second group to be bifundamental with," which caused a naive
   `"bifundamental" in kind_string` check to false-positive. Fixed by
   rewording the label and switching the check to `str.startswith`.
2. The SU(5)xSU(5) branching's free-text note argued the construction
   was "structurally distinct from both Z6-Z42 and Z43" -- but a naive
   duplicate-detector that searched note text for the literal strings
   "Z6-Z42" / "Z43" flagged it as a duplicate anyway, because the note
   *names* those phases while arguing against duplication. Fixed by
   replacing text-parsing with an explicit boolean `duplicate` field
   set per-branching, not inferred from prose.

Both are documented here and in the O2 script's git-equivalent history
(inline comments at the fix sites) per Rule 4's requirement that
caught errors stay in the audit trail rather than being silently
corrected.

One additional bug was caught and fixed within Z44 itself: the initial
commutant solver (`z44_freedom_count.py`) hardcoded the base
representation dimension as 5 inside `commutant_dimension()`, which
silently broke the Z21 cross-check (that case's generators are 3x3,
not 5x5) with a shape-mismatch error rather than a silent wrong
answer -- caught immediately because the cross-check step existed at
all. Fixed by deriving `base_dim` from `gens[0].shape[0]`. This is a
concrete example of why Task 4's brief (cross-check the solver against
Z21's known answer before trusting it on new data) mattered: an
un-cross-checked version of this solver could plausibly have returned
a silently wrong commutant dimension for the Z44 case if the bug had
manifested as a wrong-but-plausible number instead of a hard shape
error.

## Rule 1 (no unexplained new structure / flag external inputs)

Explicit check requested in the Z44 brief (Task 5): does fixing a
generation direction require an unmotivated external choice?

**Yes, and more acutely than in Z42.** The untouched SU(5)_B family
block in every bifundamental piece is 5- or 10-dimensional, never
3-dimensional. There is no step in this construction, at the level
tested (E8 > SU(5)_AxSU(5)_B, SU(5)_A broken to the SM), where "three
generations" is a distinguished substructure -- it would have to be
imposed by hand (e.g. picking a 3-dimensional subspace of the 10bar_B
block via some further breaking, embedding, or projection not
contained in this construction). This is flagged as an immediate Rule
1 violation for any attempt to read "3 generations" off this
branching, exactly as the flavon vev direction was flagged in Z42.

## Provenance labels (Rule 3 scheme)

- E8 > SU(5)xSU(5) branching table: L2 (Slansky, cited, not
  re-derived from the E8 root system) -- consistent with how the same
  source was labeled in O2.
- SU(5) > SU(3)xSU(2)xU(1) branching table: L2 (Georgi-Glashow,
  textbook-standard, cited not re-derived from SU(5) roots).
- All dimension arithmetic on both tables: L1 (checked directly in
  code, `z44_branching.py`).
- Tensor-product-vs-plethysm structural claim: L1 (checked directly,
  `z44_structure_check.py`, not inferred from the general definitional
  argument alone, though that argument is also given and matches the
  computed result).
- Commutant dimension (200) and its Z21 cross-check (1): L1, both
  computed directly, solver bug caught and fixed before the number was
  trusted (see above).

## Z44-R1: post-closure correction (Rule 4, logged not silently fixed)

A follow-up adversarial audit pass, after this phase's initial
closure, found that Task 4's headline comparison ("commutant 200 vs.
Z21's 1, therefore 200x worse") compared two setups that differ in a
way that matters: Z21's SU(3)_f is gauged; this phase's SU(5)_B was
left ungauged. That is not a fair comparison, and the "200x" framing
in the original README/interpretation is retracted.

Two checks were run and independently re-executed before accepting
this correction:

1. **Spectral-gap check** on the original 200: confirmed clean (rank
   199 eigenvalue ~1e-15, rank 200 eigenvalue = 2.0 exactly) -- the
   original 200 is not a numerical artifact or threshold-dependent
   count.
2. **Equal-footing recomputation** (`scripts/z44_audit_commutant_recheck.py`):
   with SU(5)_B also fully gauged (24 generators added, induced action
   on Lambda^2(C^5)), the commutant is 2, matching a hand derivation
   via Schur's Lemma (see `interpretation.md` for the full argument).

**What this changes:** the quantitative claim "200x worse than Z21"
is corrected to "2x worse than Z21, under the comparison that actually
matches Z21's assumptions." The 200 figure itself is not wrong -- it
correctly answers a different, narrower question (freedom with
SU(5)_B left ungauged) than the one it was compared against.

**What this does not change:** every other Task 3/5 conclusion --
bare tensor product (not plethysm), no natural 3-dimensional
substructure in the untouched block, Rule 1 violation, overall
verdict CLOSED negative. Certified below (Z44-R1 verification pass).

**Z44-R1 verification pass -- each surviving conclusion re-checked
against the correction:**

- Tensor-product (not plethysm) result: **unaffected.** This follows
  from Task 3 (Kronecker structure) and the definitional fact about
  Levi-type maximal subalgebras, neither of which the commutant
  correction touches.
- Absence of natural 3-generation structure: **unaffected.** True at
  both commutant values (200 and 2) -- neither the 5_B nor the 10bar_B
  block is ever 3-dimensional, regardless of gauging.
- Rule 1 violation: **unaffected, if anything sharper.** Even under
  the corrected, smaller residual freedom (2), there is still no
  mechanism in this construction that picks out "3" from a 5- or
  10-dimensional space; an external projection is still required.
- Overall verdict (CLOSED, negative, L1): **unchanged.**

**Certification:** only the quantitative Z21-comparison in Task 4
required correction. No other claim in this phase changed.

## Disposition

No update to the project ZIP, handoff document, related-work file,
freeze document, or tracking files. Per this phase's own stated
criterion ("update ... if and only if a genuinely new result is
obtained"), this phase's result is a confirmation of an existing
obstruction class, not a new one -- the appropriate disposition is to
close the branch here, in this phase's own folder, and let the O2
sweep's "worth_heavy_followup" flag on this branch be understood as
resolved (negative) rather than open.
