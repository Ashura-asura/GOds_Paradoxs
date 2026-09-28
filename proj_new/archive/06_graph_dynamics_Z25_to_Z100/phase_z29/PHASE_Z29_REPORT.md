# PHASE Z29 — TIE-CLASS SUPPORT CHARACTERIZATION (REFUTED)
# Rule-8 closed · 2026-08-02
# Scripts: z29_tieclass_support.py, z29_selfreinforce.py
# Engine: phase_z25\z25b_engine_v2.py (witness-free conservative T)

## The conjecture under test

Z28 proved attractor collapse is NOT explained by any scalar Lyapunov
(no standard graph statistic is strictly one-sided on 1,152 steps).
Z29 tested the natural discrete replacement:

  CONJECTURE (tie-class invariance): an attractor of mu is exactly a state
  whose extremal tie-class — the iso-classes of argmin/argmax-degree-sum
  edges R(g) and nonedges A(g) — is invariant under one T-application,
  i.e. all (r, a) in R x A rewire into one canon class (up to 2-cycle
  alternation).

## Result: falsified at 0-1%

Over the full Z28 support sample (300 converged attractors per mode):

p = 0.0
    P1 (singleton extremal swap):     0 / 300
    P3 (all R x A swaps co-collapse): 0 / 300
    coverage  P1 v P3:                0.0000
    typical tie multiplicities:       |R| = 6, |A| = 2 (mode);
                                      worst next-class count = 360

p = 1.0
    P1:     3 / 300   ( = |R|=1 & |A|=1 cases )
    P3:     3 / 300   (the same 3)
    coverage:         0.0100
    typical:          |R| = 4, |A| = 6;  worst next-class count = 450

Attractor states are the MOST tie-degenerate states seen so far,
not the least (compare Z26 transient: add-side iso-unique held on 100% at
(10,15)). The tie-class does NOT stabilize at the attractor; if anything
it maximizes its degeneracy there.

## Residual test: self-reinforcement fraction

A looser form: maybe most extremal moves stay in the 2-cycle's two canon
classes even without a tie-class fixed point. Measured over 120 attractors
x both cycle states each (full R x A enumeration):

p = 0.0:  mean stay-fraction = 0.0656,  median = 0.0833,
          attractors reaching 50%: 0 / 120
p = 1.0:  mean stay-fraction = 0.0378,  median = 0.0417,
          attractors reaching 50%: 0 / 120

Aggregate: 240 of 8,217 extremal pairs stay in-cycle at p=0;
           240 of 12,801 at p=1.
           240 = 120 attractors x 2  EXACTLY  ->  the only staying move is
           the single (r, a) the railroad tie-break always picks. Every
           other extremal move (93-96%) escapes the attractor.

## What this proves (L1)

1. The 2-cycle is a MEASURE-ZERO POINT in tie-space. Its survival depends
   completely on the deterministic lexicographic tie-break of the engine;
   replace that projection by any other selector and the cycle dissolves.
2. Both natural mechanism explanations are now Rule-8 CLOSED:
       - Z28: scalar Lyapunov X_{t+1} < X_t                (refuted)
       - Z29a: tie-class discrete fixed point              (refuted, 0-1%)
       - Z29b: coarse basin self-reinforcement >= 50%      (refuted, ~4-7%)
3. The entire observed basin uniqueness is produced by canon() merging
   degenerate extremal choices after a symmetric-exchange step, under one
   fixed tie-break; it has no independent dynamical invariant.

## Status of the roadmap

Phases 1-2 (quotient measure, invariant hunt) are now closed with a
sharper verdict than expected: there IS no intrinsic invariant — the
collapse is a selection-rule artifact. The subsystem genuinely needing
new mathematics is therefore not move-invariance but the geometry of
'extremal-set degeneracy' under conservative exchange: e.g. the law of
|R|, |A| along orbits, which Z29 measured (mode |R| 3-6, |A| 2-24).

## Ledger
- Rule 1: no physics input. PASS.
- Rule 2: no reverse-engineering. PASS.
- Rule 3: L1 = all numerics above; L3 note = no L2/L3 interpretation was
  needed for the falsification; it is direct counting.
- Rule 6: tie-break selector is an assay convention, declared.
- Rule 8: two branches closed in one phase (tie-class, coarse stability).
- Rule 9: no free parameters; every count shown.
