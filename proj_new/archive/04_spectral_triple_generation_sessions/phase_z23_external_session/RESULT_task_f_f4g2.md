# RESULT: Task F — E8 -> F4xG2 (audit B6 "E8 -> F4xG2, F4 has 26, G2 has 7, 26+? =3?")

Status: CLOSED (L1 arithmetic given L2 embedding existence; guess N/A confirmed dead)
Ground rules: Rule 3 (L1/L2 labels), Rule 6 (no free parameters), Rule 9 (discriminating power check below)
Date: 2026-08-02 (Phase Z23 external session, continuation after Task E)

## 1. Question
The B6 audit record states: "[REASONED] E8 -> F4xG2 ... F4 has 26, G2 has 7, 26+? =3? ... hedged as 'maybe' ... N/A — not a stated hypothesis, a guess".
Task: determine the actual E8 -> F4xG2 content of the 248 and test the two parts of the guess:
  (a) "26 = 16 + 10"
  (b) "7 = 3 + 3 + 1"

## 2. The embedding and the forced decomposition
F4 x G2 is a maximal NON-REGULAR subalgebra of E8, rank 6 (Dynkin's classification of maximal
subalgebras of exceptional groups; existence = L2 citation). LiE cannot construct non-regular
embeddings (no single-node deletion exists: E8's diagram has no F4xG2 sub-diagram), so all
arithmetic below is done directly on the root/weight structure.

Given the embedding, the 248 decomposition is FORCED by pure counting (L1):

  (i)   Adjoint pieces: the F4xG2 roots inside the 240 E8 roots are the 48 F4 roots + 12 G2
        roots = 60 roots -> (52,1) = 48 roots + 4 zeros, (1,14) = 12 roots + 2 zeros. 4+2 = 6
        of the 8 Cartan elements used; 248 = 52 + 14 + 182.

  (ii)  The complement (dim 182) must contain exactly 180 non-zero weights (the remaining 180
        E8 roots, each with multiplicity 1, none of them roots of F4xG2) plus 2 zero weights
        (the 2 remaining Cartan elements). This pins the irrep uniquely:
          - F4-factor must have exactly 24 non-zero weights + 2 zeros  ->  the 26 (only F4
            irrep in this size range with 2 zeros; 52 has 4, 273 has 6, 324 has 8).
          - G2-factor must have 6 non-zero + 1 zero  ->  the 7.
        Count: (26,7) gives 24*6 + 24*1 + 2*6 = 180 non-zero weights + 2*1 = 2 zeros.  EXACT.

  (iii) Other candidates ruled out:
          - (1,182): the 180 complement roots have NON-ZERO F4-projection (they are not in the
            G2 subspace); a (1,182) piece has only zero F4-weights -> impossible.
          - (26,14): 24*12 + 24*2 + 2*12 = 360 non-zero weights, not 180.
        Verified numerically (tmp_task_f_firstprinciples.py).

  =>  E8 -> F4xG2:  248 = (52,1) + (1,14) + (26,7)        [52 + 14 + 182 = 248]

## 3. Part (a) of the guess: "26 = 16 + 10"  ->  DEAD
  (i)  Rank argument (airtight): SO(10) has rank 5 > rank 4 = rank(F4), so SO(10) is NOT a
       subgroup of F4; the 26 of F4 cannot restrict to the SO(10) content 16+10.
  (ii) The actual maximal SO(9) subgroup of F4 (rank 4): the B4 roots {+-(e_i +- e_j), i<j}
       (24 long) and {+-e_i} (8 short) form a B4 subsystem inside the 48 F4 roots (verified:
       Cartan long/short counts 24/8). Restricting the 26 (24 short roots + 2 zeros):
         8 short roots +-e_i        ->  weights of the 9 (vector)
         16 half-integer roots      ->  the 16 spinor weights of B4
         2 zeros                    ->  the 1
       =>  26 -> 9 + 16 + 1   (not 16+10).  Also 52 -> 36 + 16 (adjoint + spinor).
  (iii) The "16+10" pattern belongs to the E6 -> SO(10)xU(1) story (27 -> 16bar + 10 + 1,
        Task D), not to F4: the guess appears to conflate the F4-26 with the E6-27.

## 4. Part (b) of the guess: "7 = 3 + 3 + 1"  ->  TRUE (corrected: 3 + 3bar + 1)
G2 root system realized in R^3: 6 short roots +-(e_i - e_j)-perpendicular forms and 6 long
roots +-(2e_i - e_j - e_k) perms. The A2 = long-root subsystem (simple roots (2,-1,-1),
(-1,2,-1); Cartan [[2,-1],[-1,2]] verified by inner products). Restricting the 7 (6 short
roots + 1 zero) via exact Dynkin coordinates <w, beta^v> (Fraction arithmetic):
   3 short roots -> weights of A2 3,  3 short roots -> weights of A2 3bar,  0 -> 1.
   =>  7 -> 3 + 3bar + 1   (the audit's "3+3+1" is correct up to the conjugate).
Also computed: 14 -> 8 + 3 + 3bar (adjoint of G2; the 6 long roots + 2 zeros -> 8).
Note: the pair 3 + 3bar is complex-conjugate (vector-like under A2), NOT three copies of a
chiral 3; consistent with Task E's finding that all SU(3) content of the 126 comes in
(3,3bar)-type pairs. The "3" here carries no family-group information.

## 5. Rule 9 — discriminating power
  Tested claim: B6's guess (26=16+10, 7=3+3+1 => generation structure).
  The computation discriminates:
    - the forced 248 = (52,1)+(1,14)+(26,7) vs any other F4xG2 irrep combination
      (weight-counting rules out (1,182), (26,14), etc.);
    - 7 -> 3+3bar+1 (computed exactly) vs the audit's 3+3+1 (conjugate correction);
    - 26 -> 9+16+1 under F4 superset SO(9) vs the claimed 16+10 (impossible by rank 5 > 4).
  No fitting, no free parameters (Rule 6); one provable step at a time (Rule 7).

## 6. Verdict
  The E8 -> F4xG2 chain is real (Dynkin) and 248 = (52,1)+(1,14)+(26,7) is forced, but B6's
  guess is confirmed N/A as suspected: (a) "26 = 16+10" is structurally impossible (rank) and
  the actual content is 9+16+1; (b) the surviving "7 = 3+3bar+1" yields only a conjugate
  (vector-like) pair under G2 -> A2 with no net chiral family structure. No new physics;
  nothing added to the 3-generation picture beyond Tasks C/D/E.
  Structural failure of the guess = the result (Rule 8), documented.

## Files
  - tmp_task_f_firstprinciples.py  (exact-Fraction Python; all checks passed)
  - tmp_task_f.lie                 (G2/F4 dimension tables; G2->A2 manual-rm attempt —
                                    LiE cannot build the A2 rm because the A2 coroot is not
                                    an integral G2 weight; superseded by the Python route)
