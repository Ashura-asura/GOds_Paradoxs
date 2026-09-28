# LIST_OF_CORRECTIONS.md

Every item below was independently verified in this audit (re-run code,
or traced a document claim to its actual source) before being listed.
None reverses the project's central conclusion (0/19 derived, ~13 free
parameters); all are documentation/labeling/reproducibility fixes.

---

### C-1. Item 7's L1 label is wrong; its "computation" doesn't run

**Where:** `session_new_files/new_test_item7_s3_cohomology.py`,
`session_new_files/RESULT_item7.md`,
`docs/PHASE_R_HYPOTHESIS_BACKLOG.md` line 139 inline marker.

**What's wrong:** the `.py` file has a genuine `SyntaxError` (line 54,
unescaped apostrophe in a single-quoted string) and has never executed
successfully. Its printed "results" are a hand-typed transcript of a
GAP 4.15/HAP 1.74 session run outside this repository, not a live
Python computation. It is currently labeled `[DONE - session_new_files,
CLOSED NEGATIVE, L1]` in the backlog file and `[L1]` implicitly in its
own docstring header ("computed via GAP/HAP [L1]").

**Correction:** relabel to L2 ("verified against external computation,
not independently re-derived here") throughout, matching the standard
Item 6 already sets correctly (`new_test_item6_gresnigt_cl10_s3_verify.py`
is a real, from-scratch, independently-passing Python re-derivation and
is correctly labeled L2 for citing an external paper while still
computing everything itself). Fix the syntax error regardless, and
either (a) actually re-run the GAP session and include the `.g` script
and transcript in the repository, or (b) state explicitly in
`RESULT_item7.md` that this specific claim rests on an unreproduced
external computation.

**Underlying math status:** not thrown out — S3's group homology
(H₁=Z/2Z, H₂=0, H₃=Z/6Z) is standard and checks out against known
results for the symmetric group; the anomaly-vanishing argument for a
real/orthogonal 3-dim representation is sound reasoning. The correction
is about the label and the reproducibility trail, not the conclusion.

**Update (2026-08-01):** both remediation paths this correction called
for are now done. The syntax error is fixed (the file runs — confirmed
by re-running it before and after). Rather than (a) re-running the GAP
session, option (b)'s spirit was exceeded: the numbers were
independently re-derived by a different method entirely (an LHS
spectral sequence, every input checked by code, no GAP/HAP dependency)
in `session_new_files/item7_reverification_no_gap.py` and
`session_new_files/ITEM7_LHS_SPECTRAL_SEQUENCE.md`. The label is now
genuinely L1, not by relaxing the standard this correction set, but by
satisfying it.

---

### C-2. "3 generations" stated as an unqualified L1 headline fact in
four places, without the chain-dependency caveat that exists elsewhere
in the repository

**Where:** `README.md` line 79 (phase index), `docs/solution.md`
("genuinely solved" table), `docs/FINAL_AUDIT.md` line 11 ("What was
proved (L1)"), `docs/ALL_THEOREMS.md` (Theorem A2-1).

**What's wrong:** all four state "E8 248 → 3 generations" as a flat,
zero-free-parameter fact. `docs/ALL_DERIVATIVES.md` item 10 (same
repository, hand-derived using standard branching tables) shows a
different, equally standard E8 subgroup chain
(E8→SO(16)/Z2→SO(10)×SU(4)) gives **4** generations instead, and that
nothing in the algebra picks the E6×SU(3)_f chain over this one.
`phase_s_embedding_selection_check.py` independently confirms, for a
related question (which 3 of 10 color embeddings), that no natural
subgroup of S5 singles out a unique choice either — the same pattern.

**Correction:** add one sentence to each of the four locations:
*"...given the E6×SU(3)_f branching chain; a different, equally
standard chain (SO(10)×SU(4)) gives 4 generations instead, and the
algebra does not by itself select one chain over the other — see
`ALL_DERIVATIVES.md` item 10."* This does not withdraw the result, it
correctly scopes it — exactly the kind of "L1 rounded up past what it
actually shows" gap Rule 3 warns is this project's own most common
failure mode.

---

### C-3. Items 9, 10, 11, 42: backlog file shows them open; deeper doc
shows them done; neither file is labeled per Rule 3, and neither
cross-references the other

**Where:** `docs/PHASE_R_HYPOTHESIS_BACKLOG.md` lines 159–166, 345
(no `[DONE]` marker) vs. `docs/ALL_DERIVATIVES.md` lines 147–200,
302–314, 379–401, 405–465 ("COMPLETED" / "NOW COMPLETED" verdicts).

**What's wrong:** two authoritative-looking documents disagree on
whether four backlog items are open or resolved, and neither file is
labeled with the project's own L1/L2/L3 scheme for these four items
specifically (contrast `RESULT_item6.md`/`RESULT_item7.md`, which do
label). The analysis itself is fine (standard Slansky-table branching,
correctly applied by hand) — the correction is purely bookkeeping.

**Correction:** add `[DONE - ALL_DERIVATIVES.md, L2]` inline markers
to backlog items 9, 10, 11, 42, matching the style already used for
every other resolved item in that file, and add explicit L1/L2/L3
labels to the corresponding `ALL_DERIVATIVES.md` sections (all four
should read L2: standard representation theory, hand-verified against
tables, not independently coded).

---

### C-4. `docs/FINAL_AUDIT.md` header says "Project Closed 2026-07-27";
repository shows substantial work dated 2026-07-28

**Where:** `docs/FINAL_AUDIT.md` line 3.

**Correction:** update the header, or add a note pointing to
`README.md`'s 2026-07-28 addenda (Phases Q–X, `session_new_files/`,
the Item-1 intrinsic-Dirac test), so a reader who stops at
`FINAL_AUDIT.md` because it says "closed" doesn't miss nine more
phases of real work.

---

### C-5. Packaging: 7 files require manual `PYTHONPATH` fix to run

**Where:** `phase_a1_cl10_core.py`, `phase_l_su2r_check.py`,
`phase_m_reconciliation.py`, `phase_q_triality_verification.py`,
`phase_t_su2r_octonion_confirmation.py`, `phase_v_realtier_items.py`,
part of `phase_r_backlog_tests.py`.

**Correction:** add `import sys, os;
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..',
'support'))` (or equivalent) to the top of each, or add a
`pyproject.toml`/`conftest.py` so `support/` is always importable.
Purely a reproducibility fix; verified that all 7 produce their
documented output once the path issue is resolved.

---

### C-6. Phase C's own parameter table lists 23 rows while the project
states its target as "19" throughout

**Where:** `phases/phase_c_honest_accounting.py` output table (9 masses
+ 4 CKM + 4 PMNS + m_H + α_s = 19 listed rows, but the table actually
prints 19 rows total already only if PMNS is excluded — recheck showed
the printed table includes both CKM and PMNS rows, totaling more than
the conventional 19-parameter minimal-SM count); `README.md`,
`docs/FINAL_AUDIT.md`, `docs/solution.md` all state "19" as the target
without qualification.

**Correction:** either state explicitly that the working target
includes massive-neutrino/PMNS parameters (and revise "19" to the
correct total, ~23–26 depending on Dirac vs. Majorana convention), or
trim the accounting table to the conventional massless-neutrino 19 and
handle PMNS separately with its own explicit disclaimer. Either is
fine; the current silent mismatch is not.
