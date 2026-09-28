# Phase Z23, Task D — 27 x 27 x 27 of E6 branched to SO(10) x U(1):
# the 126 content is 3 copies at U(1) charge -6, and 126bar is absent
# (computed with LiE, per-summand and full, both from scratch)

**Status: closed, L1. The narrow sub-question Item 15 left open — does
the full 27x27x27 of E6 contain an SO(10) 126, and in what multiplicity
— is answered by direct branching-rule computation: 27x27x27 = 1 +
2925 + 2(78) + 3(650) + 2(5824) + 3003 (dims sum 19683 = 27^3), and
under E6 -> SO(10)xU(1) the full product contains exactly 3 copies of
the 126 (each at U(1) charge -6) and ZERO copies of the 126bar. The
126s come from the 5824 (x2) and 3003 (x1) summands. This confirms
Phase B's working assumption (a 126 capable of the PMNS mechanism
exists in the cubic product with multiplicity 3) and settles the
Item 15 dimension-formula caveat with real branching multiplicities.**

## What this phase tested

`RESULT_item15.md` closed the general tensor-product question (via the
Weyl dimension formula over all dominant weights at level <= 3) with
the finding that neither 126 nor 3875 is an achievable E6 irrep
dimension at all — but explicitly left open: "branching each 27x27x27
summand to SO(10) directly, which still needs LiE/Sage-class
branching-rule tooling this environment lacks." Task C installed and
verified that tooling (LiE 2.2.2, Sage 10.9). This phase performs the
branching the audit flagged as outstanding.

Two independent computations:

1. **E6 -> SO(10)xU(1) via LiE**: the maximal subalgebra with deletion
   of node 6 of E6 (LiE `fundam(id(6)-6)`), restriction matrix

       [[1,0,0,0,0,2],[0,0,0,0,1,3],[0,1,0,0,0,4],
        [0,0,1,0,0,6],[0,0,0,1,0,5],[0,0,0,0,0,4]]

   (columns: D5 simple roots = E6 nodes 1,3,4,5,6; last column: U(1)
   generator = -theta). Branched the 27, each 27x27x27 summand, and the
   full tensor product; every D5 label dimension was verified against
   LiE's own `dim()` (Weyl dimension formula), and every per-summand
   branch was checked to sum to its input dimension.

2. **Full-tensor check**: the polynomial branch of 27x27x27 directly
   (not summand by summand) matches the sum of the per-summand
   branches term for term.

## Result 1 — the E6 tensor decomposition (computed, not cited)

    27 x 27       = 27bar + 351 + 351bar
    27 x 27 x 27  = 1 + 2925 + 2(78) + 3(650) + 2(5824) + 3003

  dims: 1 + 2925 + 2(78) + 3(650) + 2(5824) + 3003
      = 1 + 2925 + 156 + 1950 + 11648 + 3003 = 19683 = 27^3. EXACT.

## Result 2 — the 27 and the 27bar under SO(10)xU(1)

    27   ->  1(-4) + 16bar(-1) + 10(2)
    27bar ->  1(4)  + 16(1)    + 10(-2)      [by conjugation]

  dims 1 + 16 + 10 = 27. EXACT. (The 16bar carries the SM family; the
  10 the Higgs; the 1 the right-handed neutrino.)

## Result 3 — the full 27x27x27 -> SO(10)xU(1) branching: 3 x 126, 0 x 126bar

The complete polynomial (25 terms, all multiplicity-1 except where
noted; U(1) charges in parentheses):

    1(-12) + 6(0) + 3x16bar(-9) + 6x16bar(3) + 3x126(-6)
    + 1x672(-3) + 8x16(-3) + 6x210(0) + 3x120(-6) + 1x120(6)
    + 2x1200(-3) + 9x45(0) + 3x560(3) + 1x560(-3) + 6x10(-6)
    + 3x10(6) + 9x144(-3) + 3x1050(0) + 6x144(3) + 3x945(0)
    + 2x320(6) + 6x54(0) + 3x720(3) + 1x210(6)

  Key content:

  - **3 copies of the SO(10) 126, all at U(1) charge -6; zero copies
    of the 126bar.**
  - Generation-count structure: 8 x 16 at charge -3, 6 x 16bar at
    charge +3 (plus 3 x 16bar at -9).
  - Higgs content: 6 x 10(-6) + 3 x 10(6) + 3 x 120(-6) + 1 x 120(6)
    + 2 x 1200(-3) + ... (the 126 itself is the SO(10) Higgs candidate).

  Verified two ways: per-summand branches (below) all sum to their
  input dimensions, and the direct full-tensor branch reproduces the
  same polynomial.

## Result 4 — per-summand branches (each verified: dims sum to input)

    78   -> 1(0) + 16bar(3) + 16(-3) + 45(0)          [1+16+16+45 = 78]
    650  -> 1(0) + 16bar(3) + 16(-3) + 210(0) + 45(0) + 10(6) + 10(-6)
            + 144(-3) + 144(3) + 54(0)                [1+16+16+210+45+10+10+144+144+54 = 650]
    2925 -> 16bar(3) + 16(-3) + 210(0) + 120(6) + 120(-6) + 2x45(0)
            + 560(3) + 560(-3) + 144(-3) + 144(3) + 945(0)
            [16+16+210+120+120+90+560+560+144+144+945 = 2925]
    5824 -> 16bar(-9) + 126(-6) + 16(-3) + 210(0) + 120(-6)
            + 1200(-3) + 45(0) + 560(3) + 10(-6) + 2x144(-3) + 1050(0)
            + 144(3) + 945(0) + 320(6) + 54(0) + 720(3)
            [16+126+16+210+120+1200+45+560+10+288+1050+144+945+320+54+720 = 5824]
    3003 -> 1(-12) + 16bar(-9) + 126(-6) + 672(-3) + 10(-6)
            + 144(-3) + 1050(0) + 54(0) + 720(3) + 210(6)
            [1+16+126+672+10+144+1050+54+720+210 = 3003]

  Multiplicity of the 126 across summands: 5824 contributes 1 x 126(-6)
  and appears twice (2x5824), 3003 contributes 1 x 126(-6): total
  3 x 126(-6). No summand contains a 126bar. The 351/351bar summands
  were branched as a cross-check (351 -> 16bar(-5) + 16(1) + 120(-2)
  + 45(4) + 10(-2) + 144(1), dims 16+16+120+45+10+144 = 351; 351bar ->
  1(-8) + 16bar(-5) + 126(-2) + 10(-2) + 144(1) + 54(4), dims
  1+16+126+10+144+54 = 351) — note the 351bar already contains a 126
  (at charge -2), which is why the cubic product's 126s also arise via
  the (1,351,351bar) path.

## Result 5 — SO(10) label dimensions (LiE `dim`, Weyl formula), all verified

    [0,0,0,0,0]=1  [0,0,0,1,0]=16  [1,0,0,0,0]=10  [0,0,1,0,0]=120
    [0,1,0,0,0]=45 [0,0,0,1,1]=210 [0,0,0,2,0]=126 [0,0,0,0,2]=126
    [1,0,0,1,0]=144 [1,0,0,0,1]=144 [2,0,0,0,0]=54 [0,0,0,0,3]=672
    [1,0,0,0,2]=1050 [1,0,1,0,0]=945 [1,1,0,0,0]=320 [0,1,0,0,1]=560
    [0,1,0,1,0]=560 [0,0,1,0,1]=1200 [2,0,0,0,1]=720 [3,0,0,0,0]=210

  (Labels in E6->D5 ordering: node 6 deleted, D5 nodes in the order
   used by the restriction matrix above.)

## What this does *not* close

- The 126 multiplicity (3) is the *number of SO(10) 126-plets in the
  E6 cubic*, not a statement about which of them are light/massive or
  how they couple; the E6 cubic invariant itself lives in the 1 of
  (27,27,27) and its SO(10)xU(1) image is the trivial term, so the
  tree-level Yukawa structure remains determined by the E6 cubic
  invariant alone (the 27^3 -> 1 projection), not by the 126s.
- Whether an SO(10) breaking VEV in a 126 can realize the PMNS
  mechanism (the phase-B motivation) requires the 126 -> SM branching,
  not computed here.
- The chain dependence noted in Task C: the same E6 cubic branched
  under a different SO(10) embedding (e.g. D5 x U(1) with a different
  U(1) normalization) changes the charge assignments but not the
  126-vs-126bar counts; the multiplicities 3 and 0 are embedding-
  dependent in detail and were computed for the standard maximal
  subalgebra only.

## Rule 9 check

No fitting, falsifiable: every branch is a formal polynomial computed
by LiE's branching engine from an explicitly constructed restriction
matrix; every label dimension checked with the independent Weyl
dimension formula; every per-summand branch summed to its input
dimension; the full-tensor branch cross-checked against the sum of
per-summand branches. The key claims (3 x 126 at charge -6, 0 x 126bar)
are exact statements about the computed polynomials, not numerics.

## Net verdict

Item 15's outstanding sub-question is closed: the E6 cubic contains
exactly 3 SO(10) 126s (charge -6) and no 126bar. Phase B's assumption
that a 126 appears in the cubic product is confirmed with computed
multiplicities; the caveat that 126/3875 are not E6 irrep dimensions is
also consistent (the 126s arise from the SO(10) branching of E6
irreps, as they must). Status of the project's overall claims:
unchanged; this is verification of cited structure, per Rule 4.

## Reproducibility

`session_new_files/phase_z23_external_session/`:
- `tmp_e6_27x3.lie` — 27x27, 27x27x27 decompositions (E6 tensor
  products)
- `tmp_e6_so10_branch.lie` — E6 -> SO(10)xU(1) restriction matrix and
  27 branching
- `tmp_e6_so10_taskd.lie` — per-summand branchings (2925, 78, 650,
  5824, 3003)
- `tmp_e6_351_branch.lie`, `tmp_e6_351bar.lie` — 351 and 351bar
  branches
- `tmp_e6_27x3_so10.lie` — full 27x27x27 -> SO(10)xU(1) polynomial
  (25 terms)
- `tmp_so10_dims.lie`, `tmp_so10_dims2.lie` — SO(10) label dimension
  tables

Tools: LiE 2.2.2 (`fundam`, `res_mat`, `Cartan_type`, `branch`,
`dim`). No third-party branching package.

## Source

Standard maximal E6 > SO(10)xU(1) subalgebra (node-6 deletion); all
branchings computed here with LiE, not read from tables. Literature
(Slansky 1981, E6 tables) agrees where spot-checked; every number in
this file is independently computed (Rule 4).
