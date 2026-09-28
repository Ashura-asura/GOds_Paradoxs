# PHASE Z33 — SYMMETRY DRIFT LAW
# Rule-8 closed · 2026-08-02
# Files: phase_z33/z33_symmetry_drift.py
# Inputs: phase_z25/z25b_engine_v2.py, phase_z32 (exact |Aut|), phase_z31 (verified selectors)

## Addendum (2026-08-03, Rule-8 #2 canon fix) — every headline figure below RE-DERIVED

z25b_engine_v2.canon was not iso-invariant (asymmetric graphs returned their own labeling →
chain length/tau were labeled-state revisit times, inflated). With the in-repo iso-invariant
block canon fix (ledger 8.14), the exact same protocol gives:

| selector | median tau | |Aut| start (med) | |Aut| end-transient (med) | fold |
|----------|-----------|------------------|----------------------------|------|
| random   | 7         | 1.0              | 1440                       | 1440 |
| lex      | 7         | 1.0              | 1440                       | 1440 |
| entropy  | 7         | 1.0              | 1440                       | 1440 |
| autmin   | 6         | 1.0              | 1440                       | 1440 |

Old (buggy-canon) headline: tau 12/9/8/8; entropy/autmin transient folds 48/1440. All four
fold figures are now 1440 on the re-run. (10,15) tau median ≈ 7 matches the Z35 main cell (7)
and Z37 τ* (7). Entropy/autmin window statistics in the body below change accordingly; the
qualitative staircase-of-rare-jumps verdict is unchanged.

## Pre-registration recap (in-file header, 2026-08-02, before any run)

Question inherited from Z32: is the high-|Aut| endpoint *generative* (the exchange
rule pushes |Aut| up along the transient) or a *seed/basin* artifact (selection of
the start)? Measured per-step on the **transient** only: a chain stops at first
canon-revisit (= cycle-entry time tau), and drift pairs use only steps t < tau.
Post-cycle steps are excluded from all drift means/medians to avoid survivorship
bias, per the in-file "Trap 1" countermeasure. The sign test for A-vs-C excludes
boundary states with |Aut| = 1 (operationalization of "Trap 2": log-drift from a
bounded walk would read positive without arithmetic ascent).

Cell (10,15). Chains: random 200, lex 120, entropy 120, autmin 120 (100% converged
in all four). canon() is used ONLY to detect cycle entry; the measured object is the
labeled edge-set and its exact |Aut|. No WL proxy anywhere.

## Headline number, before the table

Every selector climbs hard in net terms from seed to the last transient step:

| selector | median tau | |Aut| start (med) | |Aut| end-transient (med) | fold |
|----------|-----------|------------------|----------------------------|------|
| random   | 12        | 1.0              | 1440                       | 1440 |
| lex      |  9        | 1.0              | 1440                       | 1440 |
| entropy  |  8        | 1.0              |   48                       |   48 |
| autmin   |  8        | 1.0              | 1440                       | 1440 |

Z32's attractor-level readings (mean |Aut| ~ 922–2313 on cycle states) are the
continuation of this climb, not a separate event.

## The drift distribution is heavy-tailed, not coherent — and that shapes the verdict

Per-window statistics on t < tau pairs (early = t 0–9, mid = 10–29, late = 30+).

random (n=1800 early, 426 mid, 0 late):
  early mean_dAut +140.4, median 0, frac_pos 0.48, frac_neg 0.07,
  geomean step mult 2.04, sign-p(excl boundary) 0.978
  mid   mean_dAut -34.0,  median 0, frac_pos 0.02, frac_neg 0.01, sign-p 1.000
lex (n=1012 early, 38 mid):
  early mean +161.8, median 1, sign-p 0.139 ; mid mean -111.2, sign-p 0.998
entropy (n=826 early only):
  early mean +83.8, median 1, sign-p 0.0218   (only window clearing 0.05)
autmin (n=840 early only):
  early mean +125.8, median 0, sign-p 0.357

Validation pass (random, 1768 pairs, 1%/99% trimmed mean = +92.3, raw mean +101.1):
  P(dAut>0)=0.360, P(dAut=0)=0.578, P(dAut<0)=0.063. Deciles of dAut:
  [0, 0, 0, 7, 64, 10032]. The positive mean is produced almost entirely by rare,
  very large upward jumps on a background of exact zeros — 58% of steps change
  |Aut| not at all. This is a **staircase of rare large jumps**, not a
  Lyapunov drift.

Orbit size N!/|Aut| under the same windows: median 302400 -> 2520 (random),
302400 -> 2520 (lex), 907200 (entropy, single window), 907200 (autmin).
Orbits shrink by roughly the fold-change above and the shrink tracks |Aut| growth
1:1 because N! is a fixed constant at N=10 — so "does orbit size shrink
monotonically" and "does |Aut| grow" are the same question here; no added
information, and Experiment 3's object is a rescaling, not a second observable.

## Conditional drift separates tie structure from symmetry

(random, top shells by sample count:)
  (R,A)=(6,2):  n=848, E[dAut]=0.000, frac_pos=0.000   <- attractor residence, frozen
  (1,1):        n=306, E[dAut]=+1052, frac_pos=0.788   <- sparse ties = big jumps
  (1,3):        n=179, E[dAut]=+1047, frac_pos=0.872
  (2,1):        n=167, E[dAut]=+22,   frac_pos=0.773
  (1,2):        n=132, E[dAut]=+815,  frac_pos=0.712

Same skeleton in the other selectors: the densest shell (6,2) is the attractor
state itself and contributes strictly zero drift; the drift lives entirely in the
sparse-tie transient shells (1,1)/(1,3)/(1,2)/(2,1). This directly cross-checks
Z31's sigma(N,M)=P(R)P(A) observation and Z30's tie-structure finding: the shell
the system *ends in* is the one with no climb left to make.

## Verdict (pre-registered decision table)

  A (generative ascent):  sign-p < 0.05 in every nonempty window for all
    selectors. NOT met. Sign-p early = 0.978, 0.139, 0.0218, 0.357; only entropy
    clears 0.05 and entropy has only a single nonempty window so the required
    cross-window comparison cannot run. Mean_dAut > 0 everywhere is real but is
    not the drift the outcome definition asks for, and Trap-2 (positive mean with
    zero median and weak sign test) screens it out of A/B by design.
  B (basin): positive-drift-early then decay to zero. NOT NOT-met. The mid-window
    decay IS visible (random mean +140 -> -34, frac_pos collapses to 0.02), and the
    heavy-tail decomposition says the early mean is jump-driven rather than
    coherent. B is the closest single label to "what the system does".
  C (correlated endpoint): zero drift / large fluctuations. NOT met as stated —
    there is clearly net climb (x48-1440). C as "no positive drift" is refuted.
  D (selector-defined flow): opposite signs of E[dAut] in the same window across
    selectors. NOT met — all four behave the same qualitatively (climb early,
    flatten at the cycle), differing only in magnitude of endpoint (entropy
    converges to |Aut|~48 vs 1440 for the others) and transient length.

### Outcome box
  **B, operationally.** Answer to "why they move there" at the level of this
  experiment: the trajectory starts from a uniform-labeled seed at |Aut|=1 (the
  typical point of the labeled space, per Z32's 71%-mass finding), and within the
  short transient (tau ~ 8-12 steps) executes a **small number of large |Aut|
  jumps against a background of exact-zero steps**; after cycle entry the drift
  is exactly zero because the (6,2) attractor shell carries no climb. So the
  symmetry is "basin-like" in the specific sense that the climb is front-loaded
  and concentrated in the transient's sparse-tie shells, and the attractor
  inherits the summit rather than climbing further. The "rule creates symmetry"
  reading is too strong: the rule does not exert a persistent directional force
  (median drift = 0 throughout), it supplies occasional large jumps whose
  arrivals are timed by when a sparse tie appears.

## Labeled failures / caveats (Rule 8)
  - Median |Aut| start = 1 is an artifact of uniform-labeled seeding (71% of
    (10,15) labeled graphs are asymmetric, Z32). The fold-change table is
    therefore partly "selection of a typical start". The internal countermeasure
    is that drift is measured *within* the transient, not inferred from endpoints.
  - 30+ window is empty for every selector: transients at (10,15) are too short
    to populate it. Its emptiness is reported, not smoothed.
  - The densest shell (6,2) is the attractor state itself, so dAut=0 there is
    definitional given cycle-entry stopping, not a finding of stillness in the
    ambient space.

## Ledger (consolidated, phases Z25-Z33)
  PRIVILEGE: canon() tie-break does not drive outcome (Z29 neutral-switch control,
    Z31 selector matrix). Rule 1 closed.
  NOISE ROBUSTNESS: Z25-c and Z27 fragility side-channel open — Z27 sharpened to
    t0-asymptotic exponential, Z29 held under selector changes, Z31 shells.
  COMPRESSION / CONCENTRATION: Z25-b concentration, Z26 information accounting
    (20x gap, no generation) confirmed; attractors = 210 of |Q|=136433 (Z28);
    H(mu)=7.46 bits (Z28) vs quotient 17.03 bits.
  GENERATIVE-vs-REVEALING: Z32 resolved geometry-only off the table (uniform
    quotient vs static-comparison); Z33 resolves the causal direction *within*
    the dynamics: productivity concentrates in a short transient of occasional
    big |Aut| jumps tied to sparse-tie shells, against a zero-median background.

  CLOSED: privilege (moving seed set, canon neutrality, selector matrix),
    endpoint concentration, attractor-count -> quotient, information accounting,
    now a clean causal reading inside dynamics (Outcome B: transient jump process).
  OPEN (carry forward): (i) theorem that tie-collapse (Z26) forces zero post-
    cycle drift; (ii) why |Aut| jumps cluster at sparse-tie (R,A) shells rather
    than uniformly along the chain; (iii) whether Outcome B persists at other
    (N,M) cells once transients are long enough to populate the 30+ window.
