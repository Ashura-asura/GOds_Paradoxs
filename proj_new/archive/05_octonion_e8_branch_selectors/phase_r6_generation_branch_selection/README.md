# Phase R6: Generation Branch Selection Audit

# Phase R6: Generation Branch Selection Audit

**[R6-R1 correction, added during R7]: this phase overclaimed that
SU(9), E7xSU(2), and F4xG2 were "already tested" branches. They are
not -- no dedicated branch computation for any of the three exists in
this repo, and the F4xG2 attribution (to `phase_z39_e8_cubic_
obstruction`) was a misreading of what that phase actually tests (the
Schur/cubic-Casimir obstruction inside the already-adopted
E6xSU(3)_f branch, not an alternative branching). See
`phase_r7_octonionic_realization_selector/README.md` for the full
correction. This does not change R6's verdict (2, chosen not forced)
-- it was already supported by the two real, comparable branches
(E6xSU(3)_f vs. SO(16)->SU(4)) alone -- but the "six branches, six
selectors tested" framing below overstates what was actually checked.
Treat everything below this notice as scoped to those two real
branches, not six.**

**Status: mostly CLOSED (verdict 2), one untested candidate flagged
(verdict-3 flavor). Every selector actually tested has zero
discriminating power among E8's maximal-subalgebra branchings. One
genuinely untested candidate remains. No change to project-level
status (0/19).**

## A. Established facts

| Claim | Label | Basis |
|---|---|---|
| By Borel-de Siebenthal, E8's equal-rank (regular, extended-Dynkin-diagram single-node-deletion) maximal subalgebras form a fixed, finite menu. This project has already tested six of them: E6xSU(3) (Phase A2, gives 3), SO(16)->SO(10)xSU(4) (`ALL_DERIVATIVES.md` item 10 / "PUSH #10", gives 4), SU(9) (Z43, plethysm-type, doesn't reach clean SM matter), SU(5)xSU(5) (Z44, closed negative, no natural 3), F4xG2 (Phase F/Z39, cubic Casimir obstruction), E7xSU(2) (noted at O2 filter stage to cap at 2 generations from the SU(2) factor) | L1 | cross-checked against each phase's own frozen result file |
| Generation multiplicity is chain-dependent: E6xSU(3) gives 3, SO(10)xSU(4) gives 4, others give non-generation-shaped or capped results. "E8 contains 3 generations" is true of exactly one branch out of (at least) six standard ones | L1 | direct comparison of the above |
| The project's own `docs/solution.md` already states this honestly: 3 generations hold "given the E6xSU(3)_f branching chain; this chain is not itself picked out uniquely by the algebra" | L1 (already frozen, not new) | `docs/solution.md` |
| The historical record shows the SO(10)xSU(4) chain was set aside with the stated reason "**Wrong gen count**: 4 gens, not 3" | L1 | `docs/ALL_DERIVATIVES.md` line ~430 (verbatim) |
| E8 has no independent cubic Casimir invariant / all its irreps are real type -- it is unconditionally anomaly-free, and this property is inherited automatically by every subalgebra embedding regardless of which branch is chosen | L2 | standard fact in the GUT/anomaly literature (consistent with this project's own closed Phase H, "the full Green-Schwarz condition adds no constraint beyond what any complete 16-plet automatically satisfies") |

## B. Candidate generation selectors

**1. Chirality preservation** (does the branch give complex, not
vectorlike, matter content?)
- Object: complex vs. self-conjugate representations at each branch.
- Exists because: representation theory of the subalgebra factors.
- Not arbitrary: a real physical requirement (the SM is chiral).
- Reduces freedom? **No.** Both surviving candidates (E6xSU(3) via
  `27`/`27bar` and SO(10)xSU(4) via `16`/`16bar`) are complex/chiral.
  This filter is satisfied by both 3- and 4-generation branches
  equally.
- **Rule 9: FAILS.** Would select the same branch regardless of
  whether the true count were 3 or 4 -- it doesn't distinguish them at
  all.

**2. Anomaly cancellation**
- Object: gauge anomaly coefficient (cubic Casimir/d-symbol) of the
  unbroken gauge group at each stage.
- Exists because: consistency of a chiral gauge theory.
- Not arbitrary: standard QFT requirement.
- Reduces freedom? **No.** E8 itself has zero independent cubic
  Casimir (Table A, row 5) -- anomaly-freedom is inherited
  automatically by *every* subalgebra of E8, not selectively by some.
- **Rule 9: FAILS, cleanly.** This is satisfied identically by all six
  tested branches; it would "select" any generation count E8 happened
  to produce along any chain.

**3. Maximal-subgroup "preference" / representation aesthetics**
- Object: some canonical ranking of Borel-de Siebenthal maximal
  subalgebras (Dynkin index, embedding index, "simplicity").
- Exists because: none, really -- checked here and found there is no
  standard total order on the extended-Dynkin-diagram node deletions;
  each of the six is "maximal" in exactly the same technical sense.
- Reduces freedom? **No.**
- **Rule 9: FAILS** -- and trivially so, since there's no actual
  criterion here to test, only the impulse to call one "nicer."

**4. Compatibility with Phase A1's specific octonionic Cl(10)
realization** (chirality/minimal-ideal/reality structure *as actually
built in this project's own code*, not the abstract SO(10) generator
algebra)
- Object: whether each of the six branchings' generators can be
  expressed consistently using only the octonion left-multiplication
  structure Phase A1's gamma matrices are actually built from
  (`support/qosc_division_connection.py`), the way Z43 showed for
  SU(9)'s plethysm embedding specifically.
- Exists because: Phase A1's Cl(10) is not an abstract, basis-free
  Cl(10) -- it is one particular, octonion-derived realization, which
  is *extra* structure beyond bare Cl(10;C)~=Mat(32,C). A branching
  chain compatible with that specific structure is a genuinely
  narrower and non-circular requirement than "any E8 branching."
- Reduces freedom? **Unknown -- not tested anywhere in this project.**
  This is a real gap, not a closed question.
- **Rule 9: cannot be evaluated yet** -- it hasn't been run. This is
  flagged, not scored.

## C. Verdict

**2. The 3-generation result is a chosen branch, not a forced one --
established by every selector actually tested (chirality, anomaly
cancellation, maximal-subgroup structure all fail Rule 9 identically).
The branch that gives 3 was, as a matter of project history, kept
specifically because it gives 3 (`ALL_DERIVATIVES.md`'s own stated
reason for rejecting the 4-generation alternative) -- exactly the
Rule 2 pattern this project exists to catch, now located precisely
rather than left implicit in `solution.md`'s honest-but-vague caveat.**

One candidate (B4, compatibility with Phase A1's specific octonionic
realization) remains genuinely untested and could in principle change
this verdict -- it is not another version of the three failed
selectors above, since it doesn't reduce to "does it match 3," and it
uses only structure this project has already committed to (Phase A1's
actual code), not new imported assumptions.

## D. Next calculation

Concretely: take each of the six branchings' generator sets (already
computed in Z39/Z43/Z44/ALL_DERIVATIVES for the gauge-algebra pieces)
and check whether they can be written as polynomials in Phase A1's
actual octonion left-multiplication operators (`build_octonion_
structure_constants`), the same way Z43 verified SU(9)'s embedding
against octonionic triality. Concretely: for E6xSU(3) vs. SO(10)xSU(4),
does one of the two arise naturally from the octonion structure Phase
A1 already builds, while the other requires generators outside that
structure (e.g. genuinely needs the SO(6)~SU(4) generators unrelated
to any octonion bilinear)? If exactly one survives this filter and it
is the 3-generation one, THAT would be a real, non-circular selector
(passes Rule 9 by construction, since it doesn't reference the desired
count at all) and would upgrade the verdict. If both survive, or
neither does cleanly, this closes as verdict 2 with no exceptions
left to check. **Not run here** -- this is the audit, not the
computation.

## Class of mechanisms eliminated by this phase

Any argument of the form "criterion X singles out the physical E8
branch" where X in {chirality of the resulting matter, gauge anomaly
cancellation, abstract maximal-subalgebra ranking} is now closed --
none of these discriminate among Borel-de Siebenthal branches of E8,
because they are either satisfied by multiple branches equally
(chirality) or inherited automatically from E8 itself regardless of
branch (anomaly-freedom), or don't exist as real criteria at all
(aesthetic maximality).
