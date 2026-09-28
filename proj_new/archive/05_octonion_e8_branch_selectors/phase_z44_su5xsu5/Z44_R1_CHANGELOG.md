# Z44 — Revision 1 (Z44-R1) Change Log

**Type: documentation correction + adversarial audit revision only.**
No phase was rerun. No new mechanism was searched. No O3 work was
done. Tasks 1–5's original scripts and outputs are untouched; this
revision adds one new script (`scripts/z44_audit_commutant_recheck.py`)
and updates the surrounding documentation to reflect what it found.

## Trigger

A follow-up adversarial audit on Task 4 identified that Z44's headline
quantitative claim — "commutant 200, therefore 200x worse than Z21's
1" — compared two setups that don't match: Z21's SU(3)_f is gauged;
Z44's SU(5)_B (as originally scoped) was left ungauged. Both the
spectral-gap check on the original 200 and the equal-footing
recomputation were independently re-run before any document was
changed.

## Corrected claims

1. **"200x worse than Z21" → retracted.** The equal-footing comparison
   (SU(5)_B also gauged, matching Z21's assumption) gives commutant =
   2, not 200. Z44 is 2x worse than Z21, not 200x.
2. Every place this ratio appeared as an unqualified headline number —
   `README.md` (twice), `interpretation.md`, `audit_report.md`,
   `results.json`, `scripts/results_z44_freedom_count.json`,
   `scripts/results_z44_comparison.json` — has been updated to state
   both numbers (200 for the ungauged scope as originally asked for;
   2 for the fair comparison) and to explain which question each one
   answers.

## Unchanged claims (re-verified against the correction, not assumed)

- SU(5)_A x SU(5)_B is a bare tensor product (Levi-type), not a
  plethysm — Task 3's result and the definitional argument behind it
  are untouched by a commutant-counting correction.
- No natural 3-dimensional substructure exists in the untouched
  SU(5)_B block (5- or 10-dimensional) — true at both commutant values.
- Rule 1 violation stands — extracting "3 generations" still requires
  an external, unmotivated projection, at either commutant value.
- Overall verdict: **CLOSED, negative, L1.** Unchanged.

## Strengthened claims

- None. This correction reduces the size of the quantitative gap
  between Z44 and Z21 (2x instead of 200x); it does not strengthen any
  claim in either direction. Flagging this explicitly because a
  correction that *only* subtracts overstatement, with nothing added
  back, is the expected and healthy outcome here — there was no
  compensating strengthening to report.

## Mathematical basis for the correction (summary; full derivation in `interpretation.md`)

The 200 → 2 shift is Schur's Lemma, applied to both factors instead of
one. SU(5)_A broken to the SM splits the 5_A factor into two
inequivalent irreps (dim 3, dim 2). Gauging SU(5)_B makes the 10bar_B
factor a single irreducible representation. The commutant of the
combined action is then forced, by Schur, to be one scalar per
SM-irreducible piece: 1 + 1 = 2. Leaving SU(5)_B ungauged instead
replaces that forced collapse with the full unconstrained endomorphism
algebra of the 10-dimensional block (dimension 100), giving 2 x 100 =
200. Same lemma Z21 already used; applied here to the factor Z44's
original scope had left out.

## Freeze / handoff document

`PROJECT_STATE_HANDOFF.md` was checked and contains no reference to
Z44 (consistent with Z44's own original disposition: "no update...
warranted" for a confirmed-negative, non-new-result phase). No change
was needed there, and none was made.

## Files touched in this revision

- `README.md` — commutant summary line, headline-result paragraph
- `interpretation.md` — freedom-count section rewritten with the
  correction and the Schur's-Lemma derivation
- `audit_report.md` — new "Z44-R1: post-closure correction" section,
  including the required re-verification of every surviving conclusion
- `methodology.md` — new "Z44-R1 addendum" noting the added script
- `results.json` — `z44_R1_correction` fields added under
  `z44_freedom_count` and `z44_comparison`
- `scripts/results_z44_freedom_count.json` — `z44_R1_correction` field added
- `scripts/results_z44_comparison.json` — `z44_R1_correction` field added
- `scripts/z44_audit_commutant_recheck.py` — new (the audit script itself)
- `scripts/results_z44_audit_commutant_recheck.json` — new (its output)
- `Z44_R1_CHANGELOG.md` — this file, new
