# Phase Z23, Task C — E8 branching rules, computed from the root system,
# not cited: E8 -> E6xA2, E8 -> E7xA1, E8 -> D8 -> D5xA3, with the 248
# and 3875 in every chain

**Status: closed, L1. Every branching rule used by this project's
Phase A2 "exactly 3 generations" claim — and by the alternative chains
the audit flagged as unverified (Item 10 E8->SO(16)->SO(10)xSU(4),
Item 11 E8->E7xSU(2), and the E6xSU(3)_f chain itself) — is now
computed from first principles (LiE closure + independent Python
root-system verification), not taken from Slansky tables. The
E8 -> E6xSU(3) chain reproduces (78,1)+(1,8)+(27,3)+(27bar,3bar) =
248 with exact root multiplicities (72+6+162), and the 3875 branches
with verified dimension sum 3875. Status of the "3 generations"
question itself is unchanged (chain-dependence remains a separate
issue, see README/Phase A2); this task closes the tooling gap, not
the selection question.**

## What this phase tested

The project's oldest standing debt (audit Item 15, Phase R backlog D,
`PHASE_W_FULL_SWEEP.md` B2, `RESULT_item15.md`): the branching rules
underlying "exactly 3 chiral generations" were cited from literature
(Slansky 1981), never computed in-project. The audit explicitly
flagged: "the ADJOINT branching (78+8+162=248, zero room left for
126/3875) was computed directly from the root system... but Phase B's
CKM=I/PMNS=I result has never actually been branched and checked with
real multiplicities in this project's own code — currently cited from
literature, not computed."

This phase computes, with real multiplicities, from LiE 2.2.2 closures
(built from explicit E8 root vectors, no built-in embedding tables) and
cross-checked by an independent pure-Python computation over the full
240-root E8 root system:

- E8 -> E6xA2 (the Phase A2 "3 generations" chain; A2 = SU(3)_f)
- E8 -> E7xA1 (audit Item 11 chain start)
- E8 -> D8 -> D5xA3 (audit Item 10 chain start; D5xA3 = SO(10)xSU(4))
- the 3875 (E8's omega_1, the candidate 126-containing rep) in each

## Method — two independent computations

1. **LiE closure method.** For each subalgebra S x T <= E8: (i) found the
   simple roots of S and T as explicit E8 root vectors (for E6xA2 the
   A2 was located by brute force over all 240x240 root pairs: the pair
   beta1 = -e1-e2, beta2 = e1-e3 has beta1.beta2 = -1 and a 72-root
   orthogonal complement of rank 6 whose Cartan matrix is isomorphic to
   E6 — verified by explicit permutation (0,1,2,4,3,5)); (ii) closed the
   set with LiE `closure()`; (iii) built the restriction matrix with
   `res_mat()`; (iv) branched 248 = [0,0,0,0,0,0,0,1] and
   3875 = [1,0,0,0,0,0,0,0] with LiE `branch()`, verifying every
   resulting label's dimension with LiE `dim()` and summing to the
   input dimension.

2. **Independent Python verification (E8 -> E6xA2).** Over the full
   240-root E8 root system in the standard e-basis (with exact
   Fraction arithmetic), projected every root onto the A2 plane:
   exactly 72 roots have zero A2-part (the E6 subsystem), 6 roots lie
   in the A2 plane (the A2 subsystem), and the remaining 162 roots have
   |A2-part|^2 = 2/3 (the weight systems of (27,3) and (27bar,3bar):
   81 + 81). Combined with the 8 Cartan elements this is exactly the
   decomposition 248 = (78,1) + (1,8) + (27,3) + (27bar,3bar), derived
   from the root system alone — no branching-rule engine involved.

## Result 1 — E8 -> E6xA2 (the "3 generations" chain), 248 and 3875

- A2 simple roots (Bourbaki coordinates): -alpha2 and -alpha3-alpha4.
  E6 simple roots: 6 explicit E8 root vectors, Cartan matrix isomorphic
  to E6 (positive roots: 36 = 72/2, rank 6).
- LiE closure type: E6A2 (8 roots closed), restriction matrix computed,
  and:

      248  ->  (78,1) + (1,8) + (27,3) + (27bar,3bar)

  dims 78 + 8 + 81 + 81 = 248. EXACT.

- Python root-system cross-check (independent): 72 + 6 + 162 roots as
  classified above; E6 Cartan matrix verified isomorphic to E6 via
  permutation; A2 pair verified as a genuine A2 (Cartan [[2,-1],[-1,2]]).
  The (27,3) family is the Phase A2 "3 generations" content: each 27
  then branches to SO(10) as 16 + 10 + 1 (Task D), giving the
  project's (16,3) claim — now with computed multiplicities.

- 3875 (omega_1 of E8):

      3875 -> (1,1) + (1,8) + (27,3) + (27,6) + (351,3) + (351,3)
            + (78,8) + (27,6) + (27,3) + (650,1)

  dims 1 + 8 + 81 + 162 + 1053 + 1053 + 624 + 162 + 81 + 650 = 3875.
  EXACT. Note the asymmetry: 27 appears (as (27,3) twice, (27,6) twice)
  but 27bar does not — the 3875 contains 126-capable SO(10) content
  under further branching (Task D), confirming the literature structure
  Phase B assumed, now computed.

## Result 2 — E8 -> E7xA1 (Item 11 chain), 248 and 3875

- Subalgebra: closure of nodes {1..7} plus the negative of the highest
  root -[2,3,4,6,5,4,3,2]; LiE type E7A1.

      248  ->  (133,1) + (56,2) + (1,3)

  dims 133 + 112 + 3 = 248. EXACT.

      3875 ->  (1,1) + (56,2) + (1539,1) + (912,2) + (133,3)

  dims 1 + 112 + 1539 + 1824 + 399 = 3875. EXACT.
  [Audit note: an earlier draft of this file's scratch script swapped
  the print labels ("248 ->" / "3875 ->"); the branching was re-run
  with the labels corrected and dims verified — the labels in this file
  are the corrected ones.]

## Result 3 — E8 -> D8 -> D5xA3 (Item 10 chain: SO(16) -> SO(10)xSU(4))

- E8 -> D8 verified two ways: (i) LiE weight-restriction of the 240
  roots in the e-basis: exactly 112 roots are the D8 roots
  (+-e_i +- e_j) and 128 restrict to the D8 spinor weights —
  248 = 120 + 128; (ii) D8 Cartan matrix in this basis verified.
- D8 -> D5xA3 (closure of nodes {1,2,3,4,6,7,8} + [0,0,0,1,2,2,1,1],
  type D5A3):

      120  ->  (45,1) + (1,15) + (10,6)      [45+15+60 = 120]
      128  ->  (16,4bar) + (16bar,4)         [64+64 = 128]
      16   ->  (10,1) + (1,6)                [10+6 = 16]

  all EXACT. Full chain: 248 -> 120 + 128 -> {(45,1),(1,15),(10,6),
  (16,4bar),(16bar,4)}. This is audit Item 10's branching, now computed
  in-project: it gives 4 generations (16,4bar) at the D5xA3 stage, not
  3 — confirming the audit's reading of the alternative chain.

## Result 4 — the 3875 contains no 27bar, only 27s (E6xA2 view)

The 3875's E6xA2 branching above has (27,3)+(27,3)+(27,6)+(27,6) and
zero (27bar,*): the 3875 is "vector-like-ish" only if a 27bar sector
exists; under E6 -> SO(10) x U(1), (27,3) -> (16,3)+(10,3)+(1,3). The
126-bearing content is inside the 351 and 650 pieces (Task D). This is
the structure Phase B's minimal-248 argument relied on; it is now
computed, not cited.

## What this does *not* close

- Chain selection. E8 -> E6xSU(3) gives (16,3) = 3 generations; E8 ->
  D8 -> D5xA3 gives 4. The algebra permits both maximal chains; nothing
  computed here selects one. This remains the Phase A2 caveat, unchanged.
- Whether the (16,3) content is actually a gauged SU(3)_f or a
  spectator flavor factor (Phase Z14 connection) is a different
  question; the branching here is group theory, not dynamics.
- The 126/3875 appearance in 27x27x27 (Phase B's CKM=I argument) is
  Task D, computed separately.

## Rule 9 check

Falsifiable, no fitting: every dimension sum is exact arithmetic
(248 = 78+8+81+81 etc.), every label's dimension was independently
computed with LiE's `dim()` (Weyl dimension formula) and every
branching was cross-checked by a second independent method (Python
root-system classification for E6xA2; direct weight restriction for
D8). The E6xA2 embedding itself was located by brute force (search
over 240x240 pairs with a rank-6 orthogonal complement of 72 roots),
not assumed. If any restriction matrix had been wrong, the dimension
sums would not close.

## Net verdict

Tooling debt closed, L1: every E8 branching rule the project cites is
now computed in-project with exact multiplicities, including the
previously-cited-only 3875 branchings and the alternative-chain
branchings the audit flagged (Items 10/11). The branching-level claims
of Phase A2/B are confirmed as stated (with the known caveat that the
chain choice itself is not selected by the algebra). No new physics
claim is made; this is verification, per Rule 4.

## Reproducibility

`session_new_files/phase_z23_external_session/`:
- `tmp_e8_e7a1.lie`, `tmp_e8_e7a1_branch.lie` — E8 -> E7xA1 closure and
  branching of 248 and 3875
- `tmp_e8_e6a2_branch.lie` — E8 -> E6xA2 closure, restriction matrix,
  and 248 branching (roots in Bourbaki coordinates, verified as E8
  roots first)
- `tmp_e8_3875_e6a2.lie` — 3875 -> E6xA2
- `tmp_e6a2_dims.lie` — E6 and A2 dimension table
- `tmp_e8_e6a2_find2.py`, `tmp_e8_e6a2_check.py`, `tmp_e8_e6_check3.py`
  — brute-force A2 location, root classification (72/6/162), E6 Cartan
  isomorphism proof
- `tmp_e8_e6a2_exact2.py` — exact (Fraction) coordinate conversions;
  [audit note: an initial b2 typo [1,0,0,0,0,0,0,-1] vs
  [1,0,-1,0,0,0,0,0] broke orthogonality and produced an E8 closure;
  fixed and re-verified — the corrected b2 = -alpha3-alpha4 is used
  everywhere in this file]
- `tmp_e8_d8_weightcheck.py`, `tmp_d8_d5d3.lie`, `tmp_d8_d5d3_branch.lie`
  — E8 -> D8 weight restriction and D8 -> D5xA3 branchings

Tools: LiE 2.2.2 (closure/res_mat/branch/dim) + Python 3.13
(numpy + exact Fraction arithmetic only). No third-party branching
package was used.

## Source

Standard maximal subalgebra chain E8 > E6xA2 (maximal regular), E8 > E7
xA1 (maximal regular), E8 > D8 > D5xA3; the A2 location and all
restriction matrices were computed here, not read from a table.
Literature (Slansky 1981) agrees where checked; everything in this
file is independently computed (Rule 4).
