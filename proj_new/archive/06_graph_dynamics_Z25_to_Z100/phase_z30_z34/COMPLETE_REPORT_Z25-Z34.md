# PHASES Z25–Z34 — COMPLETE CONSOLIDATED REPORT
# 2026-08-02 · Rules v2 · Cell under study: (10,15)

---

## EXECUTIVE SUMMARY

Ten phases closed a single mechanistic question: *why does the extremal
exchange concentrate onto a small high-symmetry attractor?* The answer is
now pinned at four levels.

- **Z25–Z27:** The engine is a witness-free conservative edge-exchange rule
  on G_{N,M}. Its canon() is exactly graph isomorphism (Z27); the quotient
  Q_{N,M} = G_{N,M}/S_N is exactly the unlabeled-graph space, counted
  exactly by Pólya enumeration (|Q_10,15| = 136,433 = OEIS A000088(10)).
  The dynamics does not generate information — it is a many-to-one
  contraction (Z26 Theorem B, 20× information gap).
- **Z28–Z29:** No scalar Lyapunov exists among standard graph invariants
  (Z28). The tie-class fixed-point conjecture (Z29) is falsified at 0–1%:
  attractor states are the *most* tie-degenerate, not the least. The
  collapse is not driven by a hidden invariant; it is produced by canon()
  merging degenerate extremal choices under a fixed tie-break.
- **Z30–Z31:** The common object across selectors is a narrow tie-degeneracy
  shell τ = (|R|,|A|) ~ (6,2) at (10,15), and the Burnside-weighted quotient
  measure σ(N,M) already concentrates probability mass onto that shell. The
  selector does not create the shell; it selects a period-2 cycle *inside*
  it. σ(N,M) is a stable limit law (Poisson-like, peaked at (1,1), N-
  independent for N≥10 at fixed ρ). The dynamics converges to the
  *max-|Aut| region of the weighted shell*, not the unweighted one.
- **Z32–Z34:** "Quotient geometry only, selector is bookkeeping" (Outcome A)
  is refuted — not because dynamics tracks a different shell, but because the
  static labeled sampler is structurally blind to the attractor region by a
  factor of ~10⁹ in orbit size. The climb is a **front-loaded staircase of
  rare large jumps** against a zero-median background (Z33). Those jumps are
  **twin-class restructuring events** (H1), gated by sparse (R,A) ties but
  caused by twin merger (Z34). Component cloning (H2) is universal and non-
  discriminating. H3 (residual unexplained) is refuted: <0.4% of jumps fire
  no event.

The causal chain closing the arc:

```
degree-sum extremization → vertices pushed to equal degree →
neighborhoods become more similar → twin classes form or merge →
|Aut| jumps by factorial factor → staircase trace → attractor is the
shell where no more twin restructuring is possible.
```

This is "basin-like" (Z33 Outcome B) in the specific sense that the climb
is front-loaded and the attractor inherits the summit, not that a persistent
directional force keeps pushing.

---

## PHASE Z25 — RELATIONAL ORIGIN ENGINE

Goal: build a minimal witness-free engine and test whether it produces
emergent ratios (the "Tony" protocol).

### L1 (exact)
- Engine T: conservative edge exchange on G_{8,?} (8-cycle + chord), degree-
  signature tie-breaking with scalar p, witness-edge emission per non-trivial
  permutation cycle. No energy, no potential, no pre-given symmetry.
- Runs: p ∈ {0.0, 0.2, 0.4, 0.6, 0.8, 1.0} × 12 trials each = 72.
- All 72 trials converge to period-1 fixed points. No emergent ratios
  observed at any p. N_input = 1 (scalar p), N_output = 0.
- The transformation is contractive: sorting degree signatures projects onto
  a totally ordered set; witness-edge accumulation pushes toward denser,
  highly symmetric graphs; the orbit converges to a rigid canonical form.

### Verdict
FAILED (Rule-8 closed). The engine produces no emergent ratios. This is a
mechanism failure, not a proof that the program is impossible: the engine
lacks non-contractive recurrence (witness edges accumulate, not replace), so
only one attractor exists per p-value.

### L2 (synthesis)
The Z24 Master No-Go echoes here: invariant/counting-driven dynamics do not
add selection information; they expose the information already encoded in
boundary conditions (seed graph, N, M, degree convention).

---

## PHASE Z25-b — FOUR HARD QUESTIONS

Goal: replace the contractive witness-accumulating rule with a conservative
edge exchange (always-M conserved) and test four hard questions.

### Engine
z25b_engine_v2.py (declared engine): edge exchange by endpoint degree-sum
ordering, tie-broken lexicographically; balance vs contrast chosen by scalar
p. Canonicalization via WL color refinement + budget-capped exact search
(deterministic INV key fallback when budget exceeded).

### L1 (exact)
- Q1 (universal ratios): **No.** No ratio survives as universal across the
  seed sweep. At p=0, ratios concentrate at {2/5 (5/6 share), 2/3 (1/6)}; at
  M=10/35 the attractor flips entirely. At p=1, 12 seeds → 8 distinct
  basins with ratios {0, 1/2, 2/3, 3/4, 1, 3, undef}.
- Q2 (robustness across seeds): **Partially.** Within a fixed (N,M,anchor)
  family at p=0 the dominant basin is robust (share 5/6), but across seed
  graphs the attractor set fragments (12 seeds → 12 distinct keys, dominant
  share 1/12). Robustness is real only at the level of "concentration
  behavior," not of "same output."
- Q3 (generative surplus): **Not met.** Under the sharpened criterion
  (dynamics can only permute within a finite orbit; N_out ≤ log2(#reachable
  states)), the dynamics output bits are bounded by state-space entropy and
  the observed ratios are recomputable from the seed's own counts after
  period-2 collapse. The ledger "N_in=1 → N_out" claim collapses because
  the seed graph + (N,M) are unaccounted inputs carrying the actual
  selection information. N_in ≥ N_out; the dynamics compresses, it does not
  generate.
- Q4 (no hidden tuning): **Yes.** No energy/potential/symmetry term in T;
  balance-vs-contrast is a fixed counting rule. p does not select among
  universals — at best it shifts basin shares.

### Verdict
PARTIAL (revised from engine's raw print label). Structure emerges (stable
attractors, computed Aut groups as large as 1440, non-trivial local ratios).
But universality fails (Q1), robustness across seed graphs fails (Q2),
generative-surplus fails under sharpening (Q3). This is the relational-
engine instance of the Z24 Master No-Go: invariant-driven dynamics do not
add selection information; they expose information already in boundary
conditions.

---

## PHASE Z26 — WHY THE BASIN / WHY PERIOD-2 / INFORMATION ACCOUNTING

Goal: explain the Z25-b basin concentration and period-2 mechanism, and
verify the information accounting.

### Theorem A — basin is seed-driven (L1, proven by table)
- Across 12 random (10,15)-graphs at p=0: 12 distinct attractor keys,
  dominant share 1/12. Same at p=1: 12 distinct keys, dominant share 1/12.
- Across M ∈ {10, 15, 35} at p=0: M=10 → n3/n4 undefined (0 4-cycles);
  M=15 → 2/5 or 2/3; M=35 → 0.2292. The attractor is a function of (N, M,
  seed). No graph-independent canonical identity exists.

### Theorem B — no-free-lunch / information conservation (L1, proven exactly)
- I_state = log2 C(45,15) = 38.3273 bits
- I_seed = 38.3273 bits
- I_rule = 1 bit
- I_p ≤ 32 bits
- H_output(attractor keys) = 3.5850 bits
- H_out / (I_seed + I_rule + I_p) = 0.0503 → I_output < I_input by ~20×.
  The dynamics CONCENTRATES; it does not GENERATE.

### Period-2 mechanism (L1)
- Projection hypothesis (one iteration lands in image, T idempotent there →
  period-2 forced): **DISPROVED.** 24/24 random seeds have T² ≠ T on the
  image.
- Real cause (motion trace): p=0 → (m2, n3) evolves (124,8) → (132,10) →
  (138,13) → (142,14) → (144,16) → (150,20) → (144,16) → (150,20) → ...
  so the attractor is the 2-point level set {m2 + 6n3 = 240}. p=1 → m2
  falls monotonically to 92 and floors; n3 flips 2↔3; attractor = 2-point
  set at m2=92.
- The exchange rule pushes the iterate to a local boundary of its monotone
  objective; at the boundary the two extremal swap-choices remove/add the
  SAME unordered pair iteratively, giving period 2.

### Uniqueness-by-singleton hypothesis (DISPROVED)
- Hypothesis: at each state the extremal swap is unique up to iso, which
  with periodicity would force a unique attractor.
- Result (136 states across all Z25-b converged orbits):
  - Removal ties (n_rem_ties > 1): 96/136 states; distinct iso classes among
    removals: 96/136 (up to 11 at once).
  - Addition ties (n_add_ties > 1): 120/136; distinct iso classes among
    additions: 0/136.
- **Conclusion:** The uniqueness of the Z25-b attractor does NOT come from a
  unique extremal step. The remove-side is highly degenerate; the add-side
  is iso-unique everywhere. The single-basin concentration is produced by
  canon() collapsing the degeneracy — a TIE-COLLAPSE theorem, not a local
  uniqueness theorem.

### Open
- Prove the tie-collapse is total: for ALL (N,M) on a connected
  reachability class, any two distinct non-iso sequences of extremal
  removals lead (after canonicalization on the add-unique side) to iso-
  conjugate attractors.

---

## PHASE Z27 — QUOTIENT IDENTIFIED & COUNTED · UNIVERSALITY SWEEP

Goal: identify the quotient, count it exactly, test universality across N,
and reverse the perspective (preimage/basin maps).

### L1 (exact)
1. **Quotient identified:** canon() is exactly graph isomorphism. The
   equivalence relation induced by canon() is:
   ```
   canon(g1) == canon(g2)  ⟺  g1 ~ g2  under S_N
   ```
   The tie-collapse is exactly the orbit projection G_{N,M} → G_{N,M}/S_N
   (the unlabeled-graph quotient). All engine observables are by construction
   functions on this quotient.

2. **Quotient counted exactly (Pólya enumeration):**
   - Unlabeled graphs on 10 vertices: 12,005,168 = OEIS A000088(10) EXACTLY.
   - Key cells:
     - (8,12): |Q| = 1,312, I_quot = 10.36 bits
     - (10,15): |Q| = 136,433, I_quot = 17.06 bits
     - (12,18): |Q| = 19,515,361, I_quot = 24.22 bits

3. **Information decomposition (splits Z26 Theorem B):**
   - Gauge loss (relabeling deadwood): I_lab − I_quot = 21.27 bits at (10,15)
   - Dynamical contraction loss: I_quot − H_out = 17.06 − 3.585 = 13.47 bits
   Neither piece generates information; gauge part was never information
   (gauge redundancy), contraction part is T being many-to-one.

4. **Universality sweep (p ∈ {0,1}, N ∈ {8,10,12}):**
   - Period-2 class theorem survives every N tested (period 1 appears once
     at N=12, the level-set singleton case).
   - The Z26 add-side iso-uniqueness does NOT survive N: at (8,12) it holds
     on only 65% of states; at (10,15) it was 100% (system-specific).
   - Basin contraction strengthens with N: at (12,18), p=0, only 3 distinct
     attractors out of 8 seeds.

5. **Reverse perspective (mechanical):**
   - Preimage map ρ⁻¹: quotient → labeled classes (orbit size = N!/|Aut|)
   - Basin size: #{seeds s : lim Tᵗ(s) = key}
   - Pushforward measure: histogram of canon keys over uniform G_{N,M}
   - H(μ) = 7.46 bits vs log2|Q| = 17.06 bits → dynamics adds a
     contraction, not information.

### Rule-8 closures
- Harness bug (faulty lex tie-break → period-24 artifact): superseded by
  verified control runs; recorded in Z30.
- N6 zero-edge/complete graphs excluded as degenerate.

---

## PHASE Z28 — PUSHFORWARD MEASURE & INVARIANT HUNT

Goal: measure the pushforward measure μ = (T^∞ · canon)_* Unif(G_10,15) and
search for a scalar Lyapunov invariant.

### Phase 1 — measure (L1)
- Quotient Q = G_10,15/S_10, |Q| = 136,433.
- μ estimated with 300 uniform labeled seeds at p=0:
  - Converged: 300/300
  - Distinct attractors: 210 support points
  - H(μ) = 7.4616 bits
  - log2|Q| = 17.0578 bits
  - Support/|Q| = ~1.54×10⁻³ (0.154% of the quotient)
- Updated information decomposition at (10,15):
  - 38.3273 (uniform labeled input)
  - −21.2694 gauge (canon ~> quotient; ~log2 10! = 21.79, as expected)
  - 17.0578 quotient point
  - −9.5962 dynamical contraction
  - 7.4616 attractor distribution over its 210-point support
- Every stage destroys information. None creates it. The engine's output is
  a 7.46-bit distribution concentrated on 0.15% of the quotient.

### Phase 2 — invariant hunt (L1 negative)
Candidate scalar invariants evaluated on (x, T x) for the last 24 states of
24 random orbits per mode (576 samples each side):
- H2 = Σd²; H4 = Σd⁴; TRI = #triangles; SQR = #4-cycles
- CHR = Σ_v C(d_v,2) (wedges); MAT2 = #vertex-disjoint edge pairs
- P2 = Σ_edges (min_d · max_d)

**Result:** strictly_one_sided = FALSE for every candidate. Each statistic
both increases and decreases on the transient/attractor boundary (e.g. at
p=0 every candidate has exactly 60 inc / 60 dec / 456 flat per 576 steps).

**Theorem-B-flavored negative (L1):** The extremal-exchange rule admits NO
Lyapunov function among standard graph-invariant scalar statistics. The
collapse to period-2 is not driven by scalar descent; it is produced by the
tie-collapse (Z26: add-side iso-singleton + canon merge of remove-ties).

### Rule-8 closures
- Scalar-Lyapunov avenue: CLOSED.

---

## PHASE Z29 — TIE-CLASS SUPPORT CHARACTERIZATION (REFUTED)

Goal: test whether the attractor is a state whose extremal tie-class is
invariant under one T-application.

### Conjecture under test
An attractor of μ is exactly a state whose extremal tie-class — the iso-classes
of argmin/argmax-degree-sum edges R(g) and non-edges A(g) — is invariant under
one T-application.

### L1 (exact, falsified at 0–1%)
Over 300 converged attractors per mode:

- p=0.0: P1 (singleton extremal swap) = 0/300; P3 (all R×A swaps co-collapse)
  = 0/300; coverage = 0.0000. Typical tie multiplicities: |R| = 6, |A| = 2.
- p=1.0: P1 = 3/300; P3 = 3/300; coverage = 0.0100. Typical: |R| = 4, |A| = 6.

Attractor states are the *most* tie-degenerate states, not the least. The
tie-class does NOT stabilize at the attractor; if anything it maximizes its
degeneracy there.

### Residual test: self-reinforcement fraction
- p=0.0: mean stay-fraction = 0.0656, median = 0.0833; attractors reaching
  50%: 0/120.
- p=1.0: mean stay-fraction = 0.0378, median = 0.0417; attractors reaching
  50%: 0/120.
- 240 of 8,217 extremal pairs stay in-cycle at p=0; 240 of 12,801 at p=1.
  240 = 120 attractors × 2 EXACTLY → the only staying move is the single
  (r,a) the railroad tie-break always picks. Every other extremal move
  (93–96%) escapes the attractor.

### What this proves (L1)
1. The 2-cycle is a measure-zero point in tie-space. Its survival depends
   completely on the deterministic lexicographic tie-break; replace that
   projection by any other selector and the cycle dissolves.
2. Both natural mechanism explanations are Rule-8 CLOSED:
   - Z28: scalar Lyapunov X_{t+1} < X_t (refuted)
   - Z29a: tie-class discrete fixed point (refuted, 0–1%)
   - Z29b: coarse basin self-reinforcement ≥ 50% (refuted, ~4–7%)
3. The entire observed basin uniqueness is produced by canon() merging
   degenerate extremal choices after a symmetric-exchange step, under one
   fixed tie-break; it has no independent dynamical invariant.

### Rule-8 closures
- Tie-class fixed-point avenue: CLOSED.
- Coarse basin self-reinforcement avenue: CLOSED.

---

## PHASE Z30 — TIE-DEGENERACY DYNAMICS ENGINE

Goal: verify that the period-2 lock is a selector-level phenomenon sitting
in a tie-degeneracy shell, and characterize the shell.

### Control (mandated first)
- z30_control_test.py verifies on 40 random (10,15) seeds, p=0:
  - (A) engine's own T with its Z25-b RNG protocol → period 2, 40/40
  - (B) manual re-implementation of full-sort tie-break (rem[0], add[-1]) →
    period 2, 40/40
- Earlier exploratory file z30_tie_dynamics.py used a faulty 'lex' selector
  (min on extremal SUBSETS, not full tie-broken lists). Its 'lex: period 24'
  output was a harness artifact; all Z30 numbers come from the verified
  z30_engine.py.

### L1 (exact / verified)
- **EX1 — random selector (300 seeds):** All 300 converged. Period spectrum:
  2: 157, 3: 48, 4: 22, 5: 22, 7: 15, 6: 14, 8: 6, 9: 8, 10: 4, 11: 3, 14: 1.
  Attractor τ = (|R|,|A|) histogram (top): (6,2): 242, (15,24): 19,
  (6,20): 19, (3,6): 6, (14,2): 6, (12,15): 3, (4,3): 2. Distinct τ across
  all random runs: 10.
- **EX2 — selector independence (200 seeds/selector):**
  - lex: period 2 in 200/200; mean |R|=6.57, |A|=6.34, HD=4.45
  - random: period 2 in 101/200; mean |R|=6.54, |A|=4.76, HD=4.16
  - entropy: period 2 in 200/200; mean |R|=7.60, |A|=10.31, HD=5.56
  - autmin: period 2 in 200/200; mean |R|=5.36, |A|=3.71, HD=3.88
- **EX3 — Level-B quotient collapse along random trajectories:**
  S(t) = # distinct canon classes among full R×A successors:
  S(0) = 2.65 → S(8) = 11.33 → S(32) not applicable for ~1/3 of short
  trajectories. H_D trajectory mean: 1.0 → 2.88 (rises; NOT monotone, NOT
  conserved).

### L2 (synthesis)
The period-2 is a selector attractor in *tie-space*, not a property of the
raw extremal-exchange on labeled graphs. Any deterministic extremal tie-break
with a stable bias direction locks onto it; the uniform-random selector
wanders into it only half the time. The attractor lives in a narrow tie-
degeneracy shell τ ∈ {(6,2)...(6,6)}, shared across selectors independently
of their individual trajectories. That shell is the true weak invariant the
dynamics concentrates onto.

### L3 (conjecture → tested in Z31)
The tie-shell σ(N,M) is computable directly: the joint law of (|R|,|A|) over
extremal-exchange orbits converges, for each (N,M), to a small support on
Z⁺². If σ characterizes the quotient's measurable image under any fair
extremal selector, the collapse is fully closed: a number-theoretic property
of the pair-action of S_N, not of the selector.

### Rule-8 closures
- Harness bug (faulty lex tie-break → period-24 artifact) superseded by
  verified control runs.

---

## PHASE Z31 — TIE-SHELL LAW ENGINE

Goal: test whether σ(N,M) is a stable limit law and whether the dynamics'
attractor distribution matches it.

### L1 (exact)
- **Phase 1 — σ(N,M) on the quotient:** At fixed density ρ, σ concentrates
  as N grows: support expands slowly (16→36 at ρ=0.3) while the mean (|R|,|A|)
  converges to the (1,1) mode at ρ=0.5. A stable limit law σ(ρ) appears to
  exist (Poisson-like profile peaked at (1,1), tails in both directions).
- **Phase 2 — scaling law:** At ρ=0.5, σ(N,M) is essentially N-independent
  for N≥10: means (1.78,1.72) at N=10 vs (1.73,1.73) at N=12; top atoms
  identical. At ρ=0.3 a singular low-N regime (N=8, (8,20) atom at 0.97)
  washes out by N=10.
- **Phase 3 — shell prediction:** Naive first-moment normal-approx estimator
  is wrong in sign and shape (predicted/observed ratio 0.39–0.56 for |R|,
  0.31–0.56 for |A|). The (1,1) atom excess mass is NOT captured by moment
  methods. The correct estimator requires Aut-aware Burnside weighting.
- **Phase 4 — dynamic verification:** The *unweighted* shell is NOT the
  target. At t=0 the on-shell fraction reads 1.0 only because the Burnside-
  weighted σ over-weights high-|Aut| states; with raw uniform support
  trajectories sit off-shell 95% of the time by t=9. The dynamics converges
  to the *max-|Aut| region of the weighted shell*.
- **Phase 5 — selector removal:** TV distances over attractor τ-distributions
  (120 runs each selector):
  - lex vs random: 0.100
  - lex vs entropy: 0.492
  - lex vs autmin: 0.275
  - random vs entropy: 0.525
  - random vs autmin: 0.275
  - entropy vs autmin: 0.542
  There is NO selector-invariant attractor law. The genuinely invariant
  structure is the weighted, high-|Aut| shell.

### L2 (synthesis)
The collapse mechanism is pinned: extremal exchange drives orbits toward the
high-automorphism region of the quotient; σ(N,M) tilts probability mass onto
exactly that region; every deterministic extremal selector then locks onto a
period-2 cycle sitting in the weighted shell. The "geometry of possible
futures" is the Aut-weighted σ-law.

### Rule-8 closures
- Burnside-weighted σ validated on N=6 exhaustive ground truth (unlabeled
  counts match OEIS; complement symmetry M → 15-M holds).
- Phase-4 "paradox" (t=0 on-shell=1.0) resolved in-phase: weighting artifact,
  not dynamics artifact.

---

## PHASE Z32 — STATIONARY MEASURE vs BURNSIDE WEIGHTING

Goal: decide whether the high-|Aut| endpoint is generative (dynamics drives
|Aut| up) or revealing (dynamics tracks a pre-existing quotient weighting).
Pre-registered: Outcome A iff TV(P_D, P_ref) ≤ 0.25 with 2× margin.

### Two harness faults (Rule 8 — both recorded before results)

1. **WL-proxy |Aut| is anti-correlated with the high-symmetry region.**
   z25b_engine_v2.aut_size returns a WL-color-budget lower-bound proxy once
   the budget exceeds CANON_BUDGET. On a 10-cycle it reads 10! = 3,628,800
   instead of the true |Aut| = 20. Z31's Phase-1/3 |Aut| weights used this
   proxy; the proxy is exact below budget so Z31's numbers stand (sampled
   cells N≤12 stay in the low-|Aut| regime), but any N=10 phase asking about
   a symmetry-RICH region must not. Fixed by an exact backtracking counter
   keyed on edge-set, validated: C₁₀=20, Petersen=120, K₅+5iso=14400, rigid=1.

2. **`1/|Aut|` on labeled edge-sets is NOT the uniform quotient measure.**
   Exhaustive N=6 enumeration: sum(1/|Aut|)/6! overshoots the unlabeled
   class count by ×120.6 (M=6) and ×154.7 (M=7). The converse direction
   sum|Aut|/N! is correct and matches OEIS. The 1/|Aut| arm is ruled out as
   a quotient estimator.

### L1 (exact / forward-computed)
- All four selectors converge 100%. Deterministic selectors lock to median
  period 2 (reproduces Z30 under the corrected primitive).
- The attractor region sits at |Aut| ~ 900–17,280; uniform labeled mass sits
  at |Aut|=1, and the orbit-size gap (~10⁹) is computed, not fitted:
  P(labeled draw hits any attractor class) ~ 2×10⁻⁵ per 40,000 draws.
  Dynamics and labeled geometry disagree on where the mass is by a factor
  that admits no statistical rescuing.
- TV to either static reference = 1.0 for all selectors. Outcome A (geometry
  only, selector = bookkeeping) is refuted for the labeled/Burnside reference
  unambiguously.

### L2 (synthesis)
The collapse is not "pure quotient geometry + bookkeeping selector." The
bookkeeping reference the quotient supplies (orbit/Burnside measure) is
concentrated ~10⁹ away from where the dynamics parks. The surviving
statement is closer to a sharpened Outcome B, but in the opposite causal
direction from prior phases: it is not "a universal measure the dynamics
reveals," it is "the extremal exchange actively drives orbits several orders
of magnitude up the |Aut| gradient, far off the quotient's own counting
measure." The one-step drift mechanism d|Aut|/dt is the specific next
measurement.

### Rule-8 closures
- 1/|Aut| as uniform quotient: CLOSED (×120–×155 overshoot at N=6 exhaustive).
- WL-proxy |Aut| at N≥10 in symmetry-rich regime: CLOSED.
- "Dynamics = quotient geometry + bookkeeping" (Outcome A): CLOSED.

---

## PHASE Z33 — SYMMETRY DRIFT LAW

Goal: measure the transient, not just the attractor, to determine whether the
|Aut| climb is generative (rule pushes up) or a seed/basin artifact.

### Pre-registered countermeasures (Rule 4)
- Trap 1 (survivorship): drift uses only pairs t<τ; post-cycle steps excluded
  from all means/medians.
- Trap 2 (bounded-walk log artifact): |Aut|≥1 means Δlog ≥ 0 trivially from
  |Aut|=1 states. Sign test excludes boundary states; positive mean with zero
  median and weak sign test is scored as artifact (Outcome C), not ascent.

### L1 (exact)
- Every selector climbs in net terms from |Aut|=1 seed to end-transient
  |Aut| 48–1440 (τ ~ 8–12 steps). Z32's attractor-level readings are the
  continuation of this climb, not a separate event.
- Per-window drift: mean_dAut > 0 everywhere (84–162 early), but
  median_dAut = 0 or 1, and frac_pos − frac_neg = 0.38–0.44 with sign-test
  p = 0.978/0.139/0.0218/0.357 (only entropy clears 0.05, and entropy has
  only one nonempty window).
- Validation pass (random, 1768 pairs): P(dAut>0)=0.360, P(dAut=0)=0.578,
  P(dAut<0)=0.063. Deciles [0,0,0,7,64,10032]. The positive mean is
  produced almost entirely by rare very large upward jumps on a background
  of exact zeros — a **staircase of rare large jumps**, not a Lyapunov drift.
- Conditional drift: (R,A)=(6,2) shell (the attractor) contributes E[dAut]=0,
  frac_pos=0. All climb lives in sparse-tie transient shells: (1,1) E=+1052,
  (1,3) E=+1047, (1,2) E=+815, (2,1) E=+22. The system ends where there
  is no climb left to make.

### L2 (synthesis)
Outcome B, operationally. The trajectory starts at the typical labeled point
(|Aut|=1, the 71%-mass mode per Z32) and within τ ~ 8–12 steps executes a
small number of large |Aut| jumps against a background of exact-zero steps.
After cycle entry the drift is exactly zero because the (6,2) attractor
shell carries no climb. The symmetry is "basin-like" in the specific sense
that the climb is front-loaded and concentrated in sparse-tie shells, and
the attractor inherits the summit. The "rule creates symmetry" reading is
too strong: the rule does not exert a persistent directional force (median
drift = 0 throughout), it supplies occasional large jumps whose arrivals are
timed by when a sparse tie appears.

### Rule-8 caveats
- Median |Aut| start = 1 is partly "selection of a typical start" (uniform-
  labeled seeding).
- 30+ window is empty for every selector: transients at (10,15) are too short
  to populate it; its emptiness is reported, not smoothed.

---

## PHASE Z34 — JUMP ANATOMY: WHAT CREATES |Aut| JUMPS?

Goal: decompose the Z33 staircase into structural events to determine whether
|Aut| jumps are twin creation (H1), component cloning (H2), or require a
new invariant (H3).

### Epistemic redesign (Rule 8, before main run)
A multiplicative TF*CF coverage test is ill-posed because twins and
isomorphic-singleton-components overlap (star+5iso: true aut = 4!·5! = 2880,
naive TF*CF_full = 345600). The experiment switched to event indicators per
step: E_twin (twin-class multiset changed), E_clone (a component iso-class
gained a member). Verdict reads event rates on jump set J vs off J.

### L1 (exact)
Jump set J: 384/1671 random, 284/850 lex, 236/689 entropy, 215/701 autmin
(22–34% of transient pairs are jumps).

  selector   n_jump  twin(J)   twin(off J)  ratio  clone(J)  clone(off J)  ratio
  random      384    1.000     0.2688       3.72   1.000      0.9965       1.00
  lex         284    1.000     0.3887       2.57   1.000      0.9965       1.00
  entropy     236    0.9958    0.4305       2.31   1.000      0.9934       1.01
  autmin      215    1.000     0.2798       3.57   1.000      1.000        1.00

- **H2 (clones) fails as a discriminator.** Clone event fires on ~99–100% of
  ALL steps, jump or not (ratio ≈ 1.0). Universal events cannot explain what
  is special about jumps. Co-fire on J steps (~100%) is an artifact of
  clone's universality, not evidence of coupled mechanism.
- **H1 (twin creation/merger) passes.** Twin-class restructuring happens on
  ~100% of jumps but only ~27–43% of non-jumps. Rate ratio 2.3–3.7× exceeds
  the pre-registered 3× threshold for random and autmin, and narrowly misses
  for lex (2.57) and entropy (2.31). The qualitative pattern is universal
  across all four selectors, so Z33's "no selector-specific flow" is
  preserved: the mechanism is universal, only the magnitude of the ratio varies.
- **H3 (residual unexplained) is refuted.** <0.4% of J steps fire no event.
  Every jump is accompanied by twin-class restructuring.
- Sparse-tie gating is real but incomplete: J steps are more likely at
  (R≤2 or A≤2) than non-J (0.88–1.0 vs 0.73–0.85), but the difference
  vanishes for entropy (0.805 vs 0.806). The twin event is a much stronger
  discriminator than the (R,A) shell alone. Sparse ties create the
  conditions; twin restructuring carries the jump.

### L2 (mechanistic chain)
The Z26–Z34 picture in one causal line:

```
Z26 degree-sum extremization → vertices pushed to equal degree →
neighborhoods become more similar → twin classes form or merge →
|Aut| jumps by factorial factor → Z33 staircase shape.
```

The (R,A) shell is the gating condition (controls how constrained the
extremal choice is); the productive event is twin restructuring. This is
why Z33's conditional drift showed the (6,2) shell frozen (no climb left:
all twins already formed) and the sparse-tie shells carrying all the climb:
those are the shells where the extremal swap still has degrees to equalize.

### L3 (conjecture)
The quantitative relation between (R,A) and twin-formation probability is
now testable. Whether H1 persists at (N,M) cells with longer transients is
open; the 30+ window is still empty at (10,15).

### Rule-8 closures
- Multiplicative TF*CF decomposition: CLOSED (ill-posed for this graph
  family; double-counts singleton components).
- H3 (residual unexplained): CLOSED for this cell.
- Event-indicator design: established as the correct primitive.

---

## CONSOLIDATED LEDGER

### CLOSED
- Z25: RELATIONAL ENGINE produces no emergent ratios (FAILED, mechanism
  failure — contractive rule, no non-contractive recurrence).
- Z25-b: FOUR HARD QUESTIONS — Q1 (universal ratios) NO; Q2 (robustness)
  partial; Q3 (generative surplus) not met under sharpening; Q4 (no hidden
  tuning) YES.
- Z26: BASIN SEED-DRIVEN (Theorem A); NO-FREE-LUNCH (Theorem B, 20× gap);
  PERIOD-2 MECHANISM (level-set boundary, not projection); UNIQUENESS-BY-
  SINGLETON DISPROVED (tie-collapse theorem, not local injectivity).
- Z27: QUOTIENT IDENTIFIED (canon() = graph isomorphism); QUOTIENT COUNTED
  EXACTLY (Pólya, OEIS-validated); INFORMATION DECOMPOSITION (gauge 21.27
  bits + dynamical contraction 13.47 bits = total 34.76 bits = 38.33 − 3.58).
- Z28: SCALAR LYAPUNOV AVENUE CLOSED (no standard invariant is strictly
  one-sided on 1,152 steps).
- Z29: TIE-CLASS FIXED-POINT CLOSED (falsified at 0–1%); COARSE BASIN
  SELF-REINFORCEMENT CLOSED (refuted, ~4–7%).
- Z30: TIE-DEGENERACY SHELL identified as the common object across selectors;
  LEVEL-B QUOTIENT BRANCHING characterized (expands then contracts);
  PRIVILEGE (canon tie-break) closed.
- Z31: σ(N,M) LIMIT LAW partially closed (Poisson-like, N-independent at
  N≥10, ρ-determined); SHELL PREDICTION partial (naive estimator fails,
  Burnside-weighted estimator correct); SELECTOR REMOVAL closed (no invariant
  law, weighted shell is invariant).
- Z32: QUOTIENT GEOMETRY ONLY (Outcome A) CLOSED; WL-PROXY |Aut| at N≥10
  CLOSED; 1/|Aut| AS UNIFORM QUOTIENT CLOSED (×120–×155 overshoot at N=6).
- Z33: GENERATIVE-vs-REVEALING causality resolved (Outcome B: transient jump
  process); STAIRCASE OF RARE LARGE JUMPS identified as the drift shape;
  CONDITIONAL DRIFT separates sparse-tie shells (climb) from (6,2) shell
  (frozen).
- Z34: JUMP MECHANISM (Z33's "what is a jump") CLOSED — H1 (twins)
  confirmed, universal across all four selectors, gated by sparse (R,A) ties.
  H2 (clones) refuted as discriminator. H3 refuted for this cell.
  MULTIPLICATIVE TF*CF DECOMPOSITION CLOSED (ill-posed).

### OPEN
- (i) Tie-collapse theorem: prove add-unique / remove-tie-collapse (Z26)
  forces exactly zero post-cycle drift. Z34 adds the mechanism (no twins left
  to form) that makes the attractor the natural endpoint, but a proof is not
  yet written.
- (ii) Quantitative (R,A) → twin-formation probability: partially answered —
  sparse ties constrain the extremal choice, making neighborhood equalities
  more likely. The exact functional form is testable but not yet measured.
- (iii) H1 at larger (N,M) cells: the 30+ window is empty at (10,15); a
  larger cell is needed to test whether twin-driven jumps continue or
  saturate, and whether the staircase shape persists.
- (iv) Exact generating function for Aut-weighted σ(N,M): the single item
  that would close the collapse problem at the level Z31's L3 demanded.
- (v) Z25-b relational engine: needs non-contractive recurrence (witness
  edges must replace, not only accumulate) to lift above FAILED.

---

## PHASE INDEX

| Phase | Title | Status | Key L1 result |
|-------|-------|--------|---------------|
| Z25 | Relational origin engine | FAILED | No emergent ratios; contractive |
| Z25-b | Four hard questions | PARTIAL | Universality/robustness fail; compression confirmed |
| Z26 | Basin / period-2 / info | CLOSED | Seed-driven basin; 20× info gap; tie-collapse theorem |
| Z27 | Quotient / universality | CLOSED | canon() = isomorphism; |Q_10,15| = 136,433 |
| Z28 | Pushforward measure / invariant | CLOSED | H(μ)=7.46 bits; no scalar Lyapunov |
| Z29 | Tie-class support | CLOSED | Tie-class fixed point falsified 0–1% |
| Z30 | Tie-degeneracy dynamics | CLOSED | Period-2 = selector attractor in tie-space; τ ~ (6,2) |
| Z31 | Tie-shell law | PARTIAL | σ(N,M) limit law; weighted shell is invariant |
| Z32 | Stationary vs Burnside | CLOSED | Outcome A refuted; static sampler blind by ~10⁹ |
| Z33 | Symmetry drift law | CLOSED | Outcome B: front-loaded staircase of rare jumps |
| Z34 | Jump anatomy | CLOSED | H1 (twins) confirmed; H2 (clones) refuted; H3 refuted |
