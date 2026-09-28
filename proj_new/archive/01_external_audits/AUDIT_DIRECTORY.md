# AUDIT_DIRECTORY.md — Phase 1: Directory / Documentation Audit

Repository: `Gods_Paradox_FINAL/` (from `Gods_Paradox_FINAL_v5.zip`)
Method: full recursive listing (`find . -type f`), then every `.py` file
was executed, and every claim of "DONE" was traced back to its source
file before this audit accepted it.

## 1. Actual structure (verified, 56 files)

```
GROUND_RULES.md, README.md
docs/            11 files (10 .md + 1 .pdf)
phases/          24 .py files (A1, A2, B–X = 24 phases)
session_new_files/ 5 .py + 6 .md
support/         2 .py
tests/           6 .py
```
This matches the folder tree README.md describes. No missing top-level
folders, no orphaned top-level files.

## 2. Packaging bug (affects reproducibility of Phase 3 below)

**Finding D-1 (real, verified).** 7 of the 24 phase files, plus one
`session_new_files` file and part of `phase_r`, import
`from qosc_division_connection import build_octonion_structure_constants`
with no `sys.path` handling. `qosc_division_connection.py` lives in
`support/`, one directory over. Run any of these files directly
(`python3 phases/phase_a1_cl10_core.py`, the way a reader following the
README would run it) and it crashes immediately with
`ModuleNotFoundError`, before printing a single result line.

Affected: `phase_a1_cl10_core.py`, `phase_l_su2r_check.py`,
`phase_m_reconciliation.py`, `phase_q_triality_verification.py`,
`phase_t_su2r_octonion_confirmation.py`, `phase_v_realtier_items.py`,
and the Item-32 associator section of `phase_r_backlog_tests.py`
(the rest of `phase_r` runs fine before hitting it).

This is **not** a mathematical error — every one of these files runs
clean and reproduces its documented output once `support/` is put on
`PYTHONPATH` (verified in Phase 3 below) — but as shipped, roughly a
third of the "run it yourself" claims in this repo are not actually
one-command reproducible. README never mentions this dependency. This
should be fixed with a two-line `sys.path.insert` at the top of each
affected file, or a `setup.py`/`pyproject.toml`.

## 3. Genuine code defect

**Finding D-2 (real, verified).** `session_new_files/new_test_item7_s3_cohomology.py`
line 54 has an unescaped apostrophe inside a single-quoted string
(`print('   => ZERO 't Hooft anomaly...')`), which is a Python
`SyntaxError`. **This file has never successfully executed in the form
it was shipped in.** See Finding C-1 in `LIST_OF_CORRECTIONS.md` for
why this matters beyond a typo — the file's actual content is a
hardcoded transcription of an external GAP session, not a live
computation, and the fact that it doesn't even parse means it was never
run end-to-end after being written, in any environment.

## 4. Documentation vs. actual repository state

**Finding D-3 (real, verified) — stale "Project Closed" header.**
`docs/FINAL_AUDIT.md` opens with `## 2026-07-27 | Project Closed`. The
repository demonstrably did not close on 2026-07-27: Phases Q through X
(9 more phases), all of `session_new_files/` (4 more backlog items run
with GAP/HAP), and `tests/new_test_intrinsic_dirac_root_coupling.py`
are all dated 2026-07-28, one day later, and are substantive (Phase X
in particular is the most technically careful file in the repo — see
Phase 3). A reader who stops at `FINAL_AUDIT.md` because it says
"Project Closed" misses everything from Phase Q onward. The header is
stale documentation, not a lie about results — but it is misleading as
written and should be corrected or dated.

**Finding D-4 (real, verified) — backlog tracking file not updated for
items 9, 10, 11, 42.** `docs/PHASE_R_HYPOTHESIS_BACKLOG.md` is the
file README explicitly designates for tracking which backlog items are
done (`[DONE - Phase R]`, `[DONE - Phase U]`, `[DONE - session_new_files]`
markers throughout). Items 9, 10, 11, and 42 carry **no** such marker —
they read as fully open, `[real]`-tier, untouched.

But `docs/ALL_THEOREMS.md`... no — `docs/ALL_DERIVATIVES.md` contains
explicit "COMPLETED" / "NOW COMPLETED" / "RECHECK: COMPLETED" verdicts
for exactly these four items (lines 147–200, 302–314, 379–401, 405–465).
The analysis is real and its conclusions are consistent with the rest
of the repo (see Phase 4 below), but:
- `ALL_DERIVATIVES.md` is **not** in README's "read in this order" list
  (only items 1–5 are; `ALL_DERIVATIVES.md` appears solely in the
  folder-tree diagram, easy to miss).
- The backlog file, which is the one place a returning reader is told
  to check for item status, was never annotated to point to it.
- There is no `.py` file backing items 9, 10, 11, or 42 — "COMPLETED"
  here means "reasoned through by hand in a markdown file," using
  standard textbook branching rules (Slansky 1981), not "computed and
  verified with code" the way the phases/ files are. `ALL_DERIVATIVES.md`
  does not consistently apply Rule 3 L1/L2/L3 labels to these four items
  (contrast with `session_new_files/RESULT_item6.md` and
  `RESULT_item7.md`, which do label). This should be L2 (external/
  standard representation theory, hand-verified, not independently
  coded) for all four, not left unlabeled.

**Net effect of D-4:** a reader can genuinely come away thinking items
9/10/11/42 are still open (backlog file) or that they were resolved
with the same rigor as the coded phases (nothing tells them
otherwise). Neither is quite right. See `LIST_OF_CORRECTIONS.md`.

**Finding D-5 (minor, verified) — duplicated item-15 filenames.**
Two different files both address backlog item 15 under similar names:
`tests/new_test_item15_e6su3_branching.py` and
`session_new_files/new_test_item15_e6_tensor_full.py`. They test
different sub-questions (E6×SU(3)_f branching vs. the full 27⊗27⊗27
tensor decomposition) and both run correctly, so this is not a
conflict — but the near-identical names invite confusion and are not
cross-referenced from one file to the other.

## 5. Referenced-but-absent / absent-but-unindexed files

- No files were found referenced in any `.md` that do not exist on disk
  (checked every `phase_*.py`, `RESULT_item*.md`, and `*.g` GAP-script
  reference — the `.g` scripts referenced in `RESULT_item*.md` files as
  having been run externally, e.g. `item7_29_v2.g`, are **not** included
  in this archive; this is expected, since they ran on GAP outside this
  environment, but it means those specific results are not independently
  reproducible from this zip — see Phase 3 caveat below).
- `docs/GODS_PARADOX_FINAL.pdf` exists and is generated by
  `support/generate_pdf.py`; not independently regenerated/diffed
  against the current `.md` sources in this audit (out of scope — it is
  a rendering of existing content, not a separate claim source).
- `docs/Gods_paradox-Book.txt` is a narrative/popular write-up; treated
  as non-authoritative relative to the phase files and `docs/` per
  GROUND_RULES.md's own priority (code > math > written claims).

## 6. Summary

No missing directories, no dangling file references, no fabricated
citations found in this pass (the one literature citation spot-checked,
Gresnigt arXiv:2601.07857, is real — confirmed by web search, see
Phase 3). The defects found are: one packaging bug (D-1), one file that
has never run (D-2), one stale status header (D-3), and one tracking
file that was never updated to reflect real work done elsewhere (D-4).
None of these change the project's mathematical bottom line, but D-3
and D-4 are exactly the kind of "documentation error vs. actual
repository contents" mismatch Phase 1 was asked to catch.
