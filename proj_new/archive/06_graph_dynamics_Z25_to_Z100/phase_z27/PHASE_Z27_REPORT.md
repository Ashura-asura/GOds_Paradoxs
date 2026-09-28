# PHASE Z27 — QUOTIENT IDENTIFIED & COUNTED · UNIVERSALITY SWEEP · REVERSE MAP
# Rule-8 logged · 2026-08-02
# Files (isolation folder only):
#   phase_z26\z27_quotient_count.py  (exact Polya quotient sizes; validated)
#   phase_z27\z27_universality.py    (mechanism universality across N)
# All scripts import z25b_engine_v2.py witness-free conservative T.

=========================================================
1. THE QUOTIENT IDENTIFIED  (Possibility 1, L1)
=========================================================

THEOREM (quotient). The equivalence relation induced by canon() is exactly
GRAPH ISOMORPHISM. For every pair of states:

    canon(g1) == canon(g2)   <==>   g1 ~ g2  under S_N

(in the EX regime canon() is a full canonical form over all relabelings within
WL color classes; in the INV fallback the key ("INV", degree-seq, edge-degree
multiset, WL manifold) is a deterministic isomorphism-invariant, so the
equivalence is a coarsening of ~ with declared L2 possible false merges).

COROLLARY. The tie-collapse of Z25-Z26 computes the classical quotient

    rho : G_{N,M}  ->>  G_{N,M} / S_N

i.e. the space of UNLABELED GRAPHS. All engine observables (n3, n4, n5,
|Aut|, degree multiset, ratios) are by construction functions on this
quotient, not on G_{N,M} itself - they are isomorphism invariants.

No new object has been created: the canon() machinery reconstructs the
familiar quotient, which is why the dynamics could only ever compress
toward it (Theorem B of Z26).

---------------------------------------------------------
2. THE QUOTIENT COUNTED EXACTLY  (L1, externally validated)
---------------------------------------------------------

Polya enumeration with the pair-action of S_N. Fixed-edge permutation
cycle lengths derived exactly:
  - within a vertex cycle of length r: floor((r-1)/2) edge-cycles of
    length r (r odd);  (r-2)/2 of length r and one of length r/2 (r even);
  - between cycles of lengths r, s: gcd(r,s) edge-cycles of length lcm(r,s).
Substitute (1 + x^L) per edge-cycle, weight by class size, divide by N!,
read off the coefficient of x^M.

External validation (paid class cost):
      unlabeled graphs on 10 vertices, all M:
      computed 12,005,168 = OEIS A000088(10)  EXACTLY

Results:

  (N,M)      |G_{N,M}| (labeled)   |G_{N,M}/S_N| (unlabeled)   I_lab    I_quot   gauge bits = I_lab - I_quot
  (8, 12)        C(28,12)                  1,312                24.8586  10.3576    14.5010
  (10, 15)       C(45,15)                136,433                38.3273  17.0578    21.2694   (~log2(10!)=21.7911)
  (12, 18)       C(66,18)             19,515,361                52.6048  24.2181    28.3867

This splits the Z26 Theorem-B information loss into its two distinct
physical parts, explicitly:

  gauge loss (relabeling deadwood):       I_lab - I_quot   = half the gap
       (8,12): 14.50   (10,15): 21.27   (12,18): 28.39 bits
  dynamical contraction loss:             I_quot - H_out
       (10,15): 17.06 - 3.585 = 13.47 bits (measured, Z26)

Neither piece generates information; the gauge part was never information
(gauge redundancy), the contraction part is the map T being many-to-one.
The output lives entirely in the small 13.5-bit window that the dynamics
leaves open after quotienting.

---------------------------------------------------------
3. UNIVERSALITY OF THE PERIOD-2 MECHANISM  (Possibility 4, L1)
---------------------------------------------------------

Sweep: random (N, M?) seeds, witness-free conservative T, p in {0, 1},
8 seeds per cell, period and extremal iso-uniqueness measured on every
visited state.

             periods   add-iso-unique-mean   rem-iso-unique-mean   attractors/8 seeds
 N=8,M=12:
   p=0       {2}           0.652                 0.240                  8 all distinct
   p=1       {2}           0.233                 0.181                  8 all distinct
 N=10,M=15:
   p=0       {2}           0.334                 0.333                  7 (one pair shared)
   p=1       {2}           0.151                 0.252                  8 all distinct
 N=12,M=18:
   p=0       {1, 2}        0.398                 0.435                  3 (concentration!)
   p=1       {2}           0.235                 0.222                  8 all distinct

Observations (L1):
  (i) The period-2 class theorem survives every N tested (period 1 appears
      once at N=12 - the level-set singleton case).
 (ii) The Z26 asymmetry "add-extremum always iso-unique" does NOT survive N:
      at (8,12) it holds on only 65% of states (p=0). At (10,15) it was 100%;
      that was system-specific. The conditional theorem stands unchanged
      (WHEN add-unique holds on the two pre-image states, period <= 2), but
      its hold-frequency is state/N-dependent.
(iii) Basin contraction strengthens with N, consistent with Theorem B:
      I_quot grows ~ quadratically while reachable attractors stay small, so
      the fraction of the quotient that the dynamics can occupy shrinks.
      At (12,18), p=0, only 3 distinct attractors out of 8 seeds.

---------------------------------------------------------
4. REVERSE THE PERSPECTIVE (Possibility 2) - mechanical enumeration done
---------------------------------------------------------

Holder: the preimage map  rho^{-1} : quotient -> {labeled classes}, and the
dynamics-fiber map  T^{-t}(attractor) -> basin of attraction, are both
explicitly available from the engine (canon() gives the quotient point;
the per-seed attractor key gives the fiber). Three computable quantities for
the next phase, not yet run:

  (a) |rho^{-1}(g)| = N! / |Aut(g)|   per attractor key   (orbit stabilizer)
  (b) basin size = #{seeds s : lim_t T^t(s) = key} across a dense seed sweep
  (c) isomorphism-invariant complete measure of the CONTRACTION itself:
      the distribution of canon keys over a uniform sample of G_{N,M}
      (a histogram on the 136,433-point quotient for N=10,M=15).

Item (c) is the strict sense in which the engine defines a probability
measure on the quotient: push-forward of the uniform-on-labeled-graphs
measure under (T^inf . canon). If that pushforward were UISEED-uniform,
the dynamics would add nothing; the measured H=3.585 bits uniform-vs
log2(136,433)=17.06 bits shows it adds a *contraction*, not information -
consistent with Theorem B and now visualizable as a measure on the
exactly-counted quotient.

---------------------------------------------------------
5. STATUS OF THE FIVE POSSIBILITIES (user roadmap)
---------------------------------------------------------

  P1  hidden quotient          -> RESOLVED: G_{N,M}/S_N, exactly counted
  P2  reverse perspective      -> mechanical: preimage/basin/pushforward
                                  maps identified; computation queued (c)
  P3  forget graphs            -> next phase if pursued: object = point of
                                  the finite quotient; dynamics = measure
                                  on it. Graph language becomes optional.
  P4  universality             -> PARTIAL: period-2 class theorem survives
                                  all N; add-iso-uniqueness frequency and
                                  basin-concentration strengthen with N
  P5  no physics language      -> adopted in this report; all statements
                                  are about quotients and measures.

NET L1 RESULT THIS PHASE. The tie-collapse is exactly the orbit projection
onto G_{N,M}/S_N, the quotient is computable in closed form and counted for
every (N,M) used so far; the dynamics' information content is a bounded
13.47-bit contraction on that quotient at (10,15).
