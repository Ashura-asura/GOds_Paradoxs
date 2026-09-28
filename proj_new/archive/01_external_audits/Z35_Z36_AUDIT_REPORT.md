# Z35 + Z36 AUDIT REPORT — WHAT WAS FALSELY STATED, WHAT WAS MISSED, HOW CORRECTED

**Date:** 2026-08-03
**Trigger:** user request — "check the z35 and z36 if something are missed because meta ai generated and run the task for that .. and we only validated them"

---

## Method

For each phase: (1) dump the JSON artifacts and re-derive every reported statistic;
(2) check internal consistency of the JSONs (P_J == n_J/n, probabilities sum to 1);
(3) re-run the deterministic cross-check scripts; (4) re-run harness cells and compare
bit-for-bit against the stored artifacts; (5) look for pre-registered tasks with no results.

---

## Z36 — what was falsely stated and how corrected

Meta-AI produced `z36_experiment.py`, `z36_results.json`, `PHASE_Z36_REPORT.md` (33 graph rows).

| # | Stated (false / misleading) | Truth found in audit | Correction |
|---|------------------------------|----------------------|------------|
| 1 | "Theta=0 random regular => Aut=1, no channel active" (L2/L3 claim) | Row `RandomRegular_N16_d4_seed4`: Theta=0, twin_aut=1, but **Aut_exact=2** (twin-free Z2 involution) — 1 exception in 15 samples. The colored-quotient cap (qN>12 -> 1) hid the residual | Recorded in report Addendum: "1 exception in 15; quotient channel (uncapped) is what explains it" |
| 2 | JSON label `Complement_Shrikhande_16_80` | Row's own M=72 (complement of (16,48) has 120-48=72 edges); spectrum [9, 1^6, -3^9] correct | Addendum: name should read `Complement_Shrikhande_16_72` |
| 3 | Colored-quotient Aut reported as decomposition factor | For quotient N>12 the harness returned 1 (cap), silently hiding residuals there | Addendum: cap noted as limitation; does not affect Theta=0 rows where quotient=G |
| 4 | Random-regular rows look reproducible | `nx.random_regular_graph` seed semantics differ across networkx versions; those 15 rows are NOT cross-reproducible, only their internal VF2 counts vouch for them | Addendum: reproducibility caveat recorded |
| 5 | Causal diagram cites "P=1.0 DeltaTheta <=> J" | That number comes from the **parallel** z35 loose protocol (definitional tautology), not the exact protocol | Addendum: citation caveat — exact protocol gives P(dt>0|J)=0.998..1.000, P(J|dt>0)<1 |
| 6 | (implicit) decomposition is a new theorem | It is a restatement of phase_z35 Amendment 3 identity: |Aut| = prod|C_i|! * |Aut(colored twin quotient)| | Verified 18/18 shared graphs across tools; recorded as "restatement of Amendment 3", not merged |

**Verified TRUE (no correction needed):**
- Shrikhande=192, Rook=1152, Petersen=120, complement=192 — all Theta=0, twin-free, exact (capped=False)
- 14/14 Z25b attractors regenerated deterministically; `cross_check_attractors.py` rerun → **RESULT: 14/14 attractors fully consistent across tools** (Aut, Theta, twin_aut, Aut/twin == q_colored all PASS)
- All 33 rows present in JSON, matching the report table

---

## Z35 — what was falsely stated, missed, and how corrected

Meta-AI produced two protocol stacks: the exact-|Aut| main protocol (`z35_tie_collapse_theorem.py`,
`z35_results.json`, `PHASE_Z35_REPORT.md`) and a loose parallel run (`z35_experiment.py`,
`z35_summary.json`, `z35_results (1).json`, `PHASE_Z35_REPORT_PARALLEL_EXPERIMENT.md`).

| # | Stated (false / missed) | Truth found in audit | Correction |
|---|--------------------------|----------------------|------------|
| 1 | **Files section: "Earlier unrun draft (Rule-8 ledger): z35_twin_creation_law.py"** — implies the draft was documented in the Rule-8 ledger | Ledger entries 8.1-8.12 contain **NO entry** for the draft. The draft is a Rule-2 pre-registered protocol (2026-08-02, H1/H2/H3 MI on TwinGain, 450 chains at (10,15)) that was **never run and never ledged** | Ran it. Found 2 harness bugs (below), fixed, reran, saved `z35_twin_creation_law_results.json`, added ledger entry 8.13, fixed Files line |
| 2 | (implicit) draft's degree-variance analysis would work as written | Bug A: `degree_stats` summed/iterated the **dict returned by E.degrees()** (keys 0..N-1) → variance constant 8.25, `I_var=0.0000` artifact, single "low" var-bin. Bug B: `random_graph_same_deg(degrees,…)` received that dict → configuration-model null never built → `control_null_rate=null` | Fixed to `list(E.degrees(g).values())`. Post-fix: I_var=0.1502, P(TwinGain\|var) low 0.4014 / med 0.7252 / high 0.1872, null rate 0.2027 (vs observed 0.439, 2.17x lift). **Verdict MIXED** — I_tau=0.3762 > I_deg=0.2468; neither pre-registered 2x-gate winner (H1/H2/H3 all false) |
| 3 | Parallel report's "autmin kills mechanism (p_jump=0.0)" | True only for the **theta-minimizer** of the loose parallel protocol. Under the exact-|Aut| protocol, main-cell autmin still nucleates jumps: P_J=0.316, P(dt>0|J)=0.998 | Already recorded in ledger 8.6/8.7 before this audit; audit re-confirmed the distinction |
| 4 | Parallel report's "(14,28) p(J)=0.0027 suppression anomaly" | Does not reproduce under exact protocol: our (14,28) gives P(dt>0|J)=0.995..1.000, P_J=0.275..0.316 | Already ledger 8.7; audit re-confirmed from JSON |
| 5 | `PHASE_Z35_REPORT 2ND TEST.md` exists as a separate report | Byte-identical duplicate of `PHASE_Z35_REPORT_PARALLEL_EXPERIMENT.md` (MD5 equal) | Noted as duplicate file; no content correction needed |
| 6 | (draft design) complement control adds information | Complement twin-gain == observed (1.2266 == 1.2266) — **forced** by complement-invariance of the twin relation; the control is tautological | Recorded in results JSON interpretation; no correction of data needed |

**Verified TRUE (no correction needed):**
- `z35_results.json` fully internally consistent: P_J == n_J/n, P(dt>0)+P(dt=0)+P(dt<0)=1.0, P(dt>0|J)+P(dt=0|J)+P(dt<0|J)=1.0 in every cell/mode
- **P(dt>0|J) >= 0.933 in all 20 selector-cells** (min = 0.9328 entropy (8,12)); **P(dt<0|J)=0.000 everywhere**; rho_spearman 0.87-0.98
- tau_median grows with N: 5-7 (8,12), 7-12 main (10,15), 11 (12,20), 14-15 (14,28), 18-19 (16,32)
- Controls A/B/C1/C2 + decision match report (h1/h3 pass, h2 fail, ctrlA/B/C fail, ctrlC2 pass; outcome B)
- Control D: G1 P(jump t=0)=0.000 (0/212) PASS; G2 P(jump & dtheta<=0)=0.0311, all dtheta=0, P(dtheta<0|jump)=0.000 PASS; end |Aut| median 3,110,400
- Parallel artifacts: `z35_summary.json` and `z35_results (1).json` match the parallel/2ND-TEST report tables exactly (random p=0.1020/1520 jumps, lex 0.0914/681, entropy 0.0715/533, autmin 0/0, controls A/B/C, generalization 5 cells)
- `shrikhande_verification.json`: Shrikhande=192 SRG(16,6,2,2) confirmed; Rook=1152 same-parameter non-isomorphic; user-submitted graph Aut=1
- **Reproducibility:** re-ran the main harness cell (8,12) → stats and monotonicity **bit-identical** to stored JSON (all 4 modes x 6 fields match; 3.8s, cache-backed)

---

## Canon bug — third-party claim vs in-repo execution (2026-08-03)

This audit discovered the z25b `canon()` iso-invariance defect (Rule-8 #1/#2). A third-party agent
then claimed it fixed the canon in `audit_fixes/canon_fixed.py` and verified it. **That path had no
artifact in the repo** (chat-only = not a fix by project rules). The fix was then implemented
directly and the downstream numbers re-derived:

| Step | What | Result |
|------|------|--------|
| Root cause | old `canon()` mapped images to the class's OWN vertex-index set → iso copies search disjoint label spaces; asymmetric graphs returned their own labeling (56% EX-key mismatch on iso pairs) | 1395/2500 EX artifacts (ledger 8.14) |
| Fix | `z25b_engine_v2.canon` + `z25b_relational_engine.canon`: images → iso-invariant contiguous blocks by WL-color rank | applied, docstrings marked Rule-8 #1/#2 |
| Second latent bug | `_MEMO`/`_AUT`/`_KC` keyed on edges only, `wl_colors` is N-dependent (isolated vertices) → cross-N pollution (N=4 result reused at N=5). Caught by A/B vs independent reference | memo keys now `(N, ...)`; A/B 880 graphs 0 mismatches |
| Verification | 1000/1000 iso pairs (EX + all keys), 300/300 non-iso vs networkx, exhaustive relabel N≤7 (235,425 pairs 0 failures), brute-force oracle note | all pass; reference verification 0/1000 + 0/300 |

**Re-derived facts (before → after, all with the fixed canon, ledger 8.14):**

| Artifact | Before | After |
|----------|--------|-------|
| Z37 t1 V2 EX artifacts on iso successors | 1395/2500 | **0**/2500 (lex counterexamples 1105/2500 unchanged) |
| Z35 main (10,15) | n_steps 10137, P(J)_rnd 0.230, tau 8–10, **h2 FAIL** (I_J_theta 0.2436 < I_J_tau 0.2777) | n_steps 6329, P(J)_rnd 0.391, tau 7, **h2 PASS** (0.1929 > 0.1381); outcome B unchanged |
| Z35 controls | A, C1 unchanged (canon-free); B n 3106; C2 lex 0.243 | B n 2162, C2 lex 0.421 |
| Z35 other cells | (8,12): 2848 steps, tau 5–7 | (8,12): 1708 steps, tau 4–5; (12,20)/(14,28) ~unchanged; (16,32) random/lex/autmin **bit-identical** (n_J 299/149/76 unchanged), entropy n 453→451 (n_J 146 frozen) — tall sparse graphs are asymmetric with ~no iso-class revisits; only 2 extra labeled-state entropy steps were cut |
| Z35 Control D | G1 0.0, G2 0.0311 / 1029 jumps | G1 0.0, G2 0.0313 / 1022 jumps (gates still PASS) |
| Z35 twin law | 3911 steps; **I_tau 0.3762 > I_deg 0.2468**; varebin mid-peaked | 2569 steps; **I_tau 0.1188 < I_deg 0.2227**; varebin monotone 0.258/0.793/0.834 |
| Z33 (10,15) | tau 12/9/8/8; entropy fold 48 | tau 7/7/7/6; folds all 1440 |
| Z26 entropy / Z27 Polya | H_out log2 12; 136,433 / 12,005,168 asserted | unchanged (quotient counts canon-independent) |

## Missed tasks found and executed

| Task | Status before audit | Executed | Results |
|------|---------------------|----------|---------|
| z35 twin-creation-law protocol (`z35_twin_creation_law.py`, pre-registered 2026-08-02) | never run; no ledger entry | RUN (post bug-fix) | 3911 transient steps, 1717 TwinGain>0 (rate 0.439); H_T=0.9892; I_tau=0.3762, I_var=0.1502, I_rep=0.0966, I_deg=0.2468, I_joint=0.5961; I_tau_given_deg=0.3494, I_deg_given_tau=0.2199; verdict **MIXED**; config-model null 0.2027 vs observed 0.439 (2.17x) |
| z36 cross-check | validated once before | re-verified | 14/14 attractors consistent across tools; 18/18 shared graphs agree |

## Files written/amended by this audit

- NEW `phase_z35/z35_twin_creation_law_results.json` — full run record, bugfix notes, interpretation
- AMENDED `phase_z35/PHASE_Z35_REPORT.md` — Rule-8 ledger entry 8.13 added; Files section corrected (draft is now "audited + run + recorded in ledger 8.13" with results file, not "Rule-8 ledger")
- AMENDED `phase_z35/z35_twin_creation_law.py` — 1-line bugfix in `degree_stats` (dict values)
- Z36 corrections already recorded in `phase_z36/PHASE_Z36_REPORT.md` Addendum (2026-08-03) — re-confirmed by this audit

## Bottom line

- **No false statistic survived in either phase's final artifacts.** Every number in
  `PHASE_Z35_REPORT.md` and `PHASE_Z36_REPORT.md` (plus Control D and the parallel run) was
  re-derived from the JSON and matches. The z35 main harness reproduces its own results bit-for-bit.
- **The canon() bug was then actually fixed in-repo** (not chat-only) and verified. ALL
  canon-keyed downstream numbers were re-derived (ledger 8.14). Consensus: outcome B unchanged;
  H1/H2/H3 now ALL pass; concentration < generation intact. Two facts corrected: the H2 gate
  FAIL→PASS, and the twin-law I_tau/I_deg ranking flipped (degree variance now dominates).
- **Remaining caveats** (unchanged, documented): Z36 random-regular rows are version-dependent;
  Z36 colored-quotient cap hides residual for qN>12. The old Z35 "tau = labeled-state upper
  bound" caveat is RESOLVED — tau is now a true iso-class revisit time (iso-invariant canon).
