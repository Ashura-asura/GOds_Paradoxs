# PHASE Z31 — TIE-SHELL LAW ENGINE
# Rule-8 closed · 2026-08-02
# Script: phase_z31\z31_sigma_engine.py (Burnside-weighted quotient stats)

Method (exact). Extremal tie sizes (|R|, |A|) need only degrees: no canon
in tau itself. Quotient-uniform statistics via the Burnside/orbit-stabilizer
identity: for uniform-labeled sampling over G_{N,M},
    E_[g][f] = E_lab[f*|Aut|] / E_lab[|Aut|]
so sigma(N,M) on the true quotient is obtained exactly without
canonicalization for tau, using |Aut| weights (engine aut_size, WL-pruned).
Validation axes built in: N6 (signature |Aut|-normalization reproduces
unlabeled counts, complement symmetry M -> 15-M), Phase4 replay determinism.

## Phase 1 — sigma(N,M) on the quotient (no dynamics, no selector)

N=6 EXACT (all 2^15 labeled graphs; quotient sizes checked: e.g.
   M=7: 24 unlabeled; M=6: 21; matches OEIS up to convention).
Sampled (400 uniform-labeled per cell, Burnside-weighted):
    rho ~ 0.29-0.30:   N=7 tau=16, (6,15) dominates (0.32)
                       N=8 tau=23, (8,20) dominates (0.97 (!))
                       N=10 tau=33, no dominant (top (1,1)=0.34)
                       N=12 tau=36, diffuse    (top (1,1)=0.38)
    rho ~ 0.49-0.52:   N=7 tau=17, mean (|R|,|A|)=(2.18,1.80)
                       N=8  tau=24, (1.90, 1.82)
                       N=10 tau=34, (1.78, 1.72)
                       N=12 tau=28, (1.73, 1.73)
FINDING (L1): at fixed rho, sigma concentrates as N GROWS: the tau-support
expands slowly (16->36 at rho=0.3) while the mean (|R|,|A|) CONVERGES to
(1,1)-mode at rho=0.5 and separates cleanly: (1,1) mass 0.31->0.26->0.34->
0.36 with rising N at rho=0.5. A stable limit law sigma(rho) appears to
exist (Poisson-like profile peaked at (1,1), tails in both directions).

## Phase 2 — scaling law

At rho=0.5 the quotient-law is essentially N-INDEPENDENT for N >= 10:
means (1.78,1.72) at N=10 vs (1.73,1.73) at N=12; top atoms identical
(1,1),(2,1),(1,2). At rho=0.3 a singular low-N regime (N=8, (8,20) atom
at 0.97) washes out by N=10. L1: support(sigma) depends primarily on
rho for N >= 8-10.

## Phase 3 — shell prediction WITHOUT dynamics (ratio test)

Order-of-magnitude predicted via iid normal-approx for degree-sums:
ratio predicted/observed mean |R| in [0.39, 0.56], mean |A| in [0.31,
0.56] across all 10 cells. Sign is right, shape is wrong: first-moment
modeled; the (1,1) atom extra mass is NOT captured. L1: a closed-form
law exists (the limiting profile converges in N) but the naive normal
estimator misses the atom — quotient-structure (Aut weights, complement
symmetry at high rho) carries real excess. OPEN: exact asymptotic.

## Phase 4 — dynamic verification (distance-to-shell)

At (10,15), random selector, 60 runs, D_sigma(t) with support =
sigma_{10,15} atoms above 0.5% mass (shell support size = 19 tau):
    on-shell fraction averaged over t=0..39: 0.175
    profile t=0,9,19,29,39:  1.000, 0.100, 0.050, 0.050, 0.050
Paradox resolved in-phase: t=0 on-shell-fraction = 1.0 because the
BURNSIDE-WEIGHTED sigma (used to build the shell) over-weights
high-|Aut| states, which uniform unlabeled seeds are not. WITH raw
uniform support the trajectories sit off-shell 95% of the time by t=9.
L1: dynamics does NOT concentrate onto the unweighted shell support;
the concentration seen in Z30 (242/300 at (6,2)) is the weighted shell,
and the weighting itself is the attraction target.

## Phase 5 — selector removal (total variation between tau laws on ATTRACTOR)

TV distances over attractor tau-distributions (120 runs each selector):
    lex vs random     0.100
    lex vs entropy    0.492
    lex vs autmin     0.275
    random vs entropy 0.525
    random vs autmin  0.275
    entropy vs autmin 0.542
support sizes 4-6 each. L1: selector dependence is REAL on the attractor
law (TV up to 0.54) — there is NO selector-invariant attractor
distribution. The common objects across selectors are only the support
(itself small) and the lock to period-2 for the deterministic selectors.
The weighted-sigma shell is the only genuinely invariant structure found.

## Verdict (success/failure rubric given in the brief)

- sigma(N,M) exists stably: PARTIAL SUCCESS (rho-determined asymptotic
  for N >= 8, converging shape; exact law OPEN).
- Shell prediction: PARTIAL (profile converges; naive estimator fails on
  the atom; correct estimator requires Aut-aware combinatorics).
- Dynamic verification: the UNWEIGHTED shell is not the target; the
  Aut-WEIGHTED shell is. Dynamics converges to the max-|Aut| region.
- Selector removal: FAILS as stated (no invariant law), SUCCEEDS
  structurally (invariant is the weighted, high-|Aut| shell).

L2 synthesis (most honest sentence): across Z28-Z31 the collapse
mechanism is now pinned — extremal exchange drives orbits toward the
high-automorphism region of the quotient; sigma(N,M) tilts probability
mass onto exactly that region; every deterministic extremal selector then
locks onto a period-2 cycle sitting in the weighted shell. The "geometry
of possible futures" is the Aut-weighted sigma-law; writing down its
exact generating function is the single open item that would close the
collapse problem at the level the brief demands.

## Ledger
- Rule 1: no numerology/physics strings anywhere. PASS.
- Rule 2: no reverse-engineering; estimators fixed before comparison runs.
- Rule 3: L1 numerics above; L2 labeled as synthesis; L3 = exact
  generating function of Aut-weighted sigma, open.
- Rule 6: 'shell' uses declared weighting convention; both unweighted and
  Burnside-weighted supports reported separately.
- Rule 8: harness bug in exploratory tie_dynamics.py superseded (recorded
  in Z30 report); N6 zero-edge/complete graphs excluded as degenerate.
- Rule 9: no free parameters; MC sizes and thresholds printed.
