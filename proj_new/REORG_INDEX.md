# Reorganization Index — old path → new path

The live thread is untouched in content, just relocated:

| Old | New |
|---|---|
| `MASTER_ROADMAP.md` | `ACTIVE_phase_S/MASTER_ROADMAP.md` |
| `PROJECT_STATE_HANDOFF.md` (top level) | `ACTIVE_phase_S/PROJECT_STATE_HANDOFF.md` |
| `phase_S0_prior_art_lock/` … `phase_S5_external_contact/` | `ACTIVE_phase_S/phase_S0_prior_art_lock/` … `phase_S5_external_contact/` (unchanged) |

Everything else (`archive_pre_S/`) is regrouped by theme instead of by
flat phase-letter, since the phase letters weren't in a single
consistent sequence to begin with (A–Y, then Z1–Z100+, then R3/R5–R8
interleaved, plus three separately-named session-log folders):

| Old (`archive_pre_S/...`) | New (`archive/...`) |
|---|---|
| `ARCHIVE_INDEX.md`, `PROJECT_STATE_HANDOFF.md`, `README.md`, `GROUND_RULES.md`, `CHANGELOG.md`, `RELATED_WORK.md`, `FINAL_AUDIT.md`, `CANON_FIX_FULL_REPORT.md`, `PATCH_NOTES_...md`, `latest_progress_report.md`, `kilo.json`, `canon_fixed*.py`, `verify_canon_fix.py`, `pathfix.py` | `00_status_and_handoff/` |
| `"audit report"/*.md`, `Z35_Z36_AUDIT_REPORT.md` | `01_external_audits/` |
| `"phases below_Z_25"/*.py`, `support/`, `tests/`, `docs/RESULT_Z2_TASK*`, `docs/PHASE_Z1*`, `docs/PHASE_Z2*`, `docs/PHASE_Z_*`, `docs/PHASE_Z24*`, `docs/AUDIT_Z2_INITIAL_STATE.md`, `docs/ALL_THEOREMS.md`, `docs/ALL_DERIVATIVES.md`, `docs/POST_AUDIT_TARGET.md`, `docs/solution.md`, `docs/adversarial_audit_2026.md`, `docs/MECHANISM_FAILURE_MAP.md`, `docs/RESEARCH_ROADMAP.md`, `docs/FINAL_AUDIT.md` | `02_foundational_phases_A_to_Y/` (`docs/FINAL_AUDIT.md` renamed `FINAL_AUDIT_docs.md` to avoid clashing with the top-level one) |
| `docs/100_PLUS_HYPOTHESES.md`, `docs/PHASE_R_HYPOTHESIS_BACKLOG.md`, `docs/PHASE_W_FULL_SWEEP.md`, `purposed_hypo_mechanism.md` | `03_hypotheses_and_backlog/` |
| `session_new_files/*` (Z3–Z24 results, Items 1/5/6/7/15/29, Phase Z23 external session, phase_z22_gresnigt_import/, phase_z24_free_parameter.../) | `04_spectral_triple_generation_sessions/` (duplicate nested `support/` dropped — see AUDIT_REPORT §0) |
| `phase_r3_s3_forced_test/`, `phase_r5_sedenion_selector_audit/`, `phase_r6_generation_branch_selection/`, `phase_r7_octonionic_realization_selector/`, `phase_r8_octonion_e8_lift_feasibility/`, `phase_z39_e8_cubic_obstruction/`, `phase_z40_generation_cl_entanglement_test/`, `phase_z42_joint_intrinsic_constraint/`, `phase_z44_su5xsu5/` (un-nested) | `05_octonion_e8_branch_selectors/` |
| `phase_z25/` … `phase_z38/`, `phase_z100/`, `phase_z100_closure/` | `06_graph_dynamics_Z25_to_Z100/` |
| `docs_new/`, `vertex_126_external_completion/`, `vertex_terms_resolved/`, `yukawa_rge_system_assembled/`, `RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md`, `SESSION_RESULT_DYNAMICAL_VACUUM_SELECTION_TASKS_1_6.md`, `archive/docs_new__RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md` | `07_yukawa_rge_thread/` (last one renamed `archived_duplicate__RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md`) |
| `docs/Gods_paradox-Book.txt`, `docs/GODS_PARADOX_FINAL.pdf` | `08_supporting_longform_docs/` |
| `results/` (empty) | dropped — see AUDIT_REPORT §0, item 3 |

See `AUDIT_REPORT.md` for the phase-by-phase content audit.
