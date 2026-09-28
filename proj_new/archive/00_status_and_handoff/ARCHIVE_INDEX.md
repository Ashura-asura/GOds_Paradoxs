# Archive Index — Everything Before Phase S

Full prior project (Phases A-Z100+, R5-R10), moved here unmodified on
2026-08-03 when the project was restructured around the gated Phase S
roadmap (see `../MASTER_ROADMAP.md`). Status at time of archiving: 0/19 SM
parameters derived. Nothing in this archive was deleted or edited.

## If you only read a handful of files in this archive, read these
(pulled out because they were specifically confirmed, cross-checked, and
directly inform Phase S -- see MASTER_ROADMAP.md for how each is used)

- `PROJECT_STATE_HANDOFF.md` — full running log of every phase's result,
  in the project's own words, chronological.
- `phase_r8_octonion_e8_lift_feasibility/feasibility_report.md` — correctly
  identifies J3(O) as the missing ingredient for octonion-to-E8 lift, and
  correctly distinguishes that question from the Distler-Garibaldi no-go
  (which does not apply to this project's construction).
- `phase_z42_joint_intrinsic_constraint/` — the Z42 result: E8's SU(3)_f
  content restricted to {1,3,3bar,8}, and via Weyl's 1939 First Fundamental
  Theorem for SU(3) invariants, no order of E8 structure constants can
  produce a generation-space invariant beyond delta/epsilon. Real, correctly
  derived, cross-verified via Monte Carlo -- but independently re-derives a
  premise already standard in the SU(3)-family-symmetry model-building
  literature (see Phase S0's table). Not novel, but not wrong.
  `scripts/z42_invariant_search.py` is a good example of the project's
  better computational-verification practice worth carrying into Phase S3.
- `phases below_Z_25/phase_q_triality_verification.py` — the project's own
  honest correction of an earlier overclaim ("3 by triality" in Phase A1),
  confirmed with a real computed Z3 automorphism, and correctly identified
  as unrelated to the generation-counting SU(3)_f index. Good example of the
  self-correction discipline worth keeping.
- `phases below_Z_25/phase_a1_cl10_core.py` and `phase_a2_e8_core.py` — the
  core constructions everything else builds on. Phase S1/S2 will likely
  reuse phase_a1's 32-dim Fock space directly.
- `session_new_files/phase_z23_external_session/tmp_task_c_sage_crosscheck.py`
  — example of real independent cross-verification (exact rational
  arithmetic, Sage cross-check), the practice Phase S3 formalizes as a gate.

## Everything else
The remaining ~90+ phase directories are preserved for reference but were
not re-audited individually when this restructuring happened. Many contain
correctly-scoped negative results (search PROJECT_STATE_HANDOFF.md for
"DO NOT re-attempt" and "closed" to find them quickly) that are worth
checking before re-opening any adjacent question in Phase S.
