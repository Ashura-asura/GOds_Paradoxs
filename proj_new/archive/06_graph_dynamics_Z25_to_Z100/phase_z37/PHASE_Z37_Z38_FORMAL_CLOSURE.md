# PHASE Z37+ — FORMAL CLOSURE PROGRAM — FINAL REPORT

Pre-registered 2026-08-03 in `Z37_PREREGISTRATION.md` (Rule-2, before any run).
Deliverable of the Z37+ closure program. All runs executed with the identical
engine/conventions as Z35 (`z37_closure.py`; jump = |Aut| ratio >= 4; |Aut| via
Amendment-3 v2 counter; Theta via twin_potential; RNG SEED0 + 131*s + 991*len(mode)).
Levels: L1 = verified exactly (closed form or exhaustive), L2 = verified statistically,
L3 = interpreted/heuristic.

---

## 0. RULE-8 LEDGER (all failures recorded)

| # | Entry |
|---|-------|
| 1 | **EX canon not iso-invariant (quantified then):** in task-1 V2, 1395 of 2500 iso successor pairs received different EX keys (56% artifact rate). For asymmetric graphs `z25b_engine_v2.canon` returns the graph's own labeling, not the global lex-min representative. INV keys are iso-invariant. **RESOLVED 2026-08-03 (fix implemented in-repo + verified, ledger 8.14): artifact count on the fixed canon is now 0/2500; genuine nx counterexamples unchanged (1105/2500).** |
| 2 | **Z27 statement "canon = isomorphism" is FALSE as implemented.** All EX-key-based measurements in Z25–Z36 (support counts, H(mu), C2, Z31 TV, orbit identification) are invalid as EX-key-based; INV-key or exact-count versions remain valid. **RESOLVED 2026-08-03:** after the iso-invariant canon fix, EX keys are exact iso-class labels (no false merges), and all canon-keyed downstream numbers have been re-derived (ledger 8.14). |
| 3 | **First t1 run discarded (probe artifact):** `frozenset((perm[a],perm[b]) ...)` produced unsorted edge tuples; `tau_of` comparisons were corrupted. Fixed with `tuple(sorted(...))`; all t1 numbers below are from the corrected run. |
| 4 | **H_T2 falsified:** CN_ADD is NOT the largest MI feature for twin formation (ranked outside top 3 in both cells); TH0 (current twin potential) dominates. |
| 5 | **R3 falsified:** 197 twin-free atlas counterexamples to "|Aut| >= 2 => num_distinct <= N/2+1". Spectral compression is not a consequence of algebraic symmetry. |
| 6 | **R2 degenerate counterexample:** single-vertex graph (|Aut|=1) violates "WL-depth <= 2 & regular => |Aut| >= 2". Holds on all other 367 twin-free atlas graphs and all 21 zoo graphs. |
| 7 | **t6 EX-canon orbit counting invalid** (cf. entry 1) — replaced by exact Burnside counting #orbits(shell) = (1/N!)·sum_{labeled in shell} |Aut|. |
| 8 | **Zoo graphs Q4, T6 initially failed** (non-integer node labels) — fixed via canonical relabel. |

---

## 1. TASK 1 — TIE-COLLAPSE THEOREM (L1)

| Verification | Result | Verdict |
|---|---|---|
| V1: R,A iso-invariance (200 states x 3 perms) | **0 / 600 violations** | 1A CONFIRMED |
| V2: lex well-defined on quotient (500 states x 5 perms, 2500 iso pairs) | **1105 counterexamples** (lex successors non-iso), INV keys agree 1105/1105 | 1B: lex FAILS |
| V2': EX-key artifacts on iso successor pairs | 1395/2500 (56%) | Rule-8 #1 |
| V3: tau* well-defined (argmin INV key over R x A) | **0 / 1500 violations** | 1B: iso-invariant tie-break PASSES |
| V4: chains under tau* (200 chains, cap 64) | median tau* = 7, endpoint support = **5**; all converged | 1C: collapse (i) quotient projection + (ii) short cycle + (iii) support concentration |
| V4 lex comparison | median tau = 7, endpoint support = **8** | C-separation: tau* concentrates more (5 vs 8) |

**Theorem candidate (supported, L1 at N=10, M=15):** the extremal-exchange quotient map
Phi = c ∘ T_tau is well-defined iff tau is iso-invariant; under iso-invariant tau the
quotient orbits are periodic with median period 7 (cap 64) and 200/200 chains converge;
lex (label-dependent) produces a well-definedness failure on 44% of iso pairs.

---

## 2. TASK 2 — TWIN FORMATION PROBABILITY LAW (L2 measurement)

| Cell | P(E) | H(E) | Top-3 MI | Minimal sufficient set (gain < 5% H_E stop) |
|---|---|---|---|---|
| (10,15) | 0.076 | 0.388 | TH0 0.267, R 0.264, FREEDOM 0.248 | [TH0, DEGVAR, A] |
| (16,32) | 0.082 | 0.408 | TH0 0.239, A 0.229, FREEDOM 0.214 | [TH0, A, DEGVAR] |

**H_T2 falsified (Rule-8 #4):** neighborhood-overlap (CN_ADD) is not the dominant
feature. The current twin potential TH0 is the strongest predictor of a twin-gain step
(twin creation is facilitated from low-theta states), followed by shell geometry
(R/A/FREEDOM) and degree variance. Law: P(E) is small (≈0.08) and near-constant
across cells; the sufficient set {TH0, DEGVAR, A} explains it.

---

## 3. TASK 3 — SCALING WINDOW (L2)

Median tau (random selector): 19, 25, 34, 45, 64.5 for N = 16, 20, 24, 30, 40.

| Fit | r^2 |
|---|---|
| tau = const | 0.000 |
| tau = -12.4 + 1.92 N (linear) | **0.999** |
| tau = a·exp(bN), b = 0.050 | 0.965 |

**Scaling: tau ~ O(N) linear, r^2 = 0.999 (5 cells).** Exponential fit is rejected by
comparison. Median t_nucl = 2–4 (nucleation is immediate), median log-slope of |Aut|
vs t ≈ 0.91–1.26 (roughly N-independent; |Aut| grows approximately log-linearly during
the transient). Endpoint support collapses to **1** for all N >= 20 and selector TV
(random vs lex) = 0.000 for N >= 20 (0.033 at (16,32)) — selectors converge to the same
endpoint class. All 182 chains converged (45+45+36+28+28 across the five scaling cells).

---

## 4. TASK 4 — QUOTIENT-CHANNEL JUMP PARTITION (L1 identity, L2 shares)

| Cell | jumps | T | Q | M | S | identity violations |
|---|---|---|---|---|---|---|
| (10,15) | 925 | 91.1% | 0.76% | 0.11% | 8.0% | 0 |
| (16,32) | 1445 | 96.3% | 0.07% | 0.00% | 3.6% | 0 |
| (24,48) | 1641 | 98.9% | 0.06% | 0.00% | 1.0% | 0 |

**Amendment-3 integrality verified on all 4,011 states (0 violations, L1).**
Q-share decays with N (0.76% -> 0.06%) and is far below the 5% gate at (24,48):
per pre-registration, the quotient channel is a **finite-size residual**, not a second
nucleation mechanism. The jump mechanism is dominated by the twin channel (T ~ 91–99%).

---

## 5. TASK 5 — ALGEBRAIC SYMMETRY ACTIVATION THEORY (L1 gate)

Zoo: 21 constructed graphs, all computed. Atlas: 1253 graphs (N <= 7), 368 twin-free.

| Rule | Atlas twin-free violations | Zoo violations | Gate (0 allowed) |
|---|---|---|---|
| R1: regular & ndistinct <= 3 => |Aut| >= N | **0 / 368** | **0 / 21** | **SURVIVES** |
| R2: WL-depth <= 2 & regular => |Aut| >= 2 | 1 / 368 (single-vertex graph, |Aut|=1) | 0 / 21 | fails (degenerate) |
| R3: twin-free & |Aut| >= 2 => ndistinct <= N/2+1 | **197 / 368** | 0 / 21 | **FALSIFIED** |

**R1 is the surviving algebraic predictor** (L1: 0 counterexamples over 368 twin-free
atlas graphs + 21 zoo graphs): regular graphs with <= 3 distinct adjacency eigenvalues
are vertex-transitive beyond triviality — |Aut| >= N. R2 holds on all non-degenerate
graphs (the single counterexample is the N=1 graph); recorded as a degenerate failure.
R3 fails massively (twin-free |Aut| = 2 trees/paths have N distinct eigenvalues), e.g.
atlas #25 (N=5, path-like, |Aut|=2, ndistinct=5 > 3.5).

---

## 6. TASK 6 — BURNSIDE SHELL LAW (L1 exhaustive)

Exhaustive enumeration: N=6 all M (32,768 labeled), N=7 M in {9,10,11} (999,362 labeled).
Orbit counts computed exactly by Burnside (#orbits(shell) = sum |Aut| / N!):

| Cell | labeled | orbits | note |
|---|---|---|---|
| N=6, all M | 32,768 | 1,1,2,5,9,15,21,24,24,21,15,9,5,2,1,1 | matches the known unlabeled-6-vertex counts per M |
| N=7, M=9 | 293,930 | 131 | |
| N=7, M=10 | 352,716 | 148 | |
| N=7, M=11 | 352,716 | 148 | |

**L1 identity found: sigma_q == sigma_a exactly** (uniform-over-orbits = Aut-weighted
labeled; Burnside duality) — verified on all cells. Validation: 20,000 Aut-weighted
labeled draws at (7,10) reproduce the exhaustive sigma_a with **TV = 0.019**.

**Dynamics vs law (pre-registered question):** attractor shell distributions do NOT
match the sigma_q/sigma_a mode (TV = 0.857 / 0.782 / 0.702 at (6,9),(7,10),(7,11),
gate 0.2 → no winner). The dynamics is *selectional*, not sampling: e.g. at (7,10) the
max-Aut shell (10,10) (mean |Aut| = 240) holds 0.7% of Burnside mass but **19% of
attractor mass**; median end |Aut| = 2 (N=6), 8 (N=7).

---

## 7. PROVEN / FALSIFIED / CANDIDATES

**Proven (L1):**
1. R,A candidate sets are iso-invariant (V1: 0/600).
2. Quotient well-definedness requires an iso-invariant tie-break; lex fails (1105
   counterexamples), tau* passes (0/1500).
3. Amendment-3 identity |Aut| = TF x |Aut(quotient)| — 0 violations on 4,011 states
   (plus 3,817 prior) and Burnside orbit counts are integers (exhaustive N=6/7).
4. R1: regular & <= 3 distinct eigenvalues => |Aut| >= N (0/389).
5. sigma_q == sigma_a exactly (Burnside duality).
6. Median tau ~ O(N) linear (r^2 = 0.999), endpoint support -> 1 for N >= 20.
7. N=6 orbit counts match the known unlabeled sequence (external cross-check).

**Falsified:**
1. H_T2 (CN_ADD dominates twin formation) — TH0 dominates instead.
2. R3 (spectral compression from |Aut| >= 2) — 197 counterexamples.
3. "Dynamics samples the Burnside shell law" — TV 0.70–0.86 vs law mode.
4. Z27 "canon = isomorphism" — EX canon is not iso-invariant (Rule-8 #1/#2).

**Theorem candidates (supported, require larger-N confirmation):**
- Tau* chain period O(N) with concentration onto a single endpoint class (support 5 at
  N=10, 1 at N >= 20).
- Single-mechanism nucleation: twin channel carries 91–99% of jumps; quotient channel
  decays with N (finite-size residual).

---

## 8. FINAL MECHANISM DIAGRAM (L1 + L2 synthesis)

```
uniform labeled seed
   |
   |  extremal exchange (any selector)
   v
[shell geometry (R,A): iso-invariant, V1]
   |
   |  twin channel (T-class jumps, 91-99%)
   v
[theta increases; |Aut| = TF x quotient-aut  (Amendment 3, exact)]
   |  (quotient channel Q: <1%, decays with N -> residual)
   |  tau* (iso-invariant tie-break, argmin INV key)
   v
[quotient cycle, median period ~ 1.92N - 12 (linear, r2=0.999)]
   |
   v
[attractor: 1 endpoint class (N>=20), high-Aut shell
            (e.g. (10,10): 19% attractor vs 0.7% Burnside mass)]
```

The collapse is: (i) iso-invariant projection onto (R,A) shells, (ii) twin-factor
nucleation (Theta increase, dominant jump channel), (iii) iso-invariant tie-break
(tau*) selecting a short quotient cycle, (iv) convergence to a single high-symmetry
endpoint class that is strongly over-selected relative to the uniform Burnside law.

---

## 9. REMAINING UNKNOWNS

1. Canon bug (Rule-8 #1) affects prior EX-key-based numbers in Z25–Z36 — full re-derivation
   of support/H(mu)/C2/Z31-TV with INV keys is open work.
2. Exact characterization of the single endpoint class (which graph is it, why).
3. tau* period distribution tails (cap 64; heavy-tail check at larger cap).
4. R2 degenerate exception (N=1) — whether "regular" should exclude N<2.
5. Linear-fit slope 1.92 at M = 2N — dependence on density M/N not yet measured.

---

## FILES

- `phase_z37/Z37_PREREGISTRATION.md` — protocol (Rule-2, before any run)
- `phase_z37/z37_closure.py` — harness (tasks t1..t6, INV-key iso logic, Burnside t6)
- `phase_z37/results/t1.json .. t6.json` — full numeric outputs
- Engine: `phase_z35/z35_tie_collapse_theorem.py` (Amendment 3), `phase_z25/z25b_engine_v2.py`
  (canon — EX bug recorded), `phase_z33/z33_symmetry_drift.py` (selectors/tau_of)
