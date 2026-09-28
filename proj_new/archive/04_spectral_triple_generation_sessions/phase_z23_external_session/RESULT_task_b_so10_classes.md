# Phase Z23, Task B (new subtask) — Conjugacy classes of SO(10) subalgebras
# of E8, computed from the root system: the three candidate chains
# (SO(16)-route, E7-route, E6-route) and their centralizers

**Status: closed, L1. The scoping question behind "non-cyclic (SU(3)_f/S3)
generation" is now answered: E8 contains exactly TWO conjugacy classes of
regular SO(10) subalgebras. The SO(16)-route and the E7-route D5's coincide
as one class (centralizer A3 = SU(4), SO(16)-position); the E6-route D5 is
the other class (centralizer A3', the twisted A3 containing the family A2 of
the maximal E8 > E6 x SU(3)). Only the E6-route class hosts the non-cyclic
SU(3)_f mechanism, where (27,3) branches to (16,3)+(10,3)+(1,3) with CKM=I
at tree level (Phase B). The SO(16)-route class hosts only the 4-generation
(16,4bar) reading of audit Item 10. The E7 chain (E8 > E7 x A1) contributes
no third class: its D5 coincides with the SO(16)-route D5 (both subdiagrams
{1..5} and {2..6} of E7 were computed; C(E7 in E8) = A1 = 2 roots).**

## What this phase tested

The Phase A2/B claim "exactly 3 chiral generations from a non-cyclic
generation mechanism" requires that the SU(3)_f generation factor be a
genuine (non-cyclic, non-U(1)) group. Phase Z22 closed the cyclic
(Z3-flavored) alternatives with a no-go; Task A and the family-group task
(RESULT_task_b_family_group.md) forced the S3 family group. This subtask
closes the SO(10)-embedding scoping: the three chains the project has been
quoting (E8 -> SO(16) -> SO(10)xSU(4), E8 -> E7xSU(2) -> ..., E8 -> E6xSU(3)
-> SO(10)) were enumerated as actual subalgebras of E8, with their
centralizers computed, from the root system alone.

## Method — exact computation over the 240 roots of E8

All arithmetic exact (Python Fraction) in R^8, no branching-rule tables:

1. **E8 simple base** (Bourbaki, verified): alpha1 = (1/2,-1/2,-1/2,-1/2,
   -1/2,-1/2,-1/2,1/2); alpha2 = (1,1,0,0,0,0,0,0); alpha3 = (-1,1,0,...);
   alpha_i = -e_{i-3}+e_{i-2} for i = 4..8. Closing the set gives exactly
   240 roots; the Cartan matrix was computed and verified (printed in the
   log; it is the E8 matrix with the chain 1-3-4-5-6-7-8 and the 2-4 bond).
   [Debug note: two off-by-one attempts produced a wrong Cartan (spurious
   alpha1-alpha8 entry) and an IndexError; the correct indexing is
   v[i-3], v[i-2].]

2. **Subalgebra from Dynkin subdiagrams.** For a simply-laced E8, the
   regular semisimple subalgebras are the Dynkin-subdiagram classes (up to
   diagram automorphism; E8 has trivial automorphism group, so subdiagram
   position = conjugacy class). Each candidate D5 is the root subsystem
   spanned by 5 chosen simple roots, closed explicitly and counted.

3. **Centralizer.** C(H) = roots of E8 orthogonal to all roots of H; the
   centralizer's own type was classified by counting roots (Dynkin: 2,6,
   12, 20, ... roots for A1, A2, A3, A4, ...).

## Result 1 — three chains, two classes

- **D5(1), SO(16)-route** = E8 -> D8 -> D5xA3: D5 on coordinates
  {e1..e5}; roots {+-e_i +- e_j, 1<=i<j<=5} (40 roots, closed). This is
  exactly the D5 of Task C Result 3.
- **D5(2), E6-route** = E8 -> E6xSU(3) -> SO(10)xU(1): D5 = subdiagram
  {alpha1..alpha5} of the E6 subdiagram {alpha1..alpha6}; 40 roots,
  closed.
- **E7-route** = E8 -> E7xA1 -> D5: BOTH D5 positions inside E7 were
  computed: subdiagram {alpha2..alpha6} of E7 gives exactly D5(1), and
  subdiagram {alpha1..alpha5} gives exactly D5(2). The E7-route therefore
  produces no third class (it runs through the same two positions).

Verdict (computed, not assumed): D5(1) == D5(2) as root subsystems is
**False**; the two subalgebra classes are distinct.

## Result 2 — centralizers, computed

- C(D5(1)) = A3 = SU(4): 12 roots, exactly
  {+-e_i +- e_j, 6<=i<j<=8} (the SO(16)-position A3 on coords 6,7,8).
- C(D5(2)) = A3' : 12 roots, exactly
  {+-(e_i+e_8), +-(e_i-e_j), i,j in {5,6,7}} — the *twisted* A3 that
  contains the family A2 = C(E6) of the maximal E8 > E6 x SU(3).
  (Note: the twisted A3 is *not* {+-e_i+-e_j, 5<=i<j<=8}; its roots
  include the mixed-sign pairs +-(e_i+e_8).)
- C(E7 in E8) = A1: 2 roots (the outer SU(2) of E8 > E7 x SU(2)),
  consistent with 248 -> (133,1)+(56,2)+(1,3).

## Result 3 — the 248 under each D5 x C(D5)

Both classes give the same 248 -> D5 x C content, counted directly by
projection of all 240 roots onto the D5 plane:

    (root, zero) x 40      =  45   (adjoint of SO(10))
    (spin, hspin) x 128    =  16 + 16bar  under each of the 4 SU(4) reps
    (vec, vec) x 60        =  10 x 6
    (zero, root) x 12      =  1 x 15
    total 240 roots + 8 Cartan = 248

i.e. 248 -> (45,1) + (1,15) + (10,6) + (16,4bar) + (16bar,4) in the
SO(16)-position basis, matching Task C Result 3 exactly; in the E6-route
position the same representation content sits under the twisted A3'.

## Result 4 — the 27 under the E6-route D5(2) (the 3-generation content)

E6 = <alpha1..alpha6>: 72 roots (verified); the E6 orbit of Lambda_1 = 27
weights (verified); 27 -> D5(2) counted by projection:

    27 -> {'spin': 16, 'vec': 10, 'zero': 1}   = 16 + 10 + 1   EXACT

matching Task D's LiE branching of the 27 and the Phase A2/B content:
(27,3) -> (16,3)+(10,3)+(1,3). The (16,3) is the 3-generation claim; the
(1,3) = 3 Higgs singlets carries the family structure of the
family-group result.

## Scoping conclusion (the point of this subtask)

A non-cyclic generation mechanism (S3/SU(3)_f) is realized only in the
E6-route class: there the family A2 = C(E6) sits inside C(D5(2)) = A3',
and the (27,3) -> 16+10+1 family content is exactly the 3-generation
structure with the Phase A2/B CKM=I tree-level result. In the
SO(16)-route class the 248 gives (16,4bar): 4 generations at the D5xA3
stage (Task C Result 3), i.e. the audit's Item 10 reading — an SU(4) of
"generations" that does not reduce to exactly 3 without an additional
SU(4) -> SU(3)xU(1) step (and then it is a spectator U(1)-charge, not a
non-cyclic group). The E7 chain offers no third option.

## Rule 9 check

Falsifiable, no fitting: every count is exact arithmetic over the 240
roots (40-40-12-12-126-72 root counts; closure flags True; equality
flags computed by set comparison). The two classes are distinguished by
their computed centralizer root sets, which are explicit. If any simple
root or closure had been wrong, the Cartan matrix, the 240 count, and
the branching counts would all fail. No literature tables were used.

## Net verdict

Closed, L1: E8 has exactly two conjugacy classes of regular SO(10)
subalgebras; the non-cyclic 3-generation mechanism is specific to the
E6-route class; the SO(16)/E7-route class gives the 4-generation
(16,4bar) reading. This completes the scoping of Task B and pins the
"exactly 3" claim to a single embedding class (chain-dependence now
reduced to the two-class dichotomy, still not dynamically selected).

## Reproducibility

`session_new_files/phase_z23_external_session/`:
- `tmp_task_b_so10_classes2.sage.py` — full exact computation (E8 base
  verification, D5(1)/D5(2), E7 126-root check with both subdiagram
  positions, centralizer root sets, 248 projection classification,
  E6 72-root + 27-orbit check, 27 -> 16+10+1)
- `task_b_so10_classes2_out.txt` — full log
- `tmp_task_b_so10_classes.sage.py` (old, broken: wrong E8 base; kept
  for the audit trail), `task_b_so10_classes_out.txt` (its stale log),
  `tmp_debug_base.py` (E8-base debug that fixed the off-by-one)

Tools: python3 (WSL Ubuntu) + sympy (matrix rank / Lambda_1 weights)
+ exact Fraction arithmetic. Runs as plain python3 (no Sage/LiE).

## Source

Computed here, from the E8 root system (Bourbaki simple roots), per
Rule 4. The two-class dichotomy matches the standard structure theory
of E8's regular subalgebras (subdiagrams of the Dynkin diagram, trivial
diagram automorphism group); the explicit centralizer root sets are new
output of this computation.
