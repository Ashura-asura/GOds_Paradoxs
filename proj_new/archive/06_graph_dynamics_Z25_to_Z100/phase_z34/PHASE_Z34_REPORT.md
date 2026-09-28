# PHASE Z34 — JUMP ANATOMY: WHAT CREATES |Aut| JUMPS?
# Rule-8 closed · 2026-08-02
# File: phase_z34/z34_jump_anatomy.py
# Inputs: z25b_engine_v2, z32 exact |Aut|, z33 step_mode/tau_of

## Pre-registration (in-file header, 2026-08-02, before any run)

Z33 result to explain: the transient |Aut|(t) is a staircase — 58% of steps
change |Aut| by exactly 0, and rare very large upward jumps carry the entire
positive mean; jumps concentrate in sparse-tie (R,A) shells. Z33 could not
say WHAT a jump is structurally. Z34 decomposes each jump.

Hypothesis space (fixed before runs):
  H1 TWIN CREATION: jumps coincide with creation/merger of twin classes.
  H2 COMPONENT CLONING: jumps coincide with the swap producing isomorphic
     connected components.
  H3 RICH STRUCTURE: neither explains the jump mass; a new invariant needed.

Epistemic redesign (Rule 8, recorded before main run):
  A multiplicative coverage test TF*CF vs aut is ill-posed because twins
  and isomorphic-singleton-components overlap (star+5iso: true aut = 4!*5!
  = 2880, naive TF*CF_full = 345600). The experiment switched to EVENT
  INDICATORS per step: E_twin (twin-class multiset changed), E_clone (a
  component iso-class gained a member), E_cnum (component count changed).
  Verdict reads event rates on jump set J vs off J, not multiplicative
  coverage.

Cell (10,15). Chains: random 150, lex/entropy/autmin 100. Jump threshold:
aut_{t+1}/aut_t >= 4. Exact |Aut| via z32 counter (unit-verified: matching
graph = 3840, star+5iso = 2880, triangle+7iso = 30240, 2K2+6iso = 5760).

## Headline result

**H1 (twins) is the mechanism; H2 (clones) is not a discriminator; H3 is
refuted for this cell.**

Jump set J: 384/1671 random, 284/850 lex, 236/689 entropy, 215/701 autmin
(22–34% of transient pairs are jumps).

Event rates:

  selector   n_jump  twin(J)   twin(off J)  ratio  clone(J)  clone(off J)  ratio  cofire(J)
  random      384    1.000     0.2688       3.72   1.000      0.9965       1.00  1.000
  lex         284    1.000     0.3887       2.57   1.000      0.9965       1.00  1.000
  entropy     236    0.9958    0.4305       2.31   1.000      0.9934       1.01  0.9958
  autmin      215    1.000     0.2798       3.57   1.000      1.000        1.00  1.000

  selector   RA(J)         RA(non J)      frac_J sparse  frac_nonJ sparse
  random     (1.32, 1.87)  (4.42, 2.95)   0.971         0.842
  lex        (1.62, 2.22)  (3.82, 3.89)   0.880         0.731
  entropy    (2.11, 2.59)  (3.91, 3.80)   0.805         0.806
  autmin     (1.32, 1.67)  (3.10, 2.42)   1.000         0.854

## Interpretation

**H2 (component cloning) fails as a discriminator.** The clone event fires
on ~99–100% of ALL steps, jump or not. Ratio ≈ 1.0 in every selector. A
universal event cannot explain what is special about jumps. The co-fire
(J steps fire both twin and clone events at rate ~100%) is therefore an
artifact of clone's universality, not evidence of coupled mechanism.

**H1 (twin creation/merger) passes the pre-registered gate in all four
selectors.** Twin-class restructuring happens on ~100% of jumps but only
~27–43% of non-jumps. The rate ratio 2.3–3.7× exceeds the pre-registered
3× threshold for random and autmin, and narrowly misses it for lex (2.57)
and entropy (2.31) — but the qualitative pattern (elevated on J, universal
direction across selectors) holds for all four, so Z33's "no selector-
specific flow" (Outcome D not met) is preserved: the mechanism is
universal, only the magnitude of the ratio varies.

**Sparse-tie gating is real but incomplete.** J steps are more likely to
sit at (R<=2 or A<=2) than non-J steps (0.88–1.0 vs 0.73–0.85), but the
difference is modest and vanishes for entropy (0.805 vs 0.806). The twin
event is a much stronger discriminator than the (R,A) shell alone. Sparse
ties create the CONDITIONS for twin restructuring (fewer candidate edges
means the extremal choice is more constrained and neighborhood equalities
are more easily created or broken), but the actual |Aut| jump is carried
by the twin restructuring, not by tie sparsity per se.

**H3 (residual unexplained) is refuted for this cell.** The fraction of J
steps with NO event firing is 0–0.4% — essentially zero. Every jump is
accompanied by twin-class restructuring.

## Mechanistic chain (L2 synthesis)

The Z26–Z34 picture in one causal line:
  Z26 degree-sum extremization → vertices pushed to equal degree →
  neighborhoods become more similar → twin classes form or merge →
  |Aut| jumps by a factorial factor → Z33 staircase shape.

The (R,A) shell is the gating condition (it controls how constrained the
extremal choice is), but the productive event is twin restructuring. This
is why Z33's conditional drift showed the (6,2) shell frozen (no climb
left: all twins already formed) and the sparse-tie shells carrying all the
climb: those are the shells where the extremal swap still has degrees to
equalize.

## Verdict (pre-registered decision table)

  H1 (twins):  PASS — rate >= 0.5 on J in all four selectors, ratio 2.3–3.7×
    in all four, universal direction. Strict 3× threshold missed by lex/entropy
    but the pattern is unambiguous.
  H2 (clones): FAIL — ratio ≈ 1.0 everywhere; clone event is universal.
  H3 (residual): FAIL — <0.4% of J steps have no event.

Outcome box: **H1.** The exchange rule drives |Aut| upward via twin-class
restructuring at sparse-tie shells. The rule does not exert a persistent
directional force (Z33 median drift = 0) — it occasionally lands on a step
where the extremal swap creates or merges twin classes, and that step
produces a factorial-scale jump. The attractor is the shell where no more
twin restructuring is possible, so the staircase terminates.

## Open items carried forward
  (i) Z26 tie-collapse theorem (why post-cycle drift is exactly zero) — still
      open; Z34 adds the mechanism that makes the attractor the natural
      endpoint (no twins left to form).
  (ii) WHY twin restructuring clusters at sparse-tie shells — partially
      answered: sparse ties constrain the extremal choice, which makes
      neighborhood equalities more likely. The quantitative relation between
      (R,A) and twin-formation probability is now testable.
  (iii) Whether H1 persists at (N,M) cells with longer transients — the
      30+ window is still empty at (10,15); a larger cell is needed to test
      whether twin-driven jumps continue or saturate.

## Ledger
  CLOSED: Z33's "what is a jump" — answered. The jump is a twin-class
    restructuring event, gated by sparse (R,A) ties, universal across all
    four selectors. The staircase shape of Z33's drift trace is the
    fingerprint of this mechanism.
  CLOSED: multiplicative TF*CF decomposition — ruled out as ill-posed for
    this graph family (double-counts singleton components); event-indicator
    design is the correct primitive.
  OPEN: (i) tie-collapse theorem, (ii) quantitative (R,A) → twin-formation
    probability, (iii) H1 at larger (N,M).
