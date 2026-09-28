# SESSION REPORT — Phase Z23 external session (WSL toolchain)

Date: 2026-08-02
Scope: Tasks A–G of the Phase Z23 external session, run per GROUND_RULES.md v2
(Rules 1–9; L1/L2 labels; Rule 6 no free parameters; Rule 8 structural
failure = result; Rule 9 discriminating power checked per task).
Overall status: **0/19** — no phase-claim resurrected, no new physics; the
tooling gap is closed and the 3-generation structure is now fully computed,
not cited.

## Tooling established (new capability, previously the project's oldest debt)
- GAP 4.15.1 + HAP (WSL Ubuntu) — group enumeration, character tables.
- LiE 2.2.2 (WSL) — regular subalgebra branchings via closure/res_mat/branch/dim.
- SageMath 10.9 (conda-forge, package `sage`; `sage -c` verified; earlier
  `sagemath` attempt failed and is logged).
- Python 3.13 + numpy/sympy (exact Rational/Fraction arithmetic) for
  root-system and anomaly computations.
- Debug trail (reserved words, non-callable class functions, LiE rm
  conventions, non-regular embeddings) documented in the task files.

## Tasks and verdicts
- **Task A (closed):** Gresnigt's un-averaged H_alpha/H_beta reproduced
  exactly (eqs. 73, 139/141); Gram diag(1/2, 9/8, 9/8); trace-free spectra;
  psi_3 = exact 120° rotation (real 2-dim S3 irrep); negative result:
  Mbar NOT in span(M_alpha, M_beta) — symmetric point unreachable from the
  S3-breaking subspace; E8 plays no role.
- **Task B (closed):** the family group is forced: among all 311 groups of
  order 2..60, exactly S3 survives the four criteria (plane rep, psi_3,
  2:1:1 reflection, faithful on 3 points). Bound-independent via criterion (iv).
- **Task C (closed):** all cited E8 branchings now computed from the root
  system: E8->E6xA2 248 = (78,1)+(1,8)+(27,3)+(27bar,3bar) (two independent
  verifications); 3875 (no 27bar — asymmetry); E8->E7xA1; E8->D8->D5xA3
  ("4 generations" reading confirmed).
- **Task D (closed):** E6 27^3 = 1+2925+2(78)+3(650)+2(5824)+3003; contains
  exactly **3 x SO(10) 126 at charge -6, 0 x 126bar**.
- **Task E (closed):** SO(10) 126 -> SU(5)xU(1) -> SM: 45 submultiplets,
  all dim-verified, exact hypercharge tracelessness; key content (1,3,-1)
  Majorana triplet, singlets (1,1,-1),(1,1,2),(1,1,0), NO (3,2,1/6); 126 is
  complex; 16x16 = 10+120+126 cross-check exact; Pati-Salam route not
  LiE-computable (documented).
- **Task F (closed):** E8 -> F4xG2 (audit B6): 248 = (52,1)+(1,14)+(26,7)
  forced by weight counting; audit guess "26 = 16+10" structurally dead
  (rank; actual content 9+16+1); "7 = 3+3+1" true as 3+3bar+1 (conjugate
  pair, no chiral structure). B6 confirmed N/A.
- **Task G (closed):** E6xSU(3)_f consistency of (27,3): A(27) = -2 != 0;
  A(16) = 0 (each generation anomaly-free); standalone chiral (27,3)
  excluded (E6^3 = -6, SU(3)_f^3 = 27); actual E8-adjoint content
  (27,3)+(27bar,3bar) anomaly-free in every channel — no extra matter.

## Cumulative picture (what is now established)
- The "3 generations" chain E8 -> E6xA2 -> E6 -> SO(10)xU(1) -> SM is fully
  computed: (27,3) carries three 27s; each contains a 16bar (anomaly-free);
  the 126 (Majorana-capable) appears 3x in 27^3 with no 126bar.
- The family group S3 is unique under the geometric criteria; it appears
  as the symmetry of the generation plane (Task A/B), NOT as a gauged
  group added by hand.
- Every anomaly channel is safe exactly because the content is the E8
  adjoint; no hand-added conjugate sector is needed.
- Chain selection is still open (E6xA2: 3 generations; D8->D5xA3: 4;
  3875 asymmetry in the E6xA2 chain). This was NOT resolved this session —
  it was not in scope (Tasks A–G are verification of the stated items).

## Open items (unchanged, outside this session's scope)
1. Chain selection among maximal chains (3 vs 4 generations reading).
2. VEV dynamics / mass ratio predictions (Item 6-style discriminators).
3. Independent cross-check of the E6->SO(10) 126-in-27^3 by a second
   method (GAP/LiE non-regular routes) if a tool becomes available.

## Files
- Result files: RESULT_task_a_orthogonal_higgs_directions.md,
  RESULT_task_b_family_group.md, RESULT_task_c_e8_branching.md,
  RESULT_task_d_e6_cubic_so10.md, RESULT_task_e_126_sm.md,
  RESULT_task_f_f4g2.md, RESULT_task_g_e6su3_anomaly.md (all in
  session_new_files/phase_z23_external_session/).
- Scripts: tmp_task_a*.py, tmp_task_b_*.g, tmp_task_c/d*.lie|.py,
  tmp_task_e_*.lie, tmp_task_f_firstprinciples.py, tmp_task_g_anomalies.py
  (same directory).
- README.md: preservation notes for Task A, Tasks C/D, Tasks B/E/F/G
  (additive; nothing above each note altered). CHANGELOG.md: entries
  added at top for each group.
