# CHANGELOG

## 2026-08-03 — Phase R8: octonionic-to-E8 lift feasibility audit (external session)

Additive only. Feasibility audit (no construction) on the prerequisite
R7 identified: can Phase A1's octonion operators, in principle, be
extended to a full E8(248) realization?

**Result: yes, in principle -- verdict 2 (additional mathematics
required, exact gap identified).** The standard Freudenthal-Tits magic
square gives `E8 = Der(O) (+) Der(J3(O)) (+) (O0 x J3(O)0) = G2 (+) F4
(+) (7x26) = 14+52+182 = 248` (Freudenthal 1954, Tits 1955, surveyed in
Baez 2002). Every equivalent formulation checked (magic square, Tits'
Freudenthal Triple System route to E7 then E8, Kantor-pair
reformulation per Truini, already cited in this project's own
hypothesis backlog) requires the **exceptional Jordan algebra J3(O)**
(27-dim, 3x3 Hermitian octonionic matrices under the Jordan product) as
the one new ingredient -- Phase A1's Clifford/CAR-operator formalism
cannot produce this on its own; it's a different category of algebra
(commutative, power-associative, not associative). This exact gap was
already flagged and left unpursued in `docs/PHASE_R_HYPOTHESIS_
BACKLOG.md` item 9 -- confirmed here with the precise dimensional
recipe and standard sourcing for the first time. No exhaustive search
of this repo found a forgotten implementation (checked: jordan/albert/
FTS/magic-square/Tits/Kantor, every hit manually reviewed; one false
lead, `tmp_task_e_fts.py`, is unrelated). No published theorem forbids
this specific lift; a different, real, precisely-cited theorem
(Distler-Garibaldi, arXiv:0905.2658, already flagged in this project as
"Priority 0") forbids a downstream step (fitting 3 chiral generations +
gravity into one E8 adjoint copy) and is noted as a risk for later, not
a reason to stop here. Nothing built, no operators invented, Phase A1
untouched, per this phase's own acceptance criteria. See
`phase_r8_octonion_e8_lift_feasibility/`. No change to project-level
status (0/19).

## 2026-08-03 — Phase R7: octonionic realization branch selector audit (external session)

Additive, plus one correction to R6. Tests R6's one remaining
non-circular candidate: does Phase A1's octonion left-multiplication
operator basis uniquely realize one of the candidate E8 branches?

**R6 correction (found while scoping R7):** R6 claimed six branches
were "already tested" (E6xSU(3), SO(16)->SU(4), SU(9), SU(5)xSU(5),
E7xSU(2), F4xG2). Checked against `PROJECT_STATE_HANDOFF.md`/
`FINAL_AUDIT.md` (which state "E8 maximal-subgroup chains other than
E6xSU(3)_f" were open/unattempted as of Z42) and against the actual
files: **SU(9) and E7xSU(2) have no dedicated branch computation
anywhere in this repo** (fabricated in R6, retracted), and **F4xG2 was
misattributed** to `phase_z39_e8_cubic_obstruction`, which actually
tests flavon dynamics inside the already-chosen E6xSU(3)_f branch, an
unrelated question. Only three real branches exist: E6xSU(3)_f (Phase
A2), SO(16)->SU(4) (pre-Z-numbering sketch in `ALL_DERIVATIVES.md`),
and SU(5)xSU(5) (Z44). R6's actual verdict is unaffected -- it was
already supported by the two comparable real branches alone.

**R7 result (outcome 3, no branches survive):** none of the three real
branches' distinguishing (non-SO(10)) generators have ever been
expressed as functions of Phase A1's octonion operators anywhere in
this project. Phase A2 and Z44 both build their E8 structure entirely
in an abstract Cartan/root-space representation (dimension counting,
Slansky tables), with zero octonion content (confirmed by direct
code/file inspection; one apparent string match in `ALL_DERIVATIVES.md`
checked manually and found to be an unrelated false positive). Phase
A1's octonion operators DO already realize the SO(10)-internal
SU(3)_c/SU(2)_L generators -- consistently across all branches, which
is exactly why that common piece can't discriminate between them.
**The missing ingredient is prerequisite, not per-branch**: nobody in
this project has extended Phase A1's octonion realization from
SO(10) (45-dim) to the full E8 (248-dim). That's flagged as new
construction work, explicitly out of scope for this falsifier phase.
See `phase_r7_octonionic_realization_selector/`. No change to
project-level status (0/19).

## 2026-08-03 — Phase R6: generation branch selection audit (external session)

Additive only. Tests whether anything selects the E6xSU(3) (3-gen)
branch of E8 over the SO(16)->SO(10)xSU(4) (4-gen) branch, or the
other four already-tested maximal-subalgebra chains. **Result: every
selector actually tested fails Rule 9.** Chirality is satisfied by
both the 3- and 4-generation branches equally. Anomaly cancellation is
inherited automatically from E8 itself (E8 has no independent cubic
Casimir -- all irreps real type) regardless of branch, so it
discriminates nothing. Abstract maximal-subalgebra "preference" is not
a real criterion (no canonical ranking exists among Borel-de
Siebenthal branches). The historical record (`ALL_DERIVATIVES.md`)
shows the 4-generation branch was in fact rejected with the stated
reason "wrong gen count" -- i.e. by direct comparison to the desired
answer, the exact Rule 2 pattern this project's own rules exist to
catch, now made explicit rather than left as `solution.md`'s general
caveat. One candidate remains untested: whether Phase A1's specific
octonionic Cl(10) realization (not the abstract algebra) is compatible
with only some of the six branches, the way Z43 checked for SU(9).
Verdict: chosen branch, not forced (with one open exception, scoped as
the concrete next test, not run). See
`phase_r6_generation_branch_selection/README.md`. No change to
project-level status (0/19).

## 2026-08-03 — Phase R5: does E8 independently select the sedenion level? (external session)

Additive only. Direct test of the missing arrow R4 identified
(`Cl(10)xE8 -> ? -> sedenion-like structure`). Result: **closed,
negative.** E8's actual mathematical origin (Freudenthal-Tits magic
square) is defined on Hurwitz division algebras only (R,C,H,O); by
Hurwitz's theorem these are exactly four, terminating at octonions
(dim 8) -- E8 is the (O,O) magic-square entry precisely because O is
the *largest* Hurwitz algebra, not an arbitrary point on an
open-ended tower. Sedenions (dim 16) are not a division algebra and
sit outside this classification entirely. Checked against Phase A1's
own code: it builds Cl(10) from octonion structure constants directly
and performs no Cayley-Dickson doubling anywhere. Verdict: the
sedenion step Gresnigt's S3 mechanism needs is not merely unmotivated
by E8 (a Rule 9 "too many options" failure) -- the framework's own
most relevant structure actively terminates one step earlier, for a
reason (Hurwitz's theorem) unrelated to generation-counting. This
route is closed, not left open pending a selector search. See
`phase_r5_sedenion_selector_audit/README.md` for the full record. No
change to project-level status (0/19).

## 2026-08-03 — Phase R3-R1: self-correction, R3 likely mistargeted

Additive only. On review (prompted by user audit of R3), checked R3's
construction against the already-frozen Z22 `psi_3` mechanism and found
R3's `S5 -> S3xS2` (partitioning one spinor's 5 Cartan directions) is
almost certainly the color/weak split (already-derived gauge structure)
and NOT the generation-replication mechanism. `psi_3`'s order-3
property is imported from Gresnigt's literature formula, not derived —
that is the actual unresolved "why 3" question, and R3 did not test it.
See `phase_r3_s3_forced_test/interpretation.md` [R3-R1 correction] and
revised README status line. No change to project-level status (0/19).

## 2026-08-03 — Phase R3: S3-forced-vs-selected test (external session)

Additive only, nothing previously-derived edited. Runs the falsifier
the Z44 external audit proposed: is S3 forced by Aut(Cl(10)'s Witt
decomposition), or merely selected?

**Result: neither cleanly. `S3 x S2` (order 12) is confirmed maximal in
`S5`, order 120, matching the qualitative "3 and 2" shape — but 10
conjugate copies exist and the bare Witt+chirality data (Weyl(D5),
order 1920) does not distinguish them. Rule 9 fails as-is: the
construction has zero power to prefer 3-vs-2 over any other partition.
Cross-referenced against the existing, unrelated Z23 Task B S3-
uniqueness result (which assumes 3 generations as input rather than
deriving it) — the two do not overlap and neither derives "3" from
nothing. See `phase_r3_s3_forced_test/` for the full record, including
the concrete follow-up (R4, not run) needed to close this either way.**

No change to project-level status (0/19 stands).

## 2026-08-02 — Phase Z23, Tasks B, E, F, G: family group, 126 -> SM,
## F4xG2, E6xSU(3)_f anomalies (external session, part 3)

Additive only, nothing previously-derived edited.

1. Task B: family-group uniqueness from GAP 4.15.1 — enumeration of
   all 311 groups of order 2..60 with the four criteria (faithful real
   2-dim plane rep; order-3 element of trace -1 = psi_3; order-2
   element of trace 0 = 2:1:1 reflection; faithful action on 3
   points): census 86 -> 30 (rotation) -> 28 (reflection) -> 10 (both,
   the dihedral D_6k) -> criterion (iv) leaves exactly S3. Verified:
   every (rotation, reflection) pair generates S3 (order 6); D12 =
   S3xC2 (isomorphism check passed); S3 character values [2,0,-1] on
   (e, reflection, rotation), real via FS indicator. GAP debug trail
   (Trace reserved; class functions not callable; Indicator/PositionClass
   absent) documented in the result file.
2. Task E: SO(10) 126 -> SU(5)xU(1): 1(-10)+10(-6)+50(-2)+5(-2)+45(2)
   +15(6), dims 126; U(1)_X total 0; then SU(5) -> SU(3)xSU(2)xU(1)_Y:
   45 submultiplets, all dim-verified, exact hypercharge tracelessness
   per SU(5) piece (e.g. 45-piece: 1+4-7-2-1-3+8 = 0). Key 126 content:
   (1,3,-1) triplet (type-II seesaw / Majorana VEV candidate), (1,1,-1),
   (1,1,2), (1,1,0) singlets; NO (3,2,1/6); 126 complex (126bar has
   negated charges). Cross-check: 16x16 = 10+120+126 branches term by
   term. Pati-Salam route documented as not LiE-computable (D5 diagram
   coloring is not a node deletion).
3. Task F: E8 -> F4xG2 (audit B6): 248 = (52,1)+(1,14)+(26,7) FORCED by
   weight counting (48 F4 + 12 G2 roots; complement 182 = 180
   non-zero weights + 2 zeros -> unique fit (26,7); (1,182) ruled out
   by nonzero F4-projections, (26,14) by weight count). B6 guess part
   (a) "26 = 16+10" DEAD: rank(SO(10)) = 5 > rank(F4) = 4; actual
   26 -> 9+16+1 under F4 superset SO(9), computed from explicit roots.
   Part (b) "7 = 3+3+1" TRUE (as 7 -> 3+3bar+1 under G2 -> A2 via the
   long-root subsystem; exact Fraction arithmetic; 14 -> 8+3+3bar
   also computed) — a conjugate (vector-like) pair, no chiral family
   structure. LiE cannot build the non-regular embedding (documented;
   Python root arithmetic used instead).
4. Task G: E6xSU(3)_f anomaly/consistency of the (27,3) family
   assignment — exact sympy generator arithmetic (SU(5) 5, 10 = Lambda^2,
   5bar, SU(3) 3): A(10)/A(5) = +1, A(5bar)/A(5) = -1, A(adjoint) = 0,
   A(16 of SO(10)) = 0 (each generation individually anomaly-free),
   A(27 of E6) = -2 != 0. Channel table: standalone chiral (27,3)
   fails E6^3 (= -6) and SU(3)_f^3 (= 27) -> structurally excluded;
   actual E8-adjoint content (27,3)+(27bar,3bar) passes every channel
   (vector-like completion already in the 248, Task C; no extra matter).
5. Result files: `.../RESULT_task_b_family_group.md`,
   `.../RESULT_task_e_126_sm.md`, `.../RESULT_task_f_f4g2.md`,
   `.../RESULT_task_g_e6su3_anomaly.md`, with scripts listed in their
   Reproducibility sections (GAP: tmp_task_b_*.g; LiE: tmp_task_e_*.lie;
   Python: tmp_task_f_firstprinciples.py, tmp_task_g_anomalies.py).
6. README.md: preservation note added after the Tasks C/D note (covers
   B, E, F, G), same format. Status remains 0/19. Nothing above that
   note was altered.

## 2026-08-02 — Phase Z23, Tasks C and D: E8/E6 branching rules computed
## from the root system (external session, part 2)

Additive only, nothing previously-derived edited.

1. Task C: closed audit Item 15's tooling gap — every E8 branching rule
   the project cites is now computed in-project with real
   multiplicities, not cited from Slansky tables. LiE 2.2.2
   `closure`/`res_mat`/`branch`/`dim`; embeddings built from explicit
   E8 root vectors (no built-in tables).
2. E8->E6xA2 (the Phase A2 "3 generations" chain): 248 = (78,1) +
   (1,8) + (27,3) + (27bar,3bar), dims 78+8+81+81 = 248, verified two
   independent ways — LiE closure AND pure-Python root classification
   (72 E6 + 6 A2 + 162 roots at |A2-part|^2 = 2/3, exact Fractions;
   E6 Cartan isomorphism proven by permutation). A2 located by brute
   force (beta1 = -e1-e2, beta2 = e1-e3; 72-root rank-6 orthogonal
   complement).
3. 3875 (omega_1) in every chain: E6xA2: (1,1)+(1,8)+(27,3)+(27,6)
   +(351,3)+(351,3)+(78,8)+(27,6)+(27,3)+(650,1), dims sum 3875 — note
   asymmetry: 27s but no 27bar. E7xA1: (1,1)+(56,2)+(1539,1)+(912,2)
   +(133,3), dims sum 3875. [Audit note: a scratch-script label swap
   ("248 ->"/"3875 ->") was caught by dimension sum and corrected.]
4. E8->D8->D5xA3 (audit Item 10 chain): 248 = 120+128 by direct weight
   restriction (112 D8 roots + 128 spinor weights); 120->(45,1)+
   (1,15)+(10,6), 128->(16,4bar)+(16bar,4), 16->(10,1)+(1,6). Item 10's
   "4 generations, not 3" reading confirmed with computed branching.
5. Task D: the Item 15 sub-question — E6 27^3 to SO(10)xU(1) — closed:
   27x27x27 = 1 + 2925 + 2(78) + 3(650) + 2(5824) + 3003 (19683 =
   27^3), and the full product contains exactly **3 x SO(10) 126 at
   U(1) charge -6, 0 x 126bar** (2x5824 + 3003 each carry one 126(-6)).
   Per-summand branches all dimension-verified; full polynomial (25
   terms) cross-checked against the sum of per-summand branches.
6. Result files:
   `session_new_files/phase_z23_external_session/RESULT_task_c_e8_branching.md`
   and `.../RESULT_task_d_e6_cubic_so10.md`, plus the Lie scripts and
   Python cross-checks listed in their Reproducibility sections.
7. Tooling: SageMath 10.9 installed and verified (conda-forge; package
   name is `sage`; the earlier `sagemath` attempt failed — now logged
   as SAGE_INSTALL_EXIT=0 in /root/sage_install2.log, `sage -c`
   verified). README.md: preservation note added after the Task A note,
   same format. Nothing above that note was altered.

## 2026-08-02 — Phase Z23, Task A: symmetric vs. orthogonal Higgs
## directions in the Cl(10)+S3 model (external session, part 1)

Additive only, nothing previously-derived edited.

1. Task A (of the Z23 external session plan): tested the escape hatch
   Z22 left explicitly open — Gresnigt's un-averaged, family-resolved
   orbit directions H_alpha, H_beta (paper eqs. 122-123), which he
   states are needed to lift the 2:1:1 degeneracy.
2. Independently reproduced paper eqs. 72/73 exactly: all four Higgs
   components are the paper's matrix units to 0.000e+00. Audit note: an
   initial err=1.000 was a bug in OUR check (`np.eye` scalar indexing
   returns 0.0, not the matrix unit) — fixed by explicit matrix-unit
   construction; the paper was right.
3. New results (all machine-precision, eigenvalues verified exactly in
   sympy): (i) Gram diag(1/2, 9/8, 9/8) — H_alpha, H_beta mutually
   HS-orthogonal and orthogonal to Hbar, equal norms, for all four
   components; (ii) both textures have the exact trace-free spectrum
   (0, +/-9*sqrt(2)/16); (iii) psi_3 acts on the (H_alpha, H_beta)
   plane as an exact 120-degree rotation — the real 2-dim irrep of S3,
   irreducible, hence NO S3-invariant direction in the plane; (iv)
   KEY NEGATIVE RESULT: Mbar is NOT in span(M_alpha, M_beta) —
   Tr(Mbar)=3/2, orthogonal directions are trace-free (exact theorem,
   residual 0.5): the symmetric point is unreachable from the
   S3-breaking subspace; (v) sector independence exact (up-type M_u =
   M_1 to 0.000e+00); (vi) E8 plays no role in this construction (pure
   Cl(10)+S3) — the VEV direction in the plane is a free angle.
4. Result file:
   `session_new_files/phase_z23_external_session/RESULT_task_a_orthogonal_higgs_directions.md`
   plus run artifacts `task_a_higgs_alpha_beta.py`, `task_a_full_output.txt`.
5. Tooling for later Z23 tasks (B-G): GAP 4.15.1 + HAP and LiE 2.2.2
   installed in WSL (verified working); SageMath install via conda-forge
   started (package is named `sage`, not `sagemath` — first install
   attempt failed on that). README.md: preservation note added after the
   Z22 note, same format. Nothing above that note was altered.

## 2026-08-02 — Phase Z22: Gresnigt's non-tensor generation structure
## imported, tested, and generalized (external session)

Additive only, nothing previously-derived edited.

1. Literature check: arXiv:2604.24795 (Gresnigt, Higgs/Yukawa completion
   of the Cl(10) S3 three-generation model already flagged in Phase U)
   read in full; its content had not previously been analyzed in this
   repo beyond noting its existence.
2. Independently reproduced Gresnigt's Cl(8)/Cl(10) + psi_3 construction
   from scratch (not cited) in `session_new_files/phase_z22_gresnigt_import/`.
   Caught and fixed one transcription bug (missing complex conjugate on
   an SVD nullspace vector, inconsistent with this project's own
   `solve_charge_conjugation` convention) during self-audit.
3. New result: `session_new_files/RESULT_phase_z22_generalized_cyclic_nogo.md`.
   Tests whether a non-tensor-product generation structure (the one
   direction Z21 left open) escapes the Z6-Z21 degeneracy. It does not
   — and the reason generalizes Z21's result rather than merely
   reconfirming it: any coupling invariant under the full S3 symmetry
   used to generate three copies from one seed is forced into a
   2-real-eigenvalues-plus-a-degenerate-pair pattern, by linear algebra
   alone, independent of tensor-vs-non-tensor implementation.
4. README.md: added a preservation note after the Z21 note, in the same
   format, describing this. Nothing above that note was altered.

This file did not exist before this pass. Created to give the repository
an in-place record of documentation-hygiene fixes, since it has no `.git`
history (confirmed: no version-control metadata anywhere in the archive).
Entries are listed newest first. Nothing described below changes any
previously-derived mathematical result; all edits are annotations,
retractions-in-place, a stray-duplicate archival, and one new addendum
script — traceable line-by-line in the diffs against the prior snapshot.

## 2026-08-01 (b) — Item 7 (S3 group cohomology) independently re-verified,
## no GAP/HAP dependency; a genuine SyntaxError fixed

Additive + one bug fix, no previously-derived physics result edited.

1. **Bug found and fixed:** `session_new_files/new_test_item7_s3_cohomology.py`
   had a genuine `SyntaxError` (line 54, unescaped apostrophe) and had
   never successfully executed — confirmed by re-running it before and
   after the fix. Its printed "GAP/HAP results" were a hand-typed
   transcript, not a live computation, exactly as
   `audit report/LIST_OF_CORRECTIONS.md` (C-1) found.
2. **New file `session_new_files/item7_reverification_no_gap.py`.**
   Independently re-derives H_1..H_4(S3;Z) with zero GAP/HAP dependency:
   builds S3 as an honest permutation group and checks (not assumes) it
   equals Z3⋊Z2 with inversion action; independently computes
   H_*(Z/2;Z) and H_*(Z/3;Z) from each cyclic group's own periodic
   resolution (first checking the resolution really is exact); checks
   the coprime-order vanishing lemma inputs explicitly. Caught and fixed
   its own bug mid-development (an earlier draft computed the
   resolution's own homology, which is trivially zero since a
   resolution is exact by construction, instead of the coinvariants
   complex that actually gives group homology) — left in the file's
   docstring as a documented correction, per the project's own
   transparency norms.
3. **New file `session_new_files/ITEM7_LHS_SPECTRAL_SEQUENCE.md`.** The
   analytic assembly step (Lyndon-Hochschild-Serre spectral sequence,
   full derivation, every input either code-checked or a named cited
   theorem) that combines the above into H_1=Z/2, H_2=0, H_3=Z/6, H_4=0
   — exactly reproducing the numbers the unrun `.py` file had quoted.
4. **`RESULT_item7.md`** updated with a status note; numbers unchanged,
   now L1 (independently re-derived) rather than an unverified external
   citation.
5. **`audit report/OPEN_PROBLEMS_AFTER_AUDIT.md`** secondary thread #4
   (Item 7 re-verification) marked closed.

## 2026-08-01 (a) — Phase Y2 added (exact-arithmetic hardening of Phase Y)

New follow-up computation, additive only — no previously-derived result
edited or retracted.

1. **New file `phases/phase_y2_hodge_star_exact_symbolic.py`.** Reruns
   Phase Y's Hodge-star self-duality split (10-vs-126 inside Sym^2(16))
   with exact sympy Gaussian-rational arithmetic instead of NumPy
   floating point — the specific "natural hardening step" Phase Y's own
   writeup flagged as still needed. Confirms the identical result: all
   122 weight blocks diagonalize to exactly +i/-i eigenvalues, and the
   self-dual eigenspace's weight table matches Phase X's residual
   exactly, key by key.
2. **New file `phases/RESULT_phase_y2_exact_symbolic.md`.** Full
   writeup, Rule 3 labeling, and an explicit statement of what remains
   out of scope (the project's actual "one real open problem" — the
   intrinsic spectral triple — plus Items 6/7/15, all of which need
   tooling this environment doesn't have).
3. **`README.md` phase table** gets one new row (Y2) directly under the
   existing Y row.
4. **`audit report/OPEN_PROBLEMS_AFTER_AUDIT.md`** updated: its
   secondary-open-thread #2 (the Phase X 10-vs-126 split, "no new
   packages needed, just more work") is marked closed, since Phase Y
   already closed it at L1 and this pass removes the one remaining
   caveat (numerical vs. symbolic). Threads #1, #3, #4 are untouched —
   still genuinely blocked on tooling (LiE/Sage/GAP-class Lie theory
   software) this environment does not have.

## 2026-07-29 — Phase Z4 added (physical-tensor projection; finds a
## grading mismatch in Z1–Z3)

Follow-up to Phase Z3, same session. Four changes, additive:

1. **New file `session_new_files/phase_z4_physical_projection_test.py`.**
   Rebuilds D_F's blocks from Phase X's actual CG tensor (`M10`, reused
   verbatim from `vertex_terms_resolved/build_and_test.py`) instead of
   Z3's generic random matrices, and checks the induced cross-block
   terms for overlap with that physical direction.
2. **New file `session_new_files/check_grading.py`.** Checks whether
   that physical tensor satisfies the standard NCG Dirac-operator
   grading axiom (`{Γ_F, D_F} = 0`). Finds it doesn't — the tensor
   commutes with Γ_F rather than anticommuting, a real, exact,
   machine-precision result (`‖{Γ_F,T32}‖ = 8.0 = 2‖T32‖`,
   `‖[Γ_F,T32]‖ = 0`), not a numerical artifact.
3. **New file `session_new_files/RESULT_phase_z4.md`.** Full writeup:
   both numeric results, the grading-axiom finding, and why the latter
   supersedes the former as the actual verdict.
4. **`docs/MECHANISM_FAILURE_MAP.md`, `docs/POST_AUDIT_TARGET.md`,
   `README.md` updated** to record the finding and correct the
   next-steps framing left by the Z3 session (those steps assumed Z1–Z3's
   D_F and Phase X's Yukawa tensor were interchangeable; Z4 shows
   they're not, without a bridge construction this project doesn't
   have).

## 2026-07-29 — Phase Z3 added (gauged SU(3)_f, order-one condition)

New mechanism session, follow-up to Phase Z2. Four changes, all
additive — no previously-derived result was edited or retracted:

1. **New file `session_new_files/phase_z3_family_gauge_order_one.py`.**
   Tests whether letting the order-one-condition's gauge element `a`
   carry a genuine `su(3)_f` generator (rather than Z2 Task 5's
   generation-trivial assumption) lets the order-one condition relate
   different generation-pair blocks of `D_F`. Built on Z2's own
   `cl10_gamma_J.py`/`z2_hilbert_space.py` objects; no reimplementation.
   Verified to run clean in-place (charge-conjugation residual 5.35e-15,
   unitary, one-dimensional null space).
2. **New file `session_new_files/RESULT_phase_z3.md`.** Full writeup:
   result (all 9 generation-pair blocks go nonzero, versus exactly zero
   in Z2), what it does and doesn't show, Rule 9 verdict (unresolved),
   and two concrete next steps.
3. **`docs/MECHANISM_FAILURE_MAP.md` updated.** New Phase Z3 row —
   the one row in the table that is neither a closed positive nor a
   closed negative — and the closing summary paragraph updated to note
   it.
4. **`docs/POST_AUDIT_TARGET.md` updated.** Priority 1 section gets a
   dated update note recording the Z3 result and the two next steps
   required before it counts as progress against the section-C target.
5. **`README.md` updated.** New addendum section at the end, same style
   as the existing Phase Z2 addenda.

## 2026-07-29 — Repository-consistency pass (external audit)

Follow-up to an independent mathematical + repository audit of the
coupled Yukawa β-function documents. Five changes:

1. **`RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md` (root and, see #3, its
   former duplicate): retraction banner + in-place Layer 4 annotation.**
   Layer 4's `λ(126,126)=6` table and its two
   `(unavailable, R_b=126)` placeholders were previously only
   *superseded by a later document*, never edited or flagged in the
   original file itself — a reader opening only this file would see
   contradicted numbers with no pointer to the correction. Fixed by:
   (a) a banner at the top of the file naming the retraction and
   pointing to the correct assembled system; (b) the stale Layer 4
   block itself kept **verbatim, for the historical record**, but
   wrapped in an explicit "RETRACTED — do not use" notice with the
   corrected values and the corrected assembled β(Y10,Y120,Y126)
   equations inserted immediately above it. Layers 0–3 (CG construction,
   `T(R)=dim(R)`, the real-real vertex table, the `C₂(16)` discussion)
   were unaffected and are unchanged.

2. **`RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md`, Layer 3: new
   cross-document flag on `C₂(16)`.** Added a note that
   `docs_new/SESSION_RESULT_2LOOP_GAUGE_YUKAWA_CLOSURE_TASKS_1_6.md`
   independently pins `C₂(16)=45/8` by citation, without reconciling it
   against this document's own first-principles `45/4` computation.
   **Not resolved** — flagged only, since resolving it requires
   determining which generator-normalization convention each document's
   `g` is defined against, which is outside the scope of either
   document's own stated task.

3. **`docs_new/RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md`: archived.**
   This was a byte-for-byte duplicate of the root file, and — checked
   against `docs_new/INDEX.md`, which enumerates exactly three session
   files for this folder — was never a tracked part of the `docs_new`
   session series. Moved to
   `archive/docs_new__RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md` (preserved,
   not deleted) and replaced at its original path with a short stub
   pointing to the canonical root file and to this changelog.

4. **`docs_new/SESSION_RESULT_2LOOP_GAUGE_YUKAWA_CLOSURE_TASKS_1_6.md`:
   matching cross-document flag added** at the point where `C₂(16)=45/8`
   is introduced, pointing back at item 2 above. Also not resolved by
   this flag — both sides now name the disagreement explicitly instead
   of one side silently disagreeing with the other.

5. **`vertex_126_external_completion/`: new addendum,
   `ADDENDUM_COVARIANCE_10_120_CROSS_TERMS.md` +
   `covariance_check_10_120_addendum.py`.** A prior audit found that the
   explicit generator-commutator covariance test used elsewhere in this
   folder (for `λ(10,10)`, `λ(10,126)`, `λ(120,126)`) had never been run
   for the nonzero cross entries `λ(120,10)=48` / `λ(10,120)=4` — the
   only source of Y10–Y120 mixing in the assembled system. This addendum
   **partially** closes the gap: it independently re-derives both
   numbers exactly (48.000000 and 4.000000, std=0, from a different
   Cl(10) code path than `build_cg.py`), but the additional
   multi-generator closure test it attempts does **not** cleanly close,
   for a specific, identified reason (a dagger-vs-transpose convention
   subtlety in the charge-conjugation-twisted bilinear transformation
   law — documented in the addendum, not papered over). **This item is
   left explicitly open, not marked resolved.**

### What this pass did NOT do

- Did not re-derive, alter, or re-check any number in
  `vertex_terms_resolved/RESULT_126_VERTEX_TERM_RESOLVED.md` or
  `yukawa_rge_system_assembled/RESULT_YUKAWA_RGE_SYSTEM_ASSEMBLED.md` —
  both were independently re-verified in the prior audit and found
  correct as written; no edits were needed there.
- Did not resolve the `C₂(16)` normalization disagreement (flagged in
  two places now, resolved in neither).
- Did not close the λ(120,10)/λ(10,120) multi-generator covariance test
  (partially attempted, left open with a named obstruction).
- Did not touch any file outside the Yukawa-RGE document set (`docs/`,
  `session_new_files/`, `audit report/`, phase `.py` files, etc.) — out
  of scope for this pass.
