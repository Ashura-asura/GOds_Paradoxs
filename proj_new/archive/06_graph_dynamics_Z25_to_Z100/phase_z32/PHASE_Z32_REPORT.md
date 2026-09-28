# PHASE Z32 — STATIONARY MEASURE vs BURNSIDE WEIGHTING
# Rule-8 closed · 2026-08-02
# Script: phase_z32\z32_stationary_vs_burnside.py (exact |Aut| backtrack; canon + exact-aut keyed)

## What the phase set out to decide

Z31 left one open fork. The attractor region is symmetry-rich; is that
caused by the dynamics (Hypothesis A: T actively drives |Aut| up) or only
revealed by it (Hypothesis B: T samples a pre-existing quotient weighting,
the selector is bookkeeping)? The phase's pre-registered decision rule was:
Outcome A iff, for every selector, the dynamic stationary measure matches
the Burnside/orbit measurement within TV <= 0.25 with a 2x margin over its
distance to the competing static base measure.

## Two harness faults surfaced before any result — both recorded (Rule 8)

1. **The project's canonical-label primitive lies about |Aut| where it
   matters most.**  `z25b_engine_v2.aut_size` returns a WL-color-budget
   "lower bound proxy" once the budget exceeds CANON_BUDGET=20000; the
   engine header itself flags this as a declared-L2 approximation. On a
   10-cycle that branch returns 10! = 3,628,800 instead of the true |Aut|
   = 20. The effect is *anti-correlated* with exactly the high-symmetry
   region Z32 exists to measure. Z31's Phase-1/3 |Aut| weights used this
   proxy; the proxy is exact below budget so Z31's *numbers* stand (its
   sampled cells, N<=12, stay in the low-|Aut| regime where the proxy is
   exact), but any N=10 phase asking about a symmetry-RICH region must not.
   **Fix (this phase):** a memoized exact backtracking automorphism counter
   keyed on the labeled edge-set, validated against closed-form targets on
   C_10 (20), Petersen (120), K_5 + 5 isolated (14,400), rigid draws (1).
   This correction is the reason the Z32 numbers below are exact rather
   than approximate.

2. **The "1/|Aut| reweighting => uniform quotient" identity (Z31's Phase-1
   method line) fails catastrophically at N=6 exhaustive ground truth.**
   Enumerating all 2^15 labeled graphs at N=6: unlabeled counts recover
   exactly (sum|Aut|/6! = 21 at M=6, 24 at M=7 — matches OEIS, so the
   counter and the *|Aut|-weighted* Burnside arm are correct), but
   sum(1/|Aut|)/6! over the same labeled-uniform enumeration overshoots
   the class count by x120.6 (M=6) and x154.7 (M=7). The 1/|Aut|-weighted
   labeled arm is, measurably, NOT the uniform quotient measure. Any
   conclusion from matching dynamics to such an arm (Z31's Phase-4 support
   test included) rests on a mislabeled reference. The two correct static
   references are (i) uniform-on-labeled keyed on canon (= orbit measure
   proportional to 1/|Aut|, the true Burnside) and (ii) first-hit-
   rejection uniform on quotient classes. Both are used below.

## Experiment — four selectors, stationary/attractor sampling

(N,M) = (10,15). Selectors random / lex / entropy / autmin, 180 chains
(stochastic) or 90 (deterministic), cap 512 steps, canon-revisit break.
Per pre-registration change forced by fault #2 (recorded before reading
results): sampling is on the *attractor* (post-first-revisit cycle
states), matching the Z28/Z30 precedent that the object of interest is
mu = (T^inf . canon)_* of the seed measure. All selectors converge:

    selector   converged  med_period   distinct canon keys   mean|Aut|  max|Aut|
    random      180/180       2.0              558             1,913.8   17,280
    lex          90/90        2.0              122             2,313.1   17,280
    entropy      90/90        2.0              176               922.3    2,880
    autmin       90/90        2.0              174             1,087.2   17,280

  The period-2 lock for every deterministic selector, and the ~50%
  period-2 / diffuse picture for random, reproduce Z30 EX2 under the
  corrected estimator — the Z30 dynamics results stand. (Z30's *lex*
  columns were produced with the buggy tie-break documented in Z30's own
  ledger; the engine-corrected "railroad" tie-break used here matches Z30's
  verified `z30_engine` behavior.)

## The decisive negative measurement (L1): the static sampler is blind

Uniform-labeled (10,15) draws have |Aut|=1 with probability ~0.71, and
over 40,000 draws the largest |Aut| seen is 48. Meanwhile the attractor
classes carry |Aut| = 1,440 (the (R,A)=(6,2) attractor's canonical form),
2,880, 17,280. Orbit-stabilizer makes the blindness quantitative and
exact:

    P(one labeled draw lands in a class of given |Aut|) = (N!/|Aut|) / C(45,15)

    |Aut|        orbit size    P(hit in 1 draw)   E[hits] in K=40,000
       48         75,600        2.19e-07           8.8e-03
    1,440          2,520        7.31e-09           2.9e-04
   17,280            210        6.09e-10           2.4e-05
   (to see even ONE attractor-family hit once in expectation needs a
    class with |Aut| <= 0.42 — impossible, so K=40,000 can see NONE)

No static weighting convention can fix this: the attractor region is
invisible to *any* estimator built on uniform labeled samples at this
budget, because its orbits are ~10^9 times smaller than the typical
labeled graph's. This is the concrete mechanism under the Z31 Phase-4
anomaly (t=0 on-shell=1.0 only when the shell was built from the
|Aut|-weighted reference): the weighting isn't a subtle correction, it
decides which tenth of the quotient the question is even about.

## TV results

    selector    TV vs quotient-uniform   TV vs labeled(Burnside)   TV vs random
    random            1.0                      1.0                   0.0
    lex               1.0                      1.0                   0.9666
    entropy           1.0                      1.0                   0.9866
    autmin            1.0                      1.0                   0.9816

    pairwise selector TV: lex-autmin 0.9944,  random-lex 0.9666,
    entropy-autmin 0.8611 (closest pair), random-entropy 0.9866.

Consequence for the pre-registered decision rule: Outcome A not met for
any selector — TV to *either* static reference is 1.0. The Z32 question
("geometry alone, selector=bookkeeping") is therefore refuted for the
labeled/Burnside reference unambiguously. It is NOT refuted for the
uniform-quotient reference by this run alone, because the static uniform-
quotient arm covers only 29.3% of |Q_10,15| and the resulting TV=1.0
partly reflects undersampling (D3 diagnostic fails), not only genuine
disagreement. That limitation is stated plainly; the stronger statement
below rests on the exact counting argument, which needs no sampling.

## Verdict, labeled per Rule 3

**L1 (exact / forward-computed):**
- All four extremal selectors converge 100% at (10,15); deterministic ones
  lock to median period 2 (reproduces Z30 under the corrected primitive).
- The attractor region sits at |Aut| ~ 900–17,280; uniform labeled mass
  sits at |Aut|=1, and the orbit-size gap (~10^9) is *computed*, not
  fitted: P(labeled draw hits any attractor class) ~ 2e-5 per 40,000
  draws. Dynamics and labeled geometry disagree on where the mass is, by
  a factor that admits no statistical rescuing.
- sum(1/|Aut|) over labeled-uniform != quotient-uniform (x120–x155 at
  N=6 exhaustive): that weighting direction is ruled out as a quotient
  estimator. (Its converse, sum|Aut|/N!, is correct and matches OEIS.)
- The project engine's `aut_size` returns WL-budget lower bounds above
  CANON_BUDGET — a declared-L2 approximation that silently contaminates
  any |Aut|-weighted conclusion at N>=10 in the symmetry-rich regime.
  Replaced here by an exact counter keyed on edge-set.

**L2 (synthesis, marked):**
- Outcome A as *pre-registered* is refuted. The collapse is not "pure
  quotient geometry + bookkeeping selector": the bookkeeping reference the
  quotient supplies (orbit/Burnside measure) is concentrated ~10^9 away
  from where the dynamics parks. Under the only reading of "geometry" the
  quotient actually defines unaided, the dynamics does not track it.
- The surviving statement is closer to a sharpened Outcome B, but in the
  opposite causal direction from prior phases: it is not "a universal
  measure the dynamics reveals," it is "the extremal exchange actively
  drives orbits several orders of magnitude up the |Aut| gradient, far
  off the quotient's own counting measure." Why the high-|Aut| region is
  absorbing — i.e. the one-step drift mechanism d|Aut|/dt — is not
  measured here (every run sampled only cycle states), and is the
  specific next measurement.

**L3 (conjecture):**
- The selectors' pairwise TVs (0.86–0.99) and their different
  mean|Aut| tiers (lex 2,313 > autmin 1,087 > entropy 922 > random 1,914 —
  note random and lex swap rank) suggest the selector is a real
  *biasing operator* selecting among high-|Aut| cycles, not a coin that
  picks uniformly inside the shell. Whether that bias decomposes as
  (universal drift) + (selector-specific tilt on a shared high-|Aut|
  support) is open and testable at Z33.

## What Z32 therefore hands to Z33

1. Replace |Aut| *snapshot-at-attractor* with a drift measurement: along
   non-attractor trajectories, record d|Aut|/dt vs t. The single curve
   "trajectory |Aut|(t) vs the labeled/Burnside null" decides whether the
   symmetry rise is generative (positive drift, falsifies B) or a
   boundary effect of already-symmetric inputs (no drift, rescues a weak B).
2. Static reference must be built by quotient-uniform sampling with full
   |Q_10,15| coverage (e.g. Pólya-exact class generation or a much larger
   K with importance correction), not by labeled-uniform draws — the
   latter is provably blind at K <= 10^6 for this cell.
3. The corrected |Aut| counter (exact, backtracking) is the required
   primitive for any N=10 symmetry statement going forward; the WL-budget
   proxy is Rule-8 closed for |Aut|-weighted claims at N>=10.

## Ledger

- Rule 1: no numerology/physics strings anywhere. PASS.
- Rule 2: thresholds (TV_UNIQUE_MATCH=0.25, margin=2.0), budgets
  (K_STATIC=40000, chains 180/90, cap 512, thin 5, samples/chain 40), and
  the four-selector battery were fixed before the decisive runs. The
  |Aut| counter was validated on closed-form targets (C_10=20,
  Petersen=120, K_5+5iso=14400, rigid=1) before any Z32 comparison used
  it. One pre-registered change, *decided before reading results*, moved
  dynamic sampling from transient tails to attractor states; the reason
  (fault #2 invalidates the transients' reference) and the change are
  both recorded above, per Rule 5.
- Rule 3: L1/L2/L3 split enforced in the Verdict section.
- Rule 4: two self-inflicted faults (WL-proxy |Aut|, 1/|Aut| weighting)
  were found only by checking against exhaustive N=6 ground truth mid-run;
  both are in this file with the failed numbers shown, not silently fixed.
- Rule 5: both faults documented with the same prominence as the result.
- Rule 6: RNG seeds declared (9100+131s dynamic, 424242 static); budgets
  are assay sizes, not fits.
- Rule 7: builds only on Z25b v2 engine behavior already established; the
  one primitive replaced (aut_size) is replaced with a strictly stronger
  exact object, and the replacement is itself validated.
- Rule 8: the 1/|Aut|-as-uniform-quotient avenue and the WL-proxy-|Aut|
  avenue are both now CLOSED, with the blocking mechanism stated
  (x120–x155 overshoot; WL budget ceiling). The "dynamics = quotient
  geometry + bookkeeping" reading (Outcome A) is closed.
- Rule 9: no fitted parameters; every count, |Aut| value, and expectation
  printed. The discriminator used (orbit-size gap ~10^9) is discriminating
  precisely because it would NOT have held if the attractor sat near
  |Aut|=1: it can be wrong, and that is what makes it a result.
