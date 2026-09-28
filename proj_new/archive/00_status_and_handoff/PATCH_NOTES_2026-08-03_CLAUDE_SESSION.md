# Patch notes — 2026-08-03 (external audit/fix session)

Two concrete, verified changes made to the repository this session. Nothing
about the science, status, or the 0/19 parameter count was touched — this is
infrastructure only, per Ground Rule "corrections filed as their own record,
not silent edits."

## 1. Fixed: sys.path bug in 7 phase files (`audit report/UPDATED_STATUS.md`
## item C-5)

Files under `phases below_Z_25/` used `sys.path.insert(0, ..., '..', '..',
'support')` — two levels up from that directory, which lands outside the
repo. Correct path is one level up (`'..', 'support'`). Fixed in:

- `phases below_Z_25/phase_a1_cl10_core.py`
- `phases below_Z_25/phase_l_su2r_check.py`
- `phases below_Z_25/phase_m_reconciliation.py`
- `phases below_Z_25/phase_q_triality_verification.py`
- `phases below_Z_25/phase_r_backlog_tests.py`
- `phases below_Z_25/phase_t_su2r_octonion_confirmation.py`
- `phases below_Z_25/phase_v_realtier_items.py`

**Verified:** all 7 now run to completion from a clean shell (no manual
`PYTHONPATH`) and print their previously-recorded results. No output changed
— this only fixes reproducibility, not any computed value.

## 2. Tooling gap closed: GAP+HAP and LiE

`docs/PHASE_R_HYPOTHESIS_BACKLOG.md`, `audit report/OPEN_PROBLEMS_AFTER_AUDIT.md`,
and the README repeatedly cite lack of "LiE/Sage/GAP-class" Lie-theory tooling
as a hard blocker (Item 15's SO(10)-126 branching sub-question, among others).
This was checked and found to be an environment gap, not a fundamental one —
both are ordinary `apt` packages (Ubuntu `universe`):

```
apt-get install -y gap gap-hap lie
```

Verified working:
- `gap` loads and `LoadPackage("hap")` succeeds.
- `lie` runs and correctly reports `dim(E6) = 78`.

**Not yet done:** the actual E6 ⊃ SO(10)×U(1) branching computation for Item
15's remaining sub-question. LiE's canned `res_mat` maximal-subgroup table
does not include D5 as a listed maximal subgroup of E6 (it's a full-rank
Borel–de Siebenthal subalgebra, found via the *extended* Dynkin diagram, not
the ordinary one `res_mat` indexes). Building that projection matrix by hand
without a cross-check would be exactly the kind of unverified Lie-theory
arithmetic Rule 4/9 warn against — flagged here as the precise next task
rather than attempted under time pressure.

### Suggested next step for whoever picks this up
1. Build the E6→D5×U(1) restriction matrix from the extended (affine) E6
   Dynkin diagram (delete the affine node, take `Cartan_type` of the
   remaining root subsystem, get its `fundam` basis).
2. Sanity-check it against the textbook branching of the **27**:
   27 → 16 + 10 + 1 under SO(10)×U(1). If that doesn't reproduce exactly,
   the matrix is wrong — don't trust it on the 83 higher candidates from
   `session_new_files/RESULT_item15.md` before this passes.
3. Only then branch the 83 tensor-cube candidates and check for a 126.
