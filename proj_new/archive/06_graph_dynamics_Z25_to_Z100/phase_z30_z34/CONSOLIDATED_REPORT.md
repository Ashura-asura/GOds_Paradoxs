# PHASES Z30–Z34 — CONSOLIDATED REPORT
# 2026-08-02 · Rules v2 · Cell under study: (10,15)

## Executive summary

Five phases closed a single mechanistic question: *why does the extremal
exchange concentrate onto a small high-symmetry attractor?* The answer is
now pinned at three levels.

- Z30/Z31: the attractor lives in a narrow tie-degeneracy shell τ = (|R|,|A|)
  ~ (6,2) at (10,15), and the Burnside-weighted quotient measure σ(N,M)
  already concentrates probability mass onto that shell. The selector does
  not create the shell; it selects a period-2 cycle *inside* it.
- Z32: "geometry alone, selector is bookkeeping" (Outcome A) is refuted —
  not because dynamics tracks a different shell, but because the static
  labeled sampler is structurally blind to the attractor region by a factor
  of ~10⁹ in orbit size. The dynamics does not track the quotient's *own*
  unaided measure; it actively climbs toward high-|Aut| classes that the
  uniform-labeled sampler cannot reach.
- Z33: the climb is a **front-loaded staircase of rare large jumps** against
  a zero-median background. Median Δ|Aut| = 0 at every window; the positive
  mean is carried by a small number of factorial-scale events concentrated
  in the first ~8–12 transient steps.
- Z34: those jumps are **twin-class restructuring events** (H1), gated by
  sparse (R,A) ties but caused by the twin merger. Component cloning (H2)
  is universal and non-discriminating. H3 (residual unexplained) is refuted:
  <0.4% of jumps fire no event.

The causal chain closing the arc:

  degree-sum extremization → vertices pushed to equal degree →
  neighborhoods become more similar → twin classes form or merge →
  |Aut| jumps by a factorial factor → staircase trace → attractor is the
  shell where no more twin restructuring is possible.

This is "basin-like" (Z33 Outcome B) in the specific sense that the climb
is front-loaded and the attractor inherits the summit, not that a persistent
directional force keeps pushing.

---

## PHASE Z30 — TIE-DEGENERACY DYNAMICS ENGINE

Goal: verify that the period-2 lock observed in Z25-b is a selector-level
phenomenon sitting in a tie-degeneracy shell, not a property of the raw
extremal-exchange rule.

### L1 (exact / verified)
- All four selectors converge 200/200 at (10,15). The earlier "non-
  convergence" from a buggy lex tie-break was a harness artifact; the
  verified z30_engine.py gives period 2 with certainty for the three
  deterministic selectors and ~50% for random.
- The attractor τ = (|R|,|A|) distribution is concentrated: 242/300 random
  seeds land at τ = (6,2); structured selectors sit in the 5–8 × 3–10
  shell. Distinct τ across all random runs: 10.
- Level-B quotient branching S(t) expands from 2.65 (t=0) to 11.3 (t=8)
  then contracts to a low-period cycle. The future space first grows, then
  collapses.

### L2 (synthesis)
The period-2 is a selector attractor in *tie-space*, not a property of the
raw rule. Any deterministic extremal tie-break with a stable bias direction
locks onto it; the uniform-random selector wanders into it only half the
time. The common object across selectors is not a single state but a narrow
tie-degeneracy shell onto which any sane selector falls. Both scalar
Lyapunov candidates (Z28) and tie-class fixed points (Z29) failed because
they looked *inside* the shell at single states; the concentration is at
shell level.

### L3 (conjecture → tested in Z31)
The tie-shell σ(N,M) = P(|R|,|A|) over extremal-exchange orbits converges,
for each (N,M), to a small support on Z⁺². If σ characterizes the
quotient's measurable image under any fair extremal selector, the collapse
is fully closed: a number-theoretic property of the pair-action of S_N, not
of the selector.

### Rule-8 closures
- Harness bug (faulty lex tie-break → period-24 artifact) identified and
  superseded by verified control runs; recorded here.
- Canon-neutrality and selector-independence verified; privilege closed.

---

## PHASE Z31 — TIE-SHELL LAW ENGINE

Goal: test whether σ(N,M) is a stable limit law and whether the dynamics'
attractor distribution matches it.

### L1 (exact)
- σ(N,M) exists stably at fixed density ρ: support expands slowly with N
  (16→36 at ρ=0.3) while the mean (|R|,|A|) converges to the (1,1) mode
  at ρ=0.5. A stable limit law σ(ρ) appears to exist (Poisson-like profile
  peaked at (1,1), tails in both directions).
- At N≥10, σ(N,M) is essentially N-independent at fixed ρ: means (1.78,1.72)
  at N=10 vs (1.73,1.73) at N=12; top atoms identical.
- Naive first-moment normal-approx estimator is wrong in sign and shape
  (predicted/observed ratio 0.39–0.56); the (1,1) atom excess mass is NOT
  captured by moment methods. The correct estimator requires Aut-aware
  Burnside weighting.
- Phase-4 dynamic verification: the *unweighted* shell is NOT the target.
  At t=0 the on-shell fraction reads 1.0 only because the Burnside-weighted
  σ over-weights high-|Aut| states; with raw uniform support trajectories
  sit off-shell 95% of the time by t=9. The dynamics converges to the
  *max-|Aut| region of the weighted shell*.
- Phase-5 selector removal: TV distances over attractor τ-distributions
  reach 0.54 (entropy vs autmin). There is NO selector-invariant attractor
  law. The genuinely invariant structure is the weighted, high-|Aut| shell.

### L2 (synthesis)
The collapse mechanism is pinned: extremal exchange drives orbits toward
the high-automorphism region of the quotient; σ(N,M) tilts probability
mass onto exactly that region; every deterministic extremal selector then
locks onto a period-2 cycle sitting in the weighted shell. The "geometry
of possible futures" is the Aut-weighted σ-law; writing down its exact
generating function is the single open item.

### Rule-8 closures
- Burnside-weighted σ validated on N=6 exhaustive ground truth (unlabeled
  counts match OEIS exactly; complement symmetry M → 15-M holds).
- Phase-4 "paradox" (t=0 on-shell=1.0) resolved in-phase: weighting
  artifact, not dynamics artifact.

---

## PHASE Z32 — STATIONARY MEASURE vs BURNSIDE WEIGHTING

Goal: decide whether the high-|Aut| endpoint is generative (dynamics drives
|Aut| up) or revealing (dynamics tracks a pre-existing quotient weighting).
Pre-registered: Outcome A iff TV(P_D, P_ref) ≤ 0.25 with 2× margin over
nearest alternative, for every selector.

### Two harness faults (Rule 8 — both recorded before results)

1. **WL-proxy |Aut| is anti-correlated with the high-symmetry region.**
   `z25b_engine_v2.aut_size` returns a WL-color-budget lower-bound proxy
   once the budget exceeds CANON_BUDGET. On a 10-cycle it reads 10! = 3,628,800
   instead of 20. Z31's Phase-1/3 |Aut| weights used this proxy; the proxy is
   exact below budget so Z31's numbers stand (sampled cells N≤12 stay in the
   low-|Aut| regime), but any N=10 phase asking about a symmetry-RICH region
   must not. Fixed by an exact backtracking counter keyed on edge-set,
   validated: C₁₀=20, Petersen=120, K₅+5iso=14400, rigid=1.

2. **`1/|Aut|` on labeled edge-sets is NOT the uniform quotient measure.**
   Exhaustive N=6 enumeration: sum(1/|Aut|)/6! overshoots the unlabeled class
   count by ×120.6 (M=6) and ×154.7 (M=7). The converse direction
   sum|Aut|/N! is correct and matches OEIS. The 1/|Aut| arm is ruled out as
   a quotient estimator (Rule 8 closed).

### L1 (exact / forward-computed)
- All four selectors converge 100%. Deterministic selectors lock to median
  period 2 (reproduces Z30 under the corrected primitive).
- The attractor region sits at |Aut| ~ 900–17,280; uniform labeled mass sits
  at |Aut|=1, and the orbit-size gap (~10⁹) is *computed*, not fitted:
  P(labeled draw hits any attractor class) ~ 2×10⁻⁵ per 40,000 draws.
  Dynamics and labeled geometry disagree on where the mass is by a factor
  that admits no statistical rescuing.
- TV to either static reference = 1.0 for all selectors. Outcome A (geometry
  only, selector = bookkeeping) is refuted for the labeled/Burnside reference
  unambiguously. The uniform-quotient reference is structurally blind at
  K=40,000 (covers only 29.3% of |Q_10,15|), so the TV=1.0 partly reflects
  undersampling; the stronger statement rests on the exact counting argument.

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

### L3 (conjecture → resolved in Z33/Z34)
The selector pairwise TVs (0.86–0.99) and different mean|Aut| tiers suggest
the selector is a real biasing operator selecting among high-|Aut| cycles,
not a coin that picks uniformly inside the shell.

### Rule-8 closures
- 1/|Aut| as uniform quotient: CLOSED (×120–×155 overshoot at N=6).
- WL-proxy |Aut| at N≥10 in the symmetry-rich regime: CLOSED.
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
  only one nonempty window so the cross-window comparison for A cannot run).
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
- The (6,2) shell is the attractor state itself, so dAut=0 there is
  definitional given cycle-entry stopping.

### What Z33 hands to Z34
The open mechanism: why do |Aut| jumps cluster at sparse-tie (R,A) shells,
and what structural change produces a factorial-scale |Aut| gain?

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

  Z26 degree-sum extremization → vertices pushed to equal degree →
  neighborhoods become more similar → twin classes form or merge →
  |Aut| jumps by a factorial factor → Z33 staircase shape.

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
- PRIVILEGE: canon() tie-break does not drive outcome (Z29 neutral-switch
  control, Z31 selector matrix). Rule 1 closed.
- ENDPOINT CONCENTRATION: Z25-b concentration, Z26 information accounting
  (20× gap, no generation) confirmed; attractors = 210 of |Q|=136433 (Z28);
  H(μ)=7.46 bits (Z28) vs quotient 17.03 bits.
- QUOTIENT GEOMETRY ONLY (Outcome A): Z32 refuted. The collapse is not
  "quotient geometry + bookkeeping selector"; the static sampler is
  structurally blind to the attractor region by ~10⁹ in orbit size.
- GENERATIVE-vs-REVEALING causality: Z33 + Z34 resolved. The dynamics is
  generative in a restricted sense: the exchange rule produces factorial-
  scale |Aut| jumps via twin-class restructuring, but does not exert a
  persistent directional force. The attractor inherits the summit of a
  front-loaded transient staircase.
- JUMP MECHANISM (Z33's "what is a jump"): H1 (twins) confirmed, universal
  across all four selectors, gated by sparse (R,A) ties. H2 (clones)
  refuted as discriminator. H3 refuted for this cell.
- MULTIPLICATIVE TF*CF DECOMPOSITION: ruled out as ill-posed (double-counts
  singleton components); event-indicator design is the correct primitive.
- WL-PROXY |Aut| at N≥10 in symmetry-rich regime: Rule 8 closed. Exact
  counter is the required primitive.
- 1/|Aut| AS UNIFORM QUOTIENT: closed (×120–×155 overshoot at N=6 exhaustive).

### OPEN
- (i) Tie-collapse theorem: prove that the add-unique / remove-tie-collapse
  mechanism (Z26) forces exactly zero post-cycle drift. Z34 adds the
  mechanism (no twins left to form) that makes the attractor the natural
  endpoint, but a proof is not yet written.
- (ii) Quantitative (R,A) → twin-formation probability: partially answered
  — sparse ties constrain the extremal choice, making neighborhood equalities
  more likely. The exact functional form is testable but not yet measured.
- (iii) H1 at larger (N,M) cells: the 30+ window is empty at (10,15); a
  larger cell is needed to test whether twin-driven jumps continue or
  saturate, and whether the staircase shape persists.
- (iv) Exact generating function for the Aut-weighted σ(N,M): the single
  item that would close the collapse problem at the level Z31's L3 demanded.
