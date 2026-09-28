# OPEN_PROBLEMS_AFTER_AUDIT.md

## Update (2026-08-01, Phase Y2): secondary thread #2 below is now closed

Phase Y (2026-07-28, not yet reflected in this file when the paragraphs
below were written) already independently derived the Phase X 10-vs-126
split at L1, numerically. Phase Y2 (`phases/phase_y2_hodge_star_exact_symbolic.py`)
reran that identical computation with exact sympy Gaussian-rational
arithmetic — zero floating point anywhere — and got the identical
result: all 122 weight blocks of Lambda^5(vector-10) diagonalize to
exactly +i/-i under the Hodge star, and the self-dual half's weight
table matches Phase X's residual exactly, key by key. **Secondary
open thread #2 below (the Phase X 10-vs-126 split) is closed, at L1,
unconditionally.** The paragraphs below predate that result and are
kept for the historical record. This does not touch the one real open
problem (the intrinsic spectral triple) or secondary threads #1, #3, #4,
which remain open for the same reasons stated below — this environment
still lacks LiE/Sage/GAP-class Lie-theory tooling.

## Update (2026-07-28, Phase Z2): the sub-question below is now closed

Phase Z2 (`docs/PHASE_Z2_EXPLICIT_SPECTRAL_TRIPLE_RESULT.md`) built Γ_F
and J_F explicitly and proved, directly on the full H_F operators, that
order-one/reality/chirality cannot relate different generation-pair
Yukawa coefficients. **dim(M_D) = 6 or 3, exactly Phase X's number — this
route is now a proved negative result, not merely an unattempted one.**
The remaining open problem is narrower than before: not "could this
axiom shape select a point," which is now answered no, but only whether
some *other*, not-yet-identified principle could. The paragraphs below
predate that result and are kept for the historical record, with this
update as the current status.

## The one real open problem (confirmed by this audit)

**Build an intrinsic Cl(10)×E8 spectral triple** — a Dirac operator
D_F, real structure J, and chirality operator, satisfying Connes'
order-one condition and the correct KO-dimension, constructed *from
Cl(10)×E8's own Witt/Clifford data* rather than borrowed from
Chamseddine–Connes–van Suijlekom's independently-built spectral
Pati-Salam model.

**Precise, falsifiable success criterion** (this audit's synthesis of
Phase X + the Item 1 addendum, not previously stated together this
explicitly anywhere in the repository): a candidate D_F succeeds only
if it picks a *specific point* in the 6-complex-parameter (symmetric
channel: H=10 or 126) or 3-complex-parameter (antisymmetric channel:
H=120) Yukawa freedom that Phase X proved is exactly what's left once
gauge symmetry has done everything it can — through a mechanism
independently justified on grounds other than "it reproduces the
known answer." If it only relocates that same freedom under a new
name (the way the messenger fix and the Dirac-root-coupling addendum
both did), it fails Rule 9 regardless of how sophisticated the
construction looks.

**What's missing to attempt it:** genuine noncommutative-geometry
tooling (Seeley-DeWitt heat-kernel expansion machinery), which this
project has never had access to. numpy/sympy are not sufficient for
the a4 coefficient calculation Item 1 requires.

## Secondary, smaller open threads (not the main prize, but genuinely
unresolved and worth naming)

1. **Item 15's narrower sub-question** — the SO(10)-126 content after
   branching each E6 summand of the full 27⊗27⊗27 decomposition —
   remains open pending LiE/Sage-class branching tools (confirmed
   still open; not contradicted by anything found in this audit).

2. ~~**The Phase X 10-vs-126 split**~~ — **CLOSED (2026-08-01, Phase Y2,
   see update note at the top of this file).** The internal
   decomposition of the symmetric channel of 16⊗16 into 10+126, closed
   at L1: independently derived by weight-table comparison the way the
   120 piece was (Phase Y, numerically; Phase Y2, exactly and
   symbolically), resolving the Hodge-star convention on Λ⁵(vector) as
   this file originally called for. No longer cited from Slansky alone.

3. **Item 6's precisely-scoped next step**: Gresnigt's Cl(8)/S3
   mechanism (independently code-verified in this audit, real paper,
   real match — see `COMPLETE_AUDIT_REPORT.md` Phase 2/3) depends on
   sedenion-automorphism-derived multivectors that Phase A1's own
   concrete Cl(10) construction does not currently carry. Importing
   that structure into Phase A1's own basis — not just citing that it
   exists elsewhere — is now precisely identified (per the README
   addendum, confirmed accurate by this audit) rather than a vague
   "compare to literature" item.

4. ~~**Item 7's cohomology result needs actual re-verification**~~ —
   **CLOSED (2026-08-01, `session_new_files/item7_reverification_no_gap.py`
   + `ITEM7_LHS_SPECTRAL_SEQUENCE.md`).** Independently re-derived
   H_1..H_4(S3;Z), with zero GAP/HAP dependency, via a
   Lyndon-Hochschild-Serre spectral sequence with every group-theoretic
   input checked by code rather than assumed. Reproduces the numbers
   exactly. The original `.py` file's genuine `SyntaxError` (found by
   this same pass) is also fixed. No longer "plausible, not yet
   independently reproduced" — now independently reproduced, by a
   different method than GAP/HAP.

## What does NOT qualify as an open problem worth pursuing further

Per the Rule 9 audit (`COMPLETE_AUDIT_REPORT.md` Phase 6), the
following are closed, not open, and re-attempting them without a
genuinely new idea or new tooling would not be progress:

- Anomaly cancellation / messenger matter / Green-Schwarz as routes to
  fixing FN charges (zero selection power, proven, not just untested).
- Any of the alternative E8 branching chains (SO(16)×SU(4), E7×SU(2))
  as routes to a *better* generation/flavor structure — both checked
  and both cost more parameters than they save.
- RG fixed-point counting (item 42) as currently scoped — a real
  version would need actual beta functions, which is a much bigger
  undertaking than "count the operators," and the counting itself
  already shows no obvious small fixed set to look for.
- p-adic FN charges, Malcev-algebra Casimirs, McKay-quiver labelings,
  E8-lattice theta functions, causal-set volume matching, E9/E10
  billiards — all closed negative, all independently re-confirmed
  where code existed, and none showed any sign of being "almost
  there" rather than genuinely dead ends.

## Honest overall statement

This is, after this audit, still what the repository's own
`solution.md` already called it: a real, partial, honestly-bounded
derivation of the Standard Model's *qualitative* structure (gauge
group, charge quantization, a generation count that is real but
chain-dependent, and a forced-to-trivial CKM/PMNS in the minimal
model), with a precisely located and well-motivated — but genuinely
unsolved, and not solvable with this project's current tools — gap
between that structure and the 19-or-23 numerical parameters of the
actual Standard Model. Nothing in this audit found a shortcut across
that gap, and nothing in this audit found the gap to be smaller or
larger than the project already, honestly, said it was.
