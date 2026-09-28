# POST_AUDIT_TARGET.md — the exact remaining target (2026-07-28)

This document responds directly to the POST_AUDIT_RESEARCH_PHASE_PROMPT's
Task 2. It states, precisely and with no rounding up, what Cl(10)×E8
has already derived, what remains free, and the exact numerical target
any future selection mechanism must hit to count as progress.

---

## A) What is already derived (L1, zero free continuous parameters)

| Result | Source | Scope note |
|---|---|---|
| Gauge group SU(3)×SU(2)×U(1) | Cl(10) Witt-pair structure (Phase A1) | Unconditional |
| Charge quantization in units of 1/3 | Cl(10) occupation numbers (Phase A1) | Unconditional |
| 3 chiral generations + right-handed neutrino | E8 → (16,3) under E6×SU(3)_f (Phase A2) | **Conditional on the E6×SU(3)_f branching chain.** A different, equally standard chain (E8→SO(16)→SO(10)×SU(4)) gives 4 generations instead. Nothing in the algebra picks one chain over the other — see `ALL_DERIVATIVES.md` item 10 and `phase_s_embedding_selection_check.py`. |
| Allowed Higgs representations for a Yukawa coupling are exactly {10, 120, 126}; every other SO(10) irrep gives Hom_G(16⊗16⊗H,1)=0 | Phase X | Unconditional, given 3 generations |
| The 10-vs-126 split within the symmetric channel | Phase X + Phase Y (2026-07-28) | Now L1 (was L2-cited); no change to the free-parameter count |
| Coupling structure per generation pair is unique (Sym²/Λ² of the flavor space, not a further gauge-invariant freedom) | Phase X | Unconditional |

## B) What remains free

- **Yukawa matrices**: exactly 6 complex parameters (H ∈ {10, 126}, symmetric
  channel) or 3 complex parameters (H = 120, antisymmetric channel), per
  Phase X/Y. This is the *flavor*-index freedom, not a gauge-index
  freedom — gauge symmetry has already done everything it can do to this
  sector.
- **Vacuum expectation values**: no mechanism in this framework generates
  or constrains any VEV; every VEV direction or magnitude used in the
  extended (Phase D, L3) model is an external input.
- **Coupling constants**: g1, g2, g3 at M_Z are QFT running-coupling data,
  not algebraic output. Cl(10)×E8 supplies which gauge groups exist, not
  their coupling strengths.
- **Scales**: no dimensionful quantity of any kind exists in Cl(10) or E8
  as abstract algebraic structures (both are defined with no built-in
  energy scale) — this rules out all fermion masses, m_H, v, and any
  threshold-dependent value from being derived by algebra alone,
  independent of whatever dynamics might eventually be layered on top.

## C) The exact target

A successful selection mechanism must reduce:

> **6 complex symmetric Yukawa parameters (if H ∈ {10, 126}), or 3 complex
> antisymmetric Yukawa parameters (if H = 120), into fixed values or
> relations.**

This is the whole target. It is not "solve the flavor problem" in the
open-ended sense — it is a specific linear-algebra object (a point, or a
constrained subvariety, inside C^6 or C^3) that a mechanism must select,
non-arbitrarily, from data already inside Cl(10)×E8.

Anything that does not touch this specific 6- or 3-dimensional space —
however sophisticated, however many other things it correctly derives —
is not progress on the open question, by definition. This is the
project's own repeated failure mode (Phases E–W): mechanisms that
correctly constrain the *gauge* sector while leaving the *flavor* sector
completely untouched, then get reported as if they were progress on "the
free-parameter problem" in general. Phase X/Y exist specifically to make
that conflation impossible to make by accident from here on.

## D) Priority ranking for future work (Task 4)

**Priority 1 — Intrinsic spectral triple / Dirac operator route.**
Can D_F, J, chirality and the order-one condition be constructed
*uniquely* from Cl(10)×E8 data (not imported from
Chamseddine–Connes–van Suijlekom)? Required test: does the construction
uniquely determine the point in the 6-or-3-dimensional Yukawa space, or
does it just relocate the freedom under a new name (a VEV ratio, a
Clebsch coefficient, a root-coupling matrix — the exact failure mode of
the messenger fix and the Item-1 addendum's root-coupling matrix)? Not
attempted this session — genuinely needs noncommutative-geometry/
Seeley-DeWitt tooling this environment does not have (see
`session_new_files/RESULT_item1.md`), and a same-session attempt at this
scale risks exactly the kind of fabricated-rigor result Rule 4 exists to
catch. Real cost: multi-week, specialized math, not incremental coding.

**Priority 2 — Invariant multiplicity completion.**
Compute dim Hom_G(R_generation ⊗ R_generation ⊗ R_Higgs, 1) for all
relevant Higgs representations; classify 0 (forbidden), 1 (unique
invariant), >1 (unresolved freedom). **This priority is now complete**
for the question as originally posed by Phase X: every H outside
{10,120,126} is Case 0 (forbidden); each of the three eligible H is
Case 1 *per generation pair* (Phase X); the internal 10-vs-126
bookkeeping ambiguity that was the one remaining loose end is now closed
(Phase Y, this session — see `session_new_files/RESULT_phase_y.md`).
Reproducibility: `phases/phase_x_hom_g_invariant_audit.py` and
`phases/phase_y_hodge_star_self_duality.py` both run clean and are
independently checked, per Task 6 below.

**Priority 3 — RG route.**
Only worth investigating if beta functions are derived from the actual
model content and boundary conditions come from Cl(10)×E8 itself, with
no fitted starting values. Not attempted — Item 42
(`docs/ALL_DERIVATIVES.md`) already establishes that this project has
never gotten past a *counting* argument (~108 possible Yukawa couplings)
to an actual beta-function calculation, and a fixed point that exists
but isn't dynamically selected is not a prediction. No new tooling for
this was added this session.

## F) Research decision (Task 6 output)

**One real derivation was chosen and completed this session: Priority 2
(invariant multiplicity completion).** Result: the 10-vs-126 split is
now L1, closing Phase X's one remaining citation gap
(`phases/phase_y_hodge_star_self_duality.py`,
`session_new_files/RESULT_phase_y.md`). It changes no downstream
conclusion — as scoped in advance (section E above), it was never
expected to.

**Continue with Priority 1 (intrinsic spectral triple) — but not in this
session, and not without the right tooling.** Reasoning: it is the only
remaining candidate mechanism in the entire failure map
(`docs/MECHANISM_FAILURE_MAP.md`) that could, in principle, actually
reduce the 6-or-3 count rather than merely relocate or fail to touch it
(unlike every other row in that table). It has a precise, pre-committed
pass/fail test (section E) so it cannot be graded on vibes later. It
genuinely requires noncommutative-geometry/Seeley-DeWitt tooling this
environment does not have, and constructing a candidate D_F by hand,
under this session's time and verification constraints, risks exactly
the fabricated-rigor failure mode Rule 4 exists to catch (see the
Item-1 addendum's own root-coupling-matrix attempt, which is already in
the failure map as a cautionary example of what a rushed attempt at
this looks like). **Do not attempt Priority 1 again without either (a)
real NCG computer-algebra tooling, or (b) a multi-week, carefully-
audited derivation budget — a same-session attempt would not meet this
project's own evidentiary bar.**

**Update (2026-07-29, Phase Z3):** Priority 1 was revisited, narrowly —
not by hand-building a candidate D_F (still out of scope per the above),
but by testing whether Z2's own generation-triviality assumption on `a`
was load-bearing. It was: gauging a real `su(3)_f` piece into `a` makes
all 9 generation-pair blocks of the order-one commutator nonzero, where
Z2 found them all exactly zero. This is a genuine, unprecedented result
in this project's history (see `docs/MECHANISM_FAILURE_MAP.md`, Phase
Z3 row) — but it is not yet a point in, or a reduction of, the
6-or-3-dimensional target defined in section C above. Two concrete,
cheap next steps close the gap between "nonzero" and "actual progress
on the target," and should be done before anything else under Priority
1:

1. Project Z3's nonzero blocks onto Phase X's 1-complex-dimension
   physical subspace per block, using tooling already in the repo
   (`z2_hilbert_space.py`, `phases/phase_x_hom_g_invariant_audit.py`).
   If the constraint is orthogonal to the physical subspace, Z3 reduces
   to another Rule 9 zero-selection-power case despite the nonzero
   numbers.
2. Compute the actual parameter count of a *working* (i.e.,
   symmetry-breaking, unlike the closed single-flavon case) SU(3)_f
   breaking sector, and net it against whatever step 1 shows Z3 removes
   from the C^6/C^3 target. This is the number that turns "likely fails
   net" (current status) into a proven result either way.

Only if both of these land favorably does Z3 graduate from "genuine but
unresolved constraint" to actual progress on the target in section C.

**Update (2026-07-29, Phase Z4 — supersedes the two steps immediately
above).** Step 1 above was attempted: D_F's blocks were built from
Phase X's actual CG tensor (`M10`, reused verbatim, not reimplemented)
instead of generic random matrices, and the induced cross-block terms
were checked for overlap with that physical direction. Numerically,
overlap was near-zero — but the more important finding came from a
prerequisite check that hadn't been done anywhere in Z1–Z3: Phase X's
CG tensor is chirality-*preserving* (`[Γ_F, T32] = 0` exactly), while
the graded spectral-triple `D_F` that the order-one condition is
defined for must be chirality-*flipping* (`{Γ_F, D_F} = 0`) by the
standard NCG grading axiom. **These are not the same kind of object.**
No construction anywhere in this project maps one to the other. This
means Z1, Z2, and Z3's block-norm results — every number in this
project's Priority-1 work so far — describe a chirality-agnostic
stand-in, not Phase X's actual Yukawa freedom. Steps 1 and 2 above are
therefore premature: **the real next step is building an explicit,
grading-respecting map from `M10`/`M120`/`M126` to a chirality-flipping
block of a graded `D_F`** (standard in principle in the NCG-GUT
literature, via a Γ_F-odd Dirac-operator construction — not attempted
here, and a genuine new construction, not a parameter tweak). Until
that bridge exists, no further order-one-condition variant on the
current chirality-agnostic D_F is worth running — it would be adding
more numbers to a construction already shown not to be asking the
right question. See `docs/MECHANISM_FAILURE_MAP.md`'s Phase Z4 row and
`session_new_files/RESULT_phase_z4.md` for the full computation.

**Stop pursuing Priority 3 (RG route) for now.** Reasoning: no new
tooling for real beta-function calculation was added or found this
session; Item 42 already establishes this project has never gotten past
a counting argument; and even a genuine fixed point, once found, is not
automatically a *dynamically selected* prediction unless the boundary
conditions themselves come from Cl(10)×E8 rather than being fitted —
which is the same failure mode as every other row in the failure map.
Revisit only if a specific, falsifiable beta-function calculation with
Cl(10)×E8-derived boundary conditions is proposed; do not restart this
as an open-ended "try RG" effort.

**Update (2026-08-01, Phases Z6–Z14).** The chirality-flipping bridge
Phase Z4 called for was built (`D_F = [[0,Y_H⊗Y_gen],[(Y_H⊗Y_gen)†,0]]`,
using Phase X's actual `M10`/`M120`/`M126` tensors), and the full
`su(3)_F` order-one condition was run on it and confirmed exactly
(symbolically, zero floating-point tolerance, Z13): unbroken `su(3)_F`
forces the symmetric-channel Yukawa to `c·I_3` (6 complex → 1 complex)
and the antisymmetric channel to exactly zero (3 complex → 0). Phase
Z14 then applied Rule 9 and checked this against Theorem B-3 (already
on record: a minimal single-triplet `SU(3)_f` flavon potential forces
its own VEV to `ε=0`). **Net result: not progress on the target as
originally hoped — the combination is a sharper exclusion instead.**
Minimal Cl(10)×E8, with `SU(3)_f` gauged (confirmed as Phase A2's
actual `(1,8)` inside 248, not an unconnected stand-in) and only a
minimal flavon sector available, dynamically prefers exactly the
vacuum that predicts degenerate-or-zero fermion masses — excluded by
observation. This closes the "unbroken vs. minimally-broken `SU(3)_f`"
question definitively negative; it does not touch whether some
non-minimal breaking sector could still work (see Z14's own next-step
note — any such attempt must state and net its own new parameter count
up front, same standard as every other row in the failure map).

**Update (2026-08-01, Phase Z19).** Two external documents this session
proposed "twisted spectral triples" as the untried route under Priority
1. Checked directly: the standard twisted order-one condition (fixed
automorphism `ρ`) is still linear/homogeneous in `D_F` (symbolic
expansion, `session_new_files/phase_z19_twisted_triple_linearity_check.py`),
so Phase Z1's impossibility proof carries over unchanged — any twist of
this standard kind still cannot isolate a point in Yukawa space, only
reorganize the moduli. **Priority 1 is now precisely: does a
`D_F`-dependent (self-referential/modular) twist exist for Cl(10)×E8,
built from `D_F`'s own spectral data rather than fixed in advance?**
This is the *only* structurally possible way any spectral-triple route
could fix a point rather than a subspace — a real, hard, well-defined
mathematical question, not the vaguer "try twisting" both documents
proposed. It still requires the same NCG/Seeley-DeWitt tooling this
environment lacks and the same multi-week-derivation caution already on
record; this update's contribution is narrowing the target, not
attempting the construction.

## E) Rule 9, applied to this document itself

Before either priority is pursued further: would the proposed mechanism
plausibly have failed to reproduce a different, wrong answer? Priority 2
(this session's actual work) passes trivially — it is not a
parameter-selection mechanism and does not claim to be one; it only
completes a representation-theory bookkeeping question with a
determinate, checkable right answer, independent of what the true SM
Yukawa values are. Priority 1, the moment any candidate D_F is proposed,
must be checked against this exact test before its result is written up
as anything more than L3/speculative.
