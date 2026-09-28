# Phase R7: Octonionic Realization Branch Selector Audit

**Status: CLOSED, negative, L1 (mechanical/static check, not
symbolic algebra -- this phase checks whether a *bridge* exists in the
repo's own code, which is exactly determinable). Outcome: 3 (no
branches survive). No change to project-level status (0/19).**

## R6 correction (required before this phase could be scoped honestly)

R6 claimed six branches were "already tested": E6xSU(3), SO(16)->SU(4),
SU(9), SU(5)xSU(5), E7xSU(2), F4xG2. Rechecked against
`PROJECT_STATE_HANDOFF.md` and `FINAL_AUDIT.md` (which explicitly list
*"E8 maximal-subgroup chains other than E6xSU(3)_f"* as **open,
unattempted**, as of Z42) and against the actual files:

- **E6xSU(3)_f** (Phase A2) and **SU(5)xSU(5)** (Z44) are real,
  frozen, and correctly attributed.
- **SO(16)->SO(10)xSU(4)** is real but lives only in
  `docs/ALL_DERIVATIVES.md`, a pre-Z-numbering exploratory scratch
  document, not a frozen phase at the same rigor tier.
- **SU(9)** and **E7xSU(2)**: no dedicated branch computation exists
  anywhere in this repo. R6 fabricated the claim that these were
  tested. Retracted.
- **F4xG2**: R6 misattributed `phase_z39_e8_cubic_obstruction` to this
  branch. That phase actually tests the E8 cubic Casimir/Schur
  obstruction *inside the already-adopted E6xSU(3)_f branch* (flavon
  dynamics), an unrelated question. No F4xG2 branch computation
  exists. Retracted.

This is logged here rather than silently fixed, per Rule 5 (document
failures, including this project's own errors, with the same
prominence as positive results).

## What R7 actually tests

For the three branches that DO have real, frozen computations
(E6xSU(3)_f, SO(16)->SU(4), SU(5)xSU(5)): does any file express that
branch's *non-SO(10)* generators (the family/flavor factor that
distinguishes the branches from each other) as an explicit function of
Phase A1's octonion left-multiplication operators
(`build_octonion_structure_constants`)?

Method (`scripts/r7_bridge_check.py`): mechanical string/content check
against the actual source files, not new symbolic derivation --
appropriate because the question "does this bridge exist in the code"
is a yes/no fact about the repository, checkable exactly, before any
per-branch algebra is worth attempting.

## Result

**Zero of the three real branches have any octonion-operator
realization of their distinguishing generators.** `phase_a2_e8_core.py`
builds all 240 E8 roots and the branching dimension-counts entirely in
an abstract 8-dimensional Cartan/SO(16)-embedding coordinate space
(`np.array` weight vectors), with no reference to octonion structure
constants anywhere. `z44_branching.py`/`z44_structure_check.py` are the
same (Slansky-table branching + literal Kronecker products, no
octonion content). The one apparent hit (`docs/ALL_DERIVATIVES.md`
contains the string "octonion") was manually checked and is a false
positive -- that mention is 120+ lines away, in an unrelated Malcev-
Casimir discussion, not attached to the SO(16) item at all.

**What Phase A1's octonion operators DO already cover, consistently
across all three branches:** the SO(10)-internal gauge generators
(SU(3)_c, SU(2)_L) are built directly from the octonion-derived gamma
matrices (`phases below_Z_25/phase_a1_cl10_core.py`, steps 4-5). This
part is common ground, not a discriminator -- every branch contains an
SO(10) factor, and that factor is octonion-grounded in all of them
equally. The generators that actually distinguish the branches (the
SU(3)_f, SU(4), or SU(5)_B factor) are exactly the ones with no
octonion realization, in every case checked.

## Acceptance criteria applied

Per the brief: a branch survives only if every generator comes
directly from the existing Phase A1 implementation, no additional
algebra, no added projectors, no new degrees of freedom, no hand-
selected subspaces. **None of the three testable branches even reach
the point of needing to check for added projectors or hand-selected
subspaces** -- they fail at the first, most basic criterion (task
question 1: "can every required generator be written exactly using the
existing octonionic basis?"). Answer: no, for the distinguishing
generators, in all three cases, because those generators were never
attempted in octonion terms at all -- Phase A2 and Z44 both work in a
wholly separate formalism (abstract root/weight space) with no
existing map back to Phase A1's operators.

## Comparison against R6

R6 concluded (correctly, and this still stands): among selectors
actually tested (chirality, anomaly cancellation, maximal-subgroup
aesthetics), none discriminate among branches, and the historical
record shows the surviving branch was kept because it matches
observation (Rule 2 pattern). R7 was supposed to test the one
remaining non-circular candidate (Phase A1 octonionic compatibility).
**It cannot yet be tested per-branch, because the object needed to run
the test -- E8 generators expressed as octonion-operator polynomials
-- does not exist in this project's code for any branch.** This is a
sharper, more fundamental finding than "the selector didn't
discriminate" -- it's "the selector-candidate was never actually built
far enough to be evaluated." R6's list of "six branches" is also now
corrected to three real ones plus three that need to be retracted.

## Outcome (per the three acceptance conditions)

**3. No branches survive.** More precisely: Phase A1's octonionic
realization, as it currently exists in this repo, cannot be used to
select among E8 branches at all, because it has never been extended
into the E8 adjoint (248-dim) in the first place -- only into the
SO(10) subalgebra (45-dim), which is common to every branch and
therefore structurally incapable of discriminating between them no
matter how the test is run.

## What this eliminates

Any claim of the form "Phase A1's octonionic structure selects the
physical E8 branch" is now closed as currently statable -- not because
it was tried and failed per-branch, but because the prerequisite
construction (an octonion-operator realization of the full 248, or at
minimum of each branch's distinguishing factor) has never been
attempted anywhere in this project. Building that bridge would be
genuinely new work (extending Phase A1's octonion operators from a
Cl(10)/SO(10) realization to a full E8 realization), not a re-run of
anything already tried -- and is explicitly out of scope here per "do
not invent new operators."
