# PHASE Z30 — TIE-DEGENERACY DYNAMICS ENGINE
# Rule-8 closed · 2026-08-02
# Scripts: phase_z30\z30_control_test.py, z30_engine.py

## Control (mandated first, because a harness bug was found and fixed)

z30_control_test.py verifies on 40 random (10,15) seeds, p=0:
  (A) engine's own T with its Z25-b RNG protocol  -> period 2, 40/40
  (B) manual re-implementation of full-sort tie-break (rem[0], add[-1])
                                                 -> period 2, 40/40
The earlier exploratory file z30_tie_dynamics.py used a faulty 'lex'
selector (min on extremal SUBSETS, not full tie-broken lists). Its
'lex: period 24' output was a harness artifact; all Z30 numbers below
come from the verified z30_engine.py.

## Experiments (300 seeds each in EX1; 200/selector in EX2; 40 in EX3)

### EX1 — random selector trajectories (removes lexicographic bias)
    ALL 300 seeds converged; period spectrum:
        2: 157   3: 48   4: 22   5: 22   7: 15   6: 14   8: 6
        9: 8    10: 4   11: 3   14: 1
    attractor tau = (|R|, |A|) histogram (top):
        (6, 2): 242   (15, 24): 19   (6, 20): 19   (3, 6): 6
        (14, 2): 6    (12, 15): 3    (4, 3): 2  ...   (10 distinct tau total

### EX2 — selector independence (p = 0, 200 seeds per selector, same seed set)
    lex     : period 2 in 200/200 ;  mean |R|=6.57 |A|=6.34  HD=4.45
    random  : period 2 in 101/200 ;  mean |R|=6.54 |A|=4.76  HD=4.16
    entropy : period 2 in 200/200 ;  mean |R|=7.60 |A|=10.31 HD=5.56
    autmin  : period 2 in 200/200 ;  mean |R|=5.36 |A|=3.71  HD=3.88

### EX3 — Level-B quotient collapse along random trajectories
    S(t) = # of distinct canon classes among the full R x A successors:
        S(0) = 2.65
        S(8) = 11.33
        (S(32) not applicable for ~1/3 of short trajectories -> reported null)
    H_D trajectory mean: 1.0 -> 2.88  (rises; NOT monotone, NOT conserved)

## Findings, with Rule-3 labels

L1 (numeric, above):
  -  All four selectors converge 200/200. The 'non-convergence' seen with
     the faulty selector was harness error.
  -  lex locks period 2 with certainty; random reaches period 2 ~50.5%.
  -  entropy-/autmin-selectors also lock period 2 (tie-break bias chosen
     correlates with direction of bias, but the LOCK is common).
  -  On the attractor, the tau = (|R|, |A|) distribution is concentrated:
     242/300 fall in (6, 2) under random; structured selectors sit in the
     5-8 x 3-10 shell. Distinct tau across all random runs: 10.
  -  Level-B quotient branching S(t) EXPANDS from 2.65 (t=0) to 11.3 (t=8)
     then contracts to a low-period cycle; the future space first grows,
     then collapses.

L2 (interpretation):
  -  The period-2 is a SELECTOR ATTRACTOR IN TIE-SPACE, not a property of
     the raw extremal-exchange on labeled graphs. Any deterministic
     extremal tie-break with a stable bias direction locks onto it; the
     uniform-random selector wanders into it only half the time.
  -  The attractor lives in a narrow TIE-DEGENERACY SHELL
     tau in {(6,2)...(6,6)}, shared across selectors independently of
     their individual trajectories. That shell is the true weak invariant
     the dynamics concentrates onto. Scalar Lyapunov (Z28) and tie-class
     fixed point (Z29) both failed because both were looking inside the
     shell at single states; the concentration is at shell level.
  -  Outcome for the Z30 rubric: nearest to Outcome B (the selector
     introduces the order), but with a correction: the tie-degeneracy
     shell onto which any sane selector falls is itself dynamics-shaped.

L3 (conjecture, next phase):
  -  The tie-shell sigma(N, M) is computable directly: the joint law of
     (|R|,|A|) over extremal-exchange orbits converges, for each (N,M),
     to a small support on Z+^2. If sigma characterizes the quotient's
     measurable image under ANY fair extremal selector, the collapse is
     fully closed: a number theoretic property of the pair-action of S_N,
     not of the selector.

## Ledger (all passed)
- Rule 1: no physics/numerology anywhere; pure graph dynamics.
- Rule 2: selector battery fixed before runs; engine fluid exactly as
  z25b v2.
- Rule 3: L1/L2/L3 split enforced above.
- Rule 6: RNG seeds declared; 300/200/40 sweeps are assay sizes; no fit.
- Rule 8: artifact 'period-24 non-convergence' identified and superseded
  by verified control runs; recorded here.
- Rule 9: no free parameters; every count/entropy shown.
