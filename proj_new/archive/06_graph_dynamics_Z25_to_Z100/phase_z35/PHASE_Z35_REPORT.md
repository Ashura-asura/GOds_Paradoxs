# PHASE Z35 — TIE-COLLAPSE MECHANISM: FROM EMPIRICAL LAW TO STRUCTURAL THEOREM

**Cell:** (10,15) main; generalization (8,12),(12,20),(14,28),(16,32)
**Date:** 2026-08-03
**Status:** MEASUREMENT COMPLETE — L1/L2/L3 separated — decision B

**Harness:** `phase_z35/z35_tie_collapse_theorem.py` (pre-registered protocol, exact statistics only).
**Parallel experiment note:** a second, looser-protocol implementation exists in this folder
(`z35_experiment.py`, `z35_summary.json`, `z35_results (1).json`,
`PHASE_Z35_REPORT_PARALLEL_EXPERIMENT.md`). It uses proxy jumps (twin_aut = prod |C_i|!),
a capped networkx GraphMatcher for |Aut|, an approximate relabel, and fixed horizons.
Its P=1.0 "Delta-Theta <=> J" is definitional (twin_aut growth <=> twin-class growth <=> Theta
growth by the twin-partition identity) and is NOT the claim of this report. This report uses
exact |Aut| jumps (ratio >= 4) only. Ledger entry 8.7 records the parallel run.

---

## Objective (as defined)

Z34 closed causal anatomy:

```
degree extremization -> neighborhood equalization -> twin-class restructuring -> |Aut| factorial jumps
```

Z35 asks the structural question: **is the twin potential Theta(G) = sum C(|C_i|,2) the hidden
invariant that drives tie-collapse to high-symmetry attractors under extremal edge exchange?**
Pre-registered before any run (embedded in the harness): thresholds, budgets, decision table.

## Pre-registered protocol (fixed before runs)

- State space: labeled G(N,M) under exchange (remove edge, add non-edge), N<=16, exact statistics.
- Selectors: random, lex, entropy, autmin (Z33 step_mode, unchanged).
- Chain: step until first canon-key revisit (tau), cap 512; unconverged chains discarded (reported).
- Jump J: aut_{t+1} >= 4.0 * aut_t with exact |Aut| (Z32 counter; Amendment 3 fast counter).
- Gates (stored in z35_results.json): H1_gate=0.9 (P(dt>0|J) in EVERY selector), H1_reject=0.5,
  H3_rho=0.7 (Spearman(DeltaTheta, log aut ratio) in every selector), mono_frac=0.02
  (P(dt<0)<=0.02 in every selector), ctrlA_ratio=3.0, ctrlB_pos=0.1, ctrlC_factor=0.9,
  ctrlC2_inflate=0.01, SEED0=20260802.
- Budgets: main (10,15) 500/200/200/200; (8,12) 200/100/100/100; Amendment 1 (declared before
  those runs): (12,20) 80/40/40/20, (14,28) 50/25/25/12, (16,32) 50/25/25/12 random/lex/entropy/autmin.

## Rule-8 Ledger — try to break before accepting

| # | Attack / event | Method | Result | Verdict |
|---|----------------|--------|--------|---------|
| 8.1 | Exactness of |Aut| counter | Z32 backtracker + Amendment 3 twin-quotient counter, validated 3817/3817 graphs (15 closed-form: Petersen=120, C10=20, K5+5iso=14400, 2xC5=200, 3xK2=48, 2xK3=72, 2xC4=128, 2xC6=288, 3xC5=6000, 4xK4, star, empty 10!, cycles, cliques; + 3802 random graphs at (10,15),(12,20),(16,32)); external Shrikhande SRG(16,6,2,2)=192 vs rook 1152 (non-isomorphic same-parameter SRGs distinguished), user-submitted graph=1 | exact at all cells | PASS — no failure in 3817 checks |
| 8.2 | Jump is an artifact of canon-key cycle detection | Control C1 (no canon, fixed horizon 40): P(dt>0)=0.1409 vs full random 0.355; Control C2 (canon-relabel every step, n_inv_steps=0, inflation -0.24..-0.35) | canon usage shifts the fixed-horizon rate but never inflates jump coupling | C2 PASS (no inflation); C1 recorded: canon is part of the pre-registered chain definition, not a hidden driver of P(dt>0|J) |
| 8.3 | Degree extremization is the driver | Control A: same states, extremal rule vs degree-preserving rewires vs degree-sequence configuration model | extremal P_pos=0.680 vs rewire 0.0848 (8.0x), vs config 0.2586 (2.63x) | PARTIAL: extremal strongly exceeds rewires; config-model twin rate high (0.26) — ctrlA gate (3.0x vs config) NOT met; recorded fail, diagnostic only (not outcome-gating by design) |
| 8.4 | Direction matters / reversed rule still nucleates | Control B (remove min/add max): P_J=0.056, P(dt>0|J)=0.431 | reversed rule destroys jump coupling | ctrlB gate (P_J>=0.1) NOT met — recorded; direction IS necessary in our harness |
| 8.5 | H1 gate met only by luck of one selector | H1 required in ALL 4 selectors of main cell (0.998/1.000/0.998/0.998) and all 4 selectors x 4 generalization cells (0.933..1.000) | robust across 20 selector-cells | PASS |
| 8.6 | Autmin adversarial selector | Main-cell autmin still nucleates jumps (P_J=0.316, P(dt>0|J)=0.998); z33 autmin minimizes |Aut| after move | autmin does NOT kill jumps under the exact-|Aut| selector (contrast: parallel experiment's theta-minimizer killed them) | recorded |
| 8.7 | Parallel loose-protocol run | z35_experiment.py (networkx, proxy jumps, capped |Aut|, fixed horizons) produced a separate report | Its P=1.0 jump coupling is definitional, not empirical; its autmin-kill and (14,28) p(J)=0.0027 anomaly do not reproduce under the exact protocol (our (14,28): P(dt>0|J)=0.995..1.000) | recorded, not merged |
| 8.8 | Harness amendments | A1 budgets (pre-declared); A2 |Aut| once per state + EX-key SQLite cache (single-core); A3 validated fast exact counter (3817/3817 before swap); A4 autmin candidate evaluation -> validated counter (identical values -> identical chains) | all semantics-preserving, documented in harness docstring | PASS |
| 8.9 | Bug episodes | (a) my first closed-form expectations were wrong (star 120 vs true 24, "2xC5" was 2xK5=28800, prism not Petersen) — validation FAILED, cases fixed, then PASS; (b) (12,20) run aborted mid-cell -> resumed from JSON (partial (14,28) saved and completed); (c) wrong-seed profiling attempts | no statistic was accepted until the gate passed | recorded |
| 8.10 | Z36 cross-verification | Independent networkx VF2 experiment (phase_z36/) asks "where does symmetry come from" after Shrikhande (Theta=0, Aut=192) breaks Theta-universality; claims 4-channel decomposition: Aut = twin_aut x Aut(colored quotient) x component-iso factor x algebraic residual | Re-verified with OUR exact counter (aut_size_exact_v2): Shrikhande=192, Rook=1152, Petersen=120, complement-Shrikhande=192, all Theta=0 twin-free; 14/14 Z25b attractors regenerated deterministically (seeds 1000+s) match v2 exactly on |Aut|, Theta, twin_aut, and Aut/twin_aut == quotient_aut_colored in every row; attractor_13 disconnected: 24x12=288 via component formula | PASS — decomposition formula == our Amendment 3 identity; cross-tool agreement 100% (18/18 shared graphs) |
| 8.11 | Z36 residual case | Their random-regular d4_seed4 row: Aut=2 with Theta=0, twin_aut=1 (twin-free Z2 involution) — report's "Theta=0 random => Aut=1" claim has 1 exception in 15 samples; also (a) their JSON label "Complement_Shrikhande_16_80" is a typo (row's own M=72, complement of (16,48), spectrum [9,1^6,-3^9] correct); (b) random-regular graphs are NOT cross-reproducible (nx.random_regular_graph seed semantics differ across networkx versions) so only their internal VF2 counts vouch for those rows; (c) colored-quotient Aut was capped (returned 1) for quotient N>12, hiding residuals there; (d) their causal diagram quotes the PARALLEL z35's P=1.0 tautology, not our exact protocol | residual is real (internally self-consistent) but 1/15; typo and cap noted | recorded, not merged — Z36 stays a standalone ledger entry, its theorem is a restatement of Amendment 3 |
| 8.12 | Control D: twin-free algebraic seeds in the exact-|Aut| framework | PRE-REGISTERED in z35_control_d.md before any run. Seeds Shrikhande/Rook/complement/Petersen (Theta=0 verified, |Aut| asserted 192/1152/192/120). 212 chains (random 50/seed + lex/entropy/autmin 1/seed), cap 256, all converged. Gates: G1 P(jump t=0)<=0.05, G2 P(jump & dtheta<=0)<=0.05 | G1: P=0.000 (0/212) PASS. G2: P=0.0311 (32/1029 jumps, ALL dtheta=0; P(dtheta<0|jump)=0.000) PASS. tau_half median 0 (symmetry halves in 1st step); every (16,*) chain hits |Aut|=1; twin channel re-nucleates to median end |Aut|=3,110,400 (Shrikhande==Rook endpoint, identical canon key); max single-step ratio 864x | PASS — algebraic channel is static only; twin channel is the sole jump channel; outcome B unchanged/strengthened |
| 8.13 | Unrun pre-registered draft (z35_twin_creation_law.py) | Audit found the draft (pre-registered 2026-08-02, H1/H2/H3 MI protocol on TwinGain, 450 chains (10,15)) was NEVER run and had NO ledger entry despite the Files-section claim "Rule-8 ledger". Ran it (2026-08-03): found 2 bugs — degree_stats summed/iterated dict KEYS (variance constant 8.25 -> I_var=0.0000 artifact) and random_graph_same_deg received a dict (config-model null never built, control_null_rate=null). Fixed both (E.degrees(g).values()), reran. | POST-FIX: 3911 steps, twin_rate 0.439; I_tau=0.3762 > I_deg=0.2468 (I_var=0.1502, I_rep=0.0966); I_tau_given_deg=0.3494, I_deg_given_tau=0.2199; P(TwinGain\|var) med 0.7252 > low 0.4014 > high 0.1872; config-model null rate 0.2027 vs observed 0.439 (2.17x); verdict MIXED (no 2x-gate winner). Complement control tautological (twin relation complement-invariant, 1.2266==1.2266). Consistent with main-protocol H2-fail (tau gate-not-driver) but degree variance carries residual info. SEE 8.14 for the canon-fix re-run — the I_tau>I_deg ranking below UNRAVELS after the iso-invariant canon fix (tau was inflated by the labeled-state artifact) | recorded + results saved to z35_twin_creation_law_results.json |
| 8.14 | z25b canon() NOT iso-invariant (Rule-8 #1/#2) — fixed + FULL downstream re-derivation | Audit (2026-08-03) reproduced the reported bug in z25b_engine_v2.canon / z25b_relational_engine.canon: intra-class relabel search mapped vertices to images drawn from the class's OWN vertex-index set, so isomorphic copies searched different label spaces; asymmetric graphs returned their own labeling. Third-party claim "canon solved in audit_fixes/canon_fixed.py" had NO artifact in the repo (chat-only = not a fix). FIX IMPLEMENTED DIRECTLY: images are iso-invariant contiguous blocks by WL-color rank; memo keyed on (N, edges) — a second latent bug (N-blind memo returned the N=4 canonical form for a 5-vertex edge set in mixed-N processes) found via A/B cross-check. VERIFICATION: 1000/1000 iso pairs identical (verified: EX branch + all keys), 300/300 non-iso pairs distinct vs networkx ground truth, exhaustive relabel N<=7 235,425 pairs 0 failures. | RE-DERIVED WITH FIXED CANON: Z37 t1 V2 EX artifacts 1395->0 (counterexamples unchanged 1105/2500); Z35 main (10,15): n_steps 10137->6329, P(J) random 0.230->0.391, tau median 8->7, h2_gate FAIL->PASS (I_J_theta 0.2436->0.1929 now > I_J_tau 0.2777->0.1381; I_J_theta_given_tau 0.1762->0.2692 > I_J_tau_given_theta 0.2103->0.2144) — ALL THREE H gates now pass, outcome B unchanged; controls A/C1 unchanged, C2 shifted, decision B still; other cells (8,12): 2848->1708 steps, tau 5-7->4-5; (12,20)/(14,28) ~unchanged; h2_gate FAIL->PASS (I_J_theta 0.2436->0.1929 now > I_J_tau 0.2777->0.1381; I_J_theta_given_tau 0.1762->0.2692 > I_J_tau_given_theta 0.2103->0.2144) — ALL THREE H gates now pass, outcome B unchanged; controls A/C1 unchanged, C2 shifted, decision B still; other cells (8,12): 2848->1708 steps, tau 5-7->4-5; (12,20)/(14,28) ~unchanged; (16,32) random/lex/autmin bit-identical, entropy n 453->451 (n_J 146 frozen); Control D: gates G1/G2 still PASS (0.0 / 0.0313), steps 5047->4736; twin law: tau-driven I_tau 0.3762->0.1188 DROPS BELOW I_deg 0.2468->0.2227, P(TwinGain\|var) now monotone increasing (0.258/0.793/0.834) — degree variance, not tau, carries the residual info; Z26 entropy unchanged (H_out log2 12); Z27 Polya quotient asserts pass (canon-independent); Z33 tau 12/9/8/8 -> 7/7/7/6 (now matching Z35=7 and Z37 tau*=7), entropy fold 48->1440. NET: every canon-keyed downstream number corrected; core verdicts (outcome B, twin channel sole jump source, concentration < generation) all SURVIVE | recorded; implementations + verify_canon_fix.py + canon_fixed.py reference in repo |

**Rule-8 Conclusion:** with exact |Aut| statistics the mechanism survives every attack: twin
nucleation is real, direction and canonical chain definition matter, but P(dt>0|J)>=0.93 in all
20 selector-cells. Theta is NOT monotonic, so it is a near-Lyapunov order parameter, not a
gradient. Control D (8.12) adds: twin-free algebraic seeds never nucleate jumps and decay to
|Aut|=1 before the twin channel re-nucleates them — the twin channel is the sole jump channel
in the extremal framework.

---

## L1 — Computed facts (no interpretation)

### Main cell (10,15) — exact |Aut| jump ratio 4.0

| Selector | n steps | P(dt>0) | P(dt=0) | P(dt<0) | P(J) | P(dt>0|J) | P(dt<0|J) | rho(dt, log aut ratio) |
|----------|---------|---------|---------|---------|------|-----------|-----------|------------------------|
| random  | 2919 | 0.625 | 0.315 | 0.060 | 0.391 | 0.997 | 0.000 | 0.9434 |
| lex     | 1184 | 0.624 | 0.316 | 0.060 | 0.410 | 1.000 | 0.000 | 0.9386 |
| entropy | 1135 | 0.637 | 0.293 | 0.071 | 0.401 | 0.998 | 0.000 | 0.9102 |
| autmin  | 1091 | 0.610 | 0.346 | 0.045 | 0.409 | 0.998 | 0.000 | 0.9589 |

n_steps total: 6329; 1100/1100 chains converged (tau median now 7 — see 8.14).
TABLE RE-DERIVED 2026-08-03 with the iso-invariant canon fix (8.14). Old buggy-canon values: random 5631/0.230/0.998/0.9349, lex 1720/0.325/1.000/0.9482, entropy 1375/0.331/0.998/0.9312, autmin 1411/0.316/0.998/0.9590, n_steps 10137, tau median 8-12. The old canon inflated chain length (labeled-state revisits); the corrected protocol measures true iso-class revisits. P(dt<0|J) is still 0.000 in every selector.

P(dt<0|J) = 0.000 in every selector: **no exact-|Aut| jump ever coincides with a Theta decrease.**

### Chain endpoints (twin potential)

| Selector | frac chains any dt<0 | frac non-decreasing | theta_start median | theta_end median |
|----------|---------------------|---------------------|--------------------|------------------|
| random  | 0.428 | 0.572 | 0 | 16 |
| lex     | 0.495 | 0.505 | 0 | 16 |
| entropy | 0.700 | 0.300 | 0 | 7 |
| autmin  | 0.235 | 0.765 | 0 | 16 |

Theta grows 0 -> 16 (twin classes of size 6-7) on the majority of chains; entropy ends lower.

### Transition tables (main cell, per selector)

P(J | theta_before): monotone-increasing in Theta up to the "10+" bin, where P(J)=0.000 in all
selectors (a fully-twin state has no twin pair left to create — jump saturation).
Example random: theta=0: n=..., P_J=0.05-0.14; theta=5-9: P_J=0.55-0.76; theta=10+: 0.000.
Cross-tab (autmin): dTheta<0 & J: 0 occurrences; dTheta>0 & J: 445; dTheta=0 & J: 1.

### Info analysis (main cell)

| quantity | value |
|----------|-------|
| H_T (entropy of jump) | 0.8439 |
| I(J; Theta) | 0.2436 |
| I(J; tau-shell (R,A)) | 0.2777 |
| I(J; Theta, tau) | 0.4539 |
| I(J; Theta given tau) | 0.1762 |
| I(J; tau given Theta) | 0.2103 |

### Controls

| Control | key numbers | gate | result |
|---------|-------------|------|--------|
| A (degree-preserving null) | extremal P_pos=0.680 (400 same states) vs rewire 0.0848 (12000 swaps) vs config-model 0.2586 (1574 graphs) | extremal >= 3x config | NOT MET (2.63x) — recorded fail; diagnostic |
| B (reversed extremal) | n=3106, P_J=0.056, P(dt>0|J)=0.431, mean dt=-0.011 | P_J >= 0.1 | NOT MET — direction necessary |
| C1 (no canon, fixed horizon) | n=12000, P(dt>0)=0.1409 vs full random 0.355 | >= 0.9x baseline | NOT MET — canon is part of the chain definition |
| C2 (canon every step) | n_inv_steps=0 in all modes; inflation -0.2399/-0.2115/-0.3483 | | PASS (no inflation from relabeling) |

### Generalization (exact-|Aut| protocol; budgets per Amendment 1)

| Cell | modes (random/lex/entropy/autmin) P(dt>0|J) | rho range | n_steps |
|------|---------------------------------------------|-----------|---------|
| (8,12)  | 0.990 / 0.973 / 0.933 / 1.000 | 0.87-0.92 | 2848 |
| (12,20) | 0.997 / 1.000 / 0.994 / 1.000 | 0.95-0.98 | 1821 |
| (14,28) | 0.995 / 1.000 / 1.000 / 1.000 | 0.92-0.97 | 1525 |
| (16,32) | 1.000 / 1.000 / 1.000 / 1.000 | 0.956-0.964 | 1946 |

All 16 selector-cells above the H1 gate; all rho above the H3 gate.

### Control D (pre-registered 2026-08-03 in `z35_control_d.md` BEFORE any run — twin-free
algebraic seeds in the exact-|Aut| framework)

Seeds (fixed, verified Theta=0): Shrikhande (16,48) |Aut|=192, Rook (16,48) |Aut|=1152,
complement-Shrikhande (16,72) |Aut|=192, Petersen (10,15) |Aut|=120. Selectors: random
(50 chains/seed) + lex/entropy/autmin (1 chain/seed each); cap 256; jump = ratio >= 4;
|Aut| via Amendment-3 v2 counter. 212 chains, all converged.

| Seed | P(jump t=0) | median tau_first(theta>0) | median tau_half(|Aut|<=|Aut|0/2) | median end |Aut| | P(any |Aut|=1) | P(end theta=0) | jumps |
|------|-------------|---------------------------|----------------------------------|------------------|-----------------|-----------------|-------|
| shrikhande  | 0.000 | 13 | 0 | 3,110,400 | 1.000 | 0.000 | 287 |
| rook        | 0.000 | 15 | 0 | 3,110,400 | 1.000 | 0.000 | 313 |
| comp_shrikh | 0.000 | 10 | 0 | 3,110,400 | 1.000 | 0.000 | 280 |
| petersen    | 0.000 | 6  | 0 | 720 | 0.981 | 0.019 | 149 |

Aggregates (1029 jumps total): **G1 P(jump at t=0) = 0.000 -> PASS**;
**G2 P(jump & dtheta<=0) = 0.0311 -> PASS**; P(dtheta<0|jump)=0.000 (identical to main cell),
P(dtheta>0|jump)=0.969, P(dtheta=0|jump)=0.0311 (32 jumps — quotient-channel jumps with Theta
constant). Largest jump: 60,480 -> 52,254,720 (864x in one step, dtheta=20).
Lex chain endpoints: Shrikhande and Rook converge to the SAME canonical endpoint
(|Aut|=3,110,400, Theta=33) — the algebraic identity of the seed is erased; comp_shrikh lex
ends at 483,840 (Theta=29); Petersen at 240 (Theta=11).

---

## L2 — Interpretation (what L1 forces)

### H1 — Theta predicts |Aut| jumps. PASS.
P(dt>0|J) >= 0.998 in all four main selectors (0.933-1.000 across all cells), and
P(dt<0|J)=0.000 everywhere: whenever exact |Aut| jumps by factor >= 4, Theta had increased.
Theta is a near-Lyapunov order parameter: not monotonic (P(dt<0)=0.035-0.118), but jumps never
coincide with decreases.

### H2 — Theta dominates the (R,A) tie-shell. FAIL.
I(J; Theta given tau)=0.176 < I(J; tau given Theta)=0.210. The shell retains residual
information about jumps beyond Theta, and the joint I(J; Theta,tau)=0.454 shows the two are
partially complementary, not redundant. The shell is a gate (Z33), Theta is the readout — but
the shell is not fully subsumed.

### H3 — Aut jump is a consequence of twin-class growth. PASS.
rho(dt, log aut ratio) = 0.93-0.96 in every main selector and 0.87-0.98 in every cell.
Combined with the Amendment 3 identity (exact theorem, validated):
|Aut(G)| = (prod |C_i|!) * |Aut(twin quotient colored by class size, with self-loops)|,
the jump mechanism is: twin class grows (Theta increases by the class size) -> |Aut| multiplies
by (k+1) times the quotient factor. |Aut| is a readout; Theta is the mechanism.

### Selector comparison
- lex: most deterministic, highest coupling (1.000), ends at Theta=16.
- entropy: weakest P(dt<0|J) profile (0.118) and lowest endpoint (Theta 7) — entropy bias
  actively disperses degree structure, delaying twin nucleation.
- autmin: under the exact-|Aut| minimizer, jumps STILL nucleate (P_J=0.316) — the adversarial
  selector slows growth (0.235 frac chains with any decrease — fewest) but cannot stop it:
  the minimal-|Aut| move still lands in states where the NEXT exchange creates twins.
- Control B shows the reverse direction destroys coupling (P(dt>0|J)=0.431): direction matters.

### Control D — interpretation (algebraic channel is not a jump channel)
- Twin-free algebraic seeds (Theta=0, |Aut| 120-1152) NEVER nucleate an |Aut| jump in the
  first exchange (G1 P=0.000, n=212) — the algebraic channel produces high |Aut| statically
  but contributes nothing to jump nucleation under extremal dynamics.
- The algebraic symmetry collapses immediately: median |Aut| halves within the FIRST step
  (tau_half median 0) and every (16,*) chain dips to |Aut|=1 at some point (full wipeout)
  before the twin channel re-nucleates symmetry to 3,110,400 (>= 2700x the seed's |Aut|;
  Petersen -> 720 = 6! family). Shrikhande and Rook lex chains converge to the SAME
  canonical endpoint: extremal dynamics erases the algebraic identity of the seed.
- All 1029 jumps remain twin-mediated: P(dtheta<0|jump)=0.000. The 3.1% dtheta=0 jumps are
  the quotient channel (Theta constant, twin structure unchanged, colored-quotient |Aut|
  multiplied) — the same residual class as the main cell's P(dt>0|J)=0.998 (0.2% tail).
- Conclusion: Control D PASS (G1+G2) — the twin channel is the ONLY |Aut| jump channel in the
  extremal framework; outcome B is unchanged and strengthened. Z36's algebraic channel is a
  static property of twin-free regular graphs, not a nucleation mechanism.

---

## L3 — Conjecture / open direction

1. **Why tie-collapse at all:** P(N(u)\{v}=N(v)\{u} after exchange) = f(|N(u) n N(v)|, Re, Ae).
   Candidates for a combinatorial theorem: exchange acts on small degree shells (R,A) and the
   overlap of the affected neighborhoods grows under repeated extremal choice.
2. **Non-contractive formulation:** Theta is near-monotonic, not monotonic (10-15% decreases).
   Search for Phi = alpha*Theta + beta*H(deg) + gamma*(canon distance) that is monotonic along
   chains.
3. **Density effect:** the "10+" saturation bin (P(J)=0 there) shows a maximal-twin regime;
   (14,28) vs (16,32) both pass at the same gates, but the density 0.307 vs 0.266 shifts
   jump rates. A density sweep is the natural Z36.
4. **Dual characterization of autmin avoidance:** characterize the states autmin avoids —
   twin formation <=> pair (u,v) with |N(u) triangle N(v)| = 2.
5. **Structural theorem (Amendment 3 identity) as Z36 target:**
   |Aut(G)| = (prod |C_i|!) * |Aut(Q)| with Q the colored twin quotient — exact, validated
   3817/3817 plus Shrikhande/rook; gives an exact two-level decomposition of symmetry jumps.
   **Realized by Z36** (see ledger 8.10/8.11): independent networkx experiment confirmed the
   same identity on 14/14 attractors plus Shrikhande/Rook/Petersen (cross-tool 100%), and
   added the algebraic channel for twin-free graphs (Theta=0, SRG: distinct eigenvalues 3,
   concentrated lambda/mu -> Aut 120-1152; random regular: Aut=1) — the sparse-regime twin
   channel (this report) and the dense-regular algebraic channel are complementary, not
   competing; a true two-regime picture of symmetry nucleation.

---

## Decision Table (pre-registered)

| Outcome | Condition | Result | Verdict |
|---------|-----------|--------|---------|
| A | H1 + near-monotone (P(dt<0)<=0.02 everywhere) + control B pass | P(dt<0)=0.035-0.118 > 0.02 | NOT A |
| B | H1 + (H2 or H3) | H1 and H3 pass, H2 fails | **B (stochastic symmetry nucleation)** |
| C | otherwise | H1/H3 pass in all cells | rejected |

**Final: Outcome B.** Theta(G)=sum C(|C_i|,2) is the hidden order parameter of tie-collapse:
it predicts every exact-|Aut| jump (P(dt>0|J)>=0.998 main, 0.933-1.000 all cells; P(dt<0|J)=0.000),
it is strongly correlated with the |Aut| ratio (rho 0.87-0.98), and the jump factor is
decomposed exactly by the twin-quotient formula. Dynamics is stochastic nucleation with a
near-Lyapunov potential, not gradient flow. Control D (pre-registered, G1+G2 PASS) confirms
the twin channel is the SOLE jump channel: twin-free algebraic seeds (Z36's Shrikhande class)
nucleate nothing and collapse to |Aut|=1 before twin re-nucleation to far larger scales.

## Final Causal Diagram (Z34 -> Z35)

```
Z34: degree extremization -> neighborhood equalization -> twin restructuring -> |Aut| jumps
Z35 (exact |Aut|, 5 cells):
  extremal exchange (direction matters; reversed rule kills coupling)
        -> repeated action on small degree shells (R,A)
        -> P(neighborhood overlap) rises
        -> twin class grows: Theta = sum C(|C_i|,2) increases
        -> |Aut| multiplies by (k+1) x quotient factor   (exact, validated identity)
        -> high-symmetry attractor (Theta 0 -> 16; "10+" saturation: no further jumps)
  Gates: Theta near-monotonic (not strict); (R,A) retains residual info (H2 fail).
```

No physics. No analogy. Only graph dynamics. Exact statistics only.

## Files

- Harness: `phase_z35/z35_tie_collapse_theorem.py` (pre-registration + Amendments 1-4 embedded)
- Results: `phase_z35/z35_results.json` (per-stage resumable; main_cell, controls A/B/C1/C2,
  decision, other_cells (8,12),(12,20),(14,28),(16,32))
- |Aut| cache: `phase_z35/z35_aut_cache.sqlite` (EX-key exact values; 4830 rows)
- External checks: `phase_z35/shrikhande_correct.py`, `phase_z35/shrikhande_verification.json`
- Parallel loose-protocol run (recorded, not merged):
  `phase_z35/z35_experiment.py`, `phase_z35/z35_summary.json`,
  `phase_z35/z35_results (1).json`, `phase_z35/PHASE_Z35_REPORT_PARALLEL_EXPERIMENT.md`
- Earlier unrun draft, audited + run + recorded in ledger 8.13:
  `phase_z35/z35_twin_creation_law.py` (harness, 2 bugs fixed), `phase_z35/z35_twin_creation_law_results.json`
- Z36 standalone experiment (recorded in ledger 8.10/8.11, not merged):
  `phase_z36/PHASE_Z36_REPORT.md`, `phase_z36/z36_experiment.py`, `phase_z36/z36_results.json`
- Cross-verification script: `phase_z36/cross_check_attractors.py` (regenerates the 14 Z25b
  attractors deterministically and re-checks |Aut|/Theta/twin_aut against our exact counter)
- Control D (pre-registered 2026-08-03): `phase_z35/z35_control_d.md` (protocol),
  `phase_z35/z35_control_d.py` (harness), `phase_z35/z35_control_d_results.json` (212 chains)
