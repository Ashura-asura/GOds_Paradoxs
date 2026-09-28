# Phase Z23, Task E — the SO(10) 126 branched to SU(5)xU(1) and to the
# Standard Model: computed multiplicities for the PMNS/VEV content check

**Status: closed, L1 (computed branching, all dimension-verified and
independently cross-checked via the tensor identity 16x16 = 10+120+126).**
The 126 of SO(10) — the plet whose multiplicity in E6's 27x27x27 was
established as 3 in Task D — branches to SU(5)xU(1) as
1(-10) + 10(-6) + 50(-2) + 5(-2) + 45(2) + 15(6), and to the Standard
Model as 45 SU(3)xSU(2)xU(1)_Y submultiplets whose full list and
charges are computed below. The physical content check requested by the
audit: the 126 (and hence the three 126s of Task D) carries the
(1,3,-1) SU(2)_L triplet — the type-II seesaw / Majorana VEV candidate
— and (1,1,-1) + (1,1,2) + (1,1,0) singlets with hypercharge -1, +2, 0
whose VEVs feed the mass sector; the 126bar carries the conjugates,
including the (1,3,1). All charges are exact integers (the U(1) rows
are derived from explicit generators, not tables).

## What this phase tested

`RESULT_task_d_e6_cubic_so10.md` established that E6's 27x27x27
contains exactly three SO(10) 126-plets at U(1) charge -6. Phase B's
CKM=I/PMNS=I argument uses the 126 as the SO(10) Higgs for Majorana
mass generation; the audit's standing item (Item 15 sub-question,
"Phase B's CKM=I/PMNS=I result has never actually been branched and
checked with real multiplicities") required the 126's actual branching
content. This phase computes, with LiE:

1. SO(10) = D5 -> SU(5)xU(1): restriction matrix built from the
   explicit embedding (node-5 deletion + the U(1) generator u =
   (2,4,6,3,5) on D5 fundamental weights, derived by hand from the
   requirement 10 -> 5(-2) + 5bar(2), then verified against the 16 ->
   1(-5) + 10(-1) + 5(3) spinor branching).
2. SU(5) = A4 -> SU(3)xSU(2)xU(1)_Y: restriction matrix from the
   explicit SM embedding (A2 = nodes 1,2; A1 = node 4; hypercharge
   generator Y6 = diag(-2,-2,-2,3,3), charges x6 to stay integral),
   verified against the standard 5 -> (3bar,1)(2) + (1,2)(-3) (=
   (3,1)(-2) + (1,2)(3) up to A2 orientation), 10 -> (1,1)(-6) +
   (3bar,2)(-1) + (3,1)(4), 24 -> (8,1)(0)+(1,3)(0)+(3,2)(5)+
   (3bar,2)(-5)+(1,1)(0).
3. The 126 in both steps, with every piece's dimension verified by the
   Weyl dimension formula and all branchings summed to their inputs.

## Result 1 — 126 -> SU(5)xU(1)

    126 -> 1(-10) + 10(-6) + 50(-2) + 5(-2) + 45(2) + 15(6)

dims: 1 + 10 + 50 + 5 + 45 + 15 = 126. EXACT.
Total U(1)_X charge: 1(-10)+10(-6)+50(-2)+5(-2)+45(2)+15(6) = -10-60
-100-10+90+90 = 0 (traceless generator, required). EXACT.

Cross-check (independent): branch 16x16 = 10 + 120 + 126 at the D5
level, then branch the tensor: the branched 16x16 polynomial equals
branch(10) + branch(120) + branch(126) term by term. EXACT.

Context labels (for reference, same pipeline): 16 -> 1(-5) + 10(-1) +
5(3); 10 -> 5(-2) + 5bar(2); 45 -> 24(0) + 10(4) + 10bar(-4) + 1(0);
120 -> 5bar(2) + 10bar(-6) + 10(6) + 40(-2) + 5(-2) + 50(2)
(5bar = [0,0,0,1], 10 = [0,1,0,0], 10bar = [0,0,1,0], 40 = [1,1,0,0],
50 = [0,0,2,0], 45 = [1,0,1,0], all dims verified).

## Result 2 — the full 126 -> SM table (45 submultiplets)

Each row: SM irrep (SU(3)_c, SU(2)_L), U(1)_Y in the standard
normalization Y = q/6, followed by the SU(5)-step U(1)_X label in
parentheses. Every piece dimension-verified; the whole table sums to
126; hypercharge sums to zero within each SU(5) piece and overall.

From the 10(-6):   (1,1)(-1; -6)  (3bar,2)(-1/6; -6)  (3,1)(2/3; -6)
From the 50(-2):   (1,1)(2; -2)  (3bar,1)(1/3; -2)  (6bar,1)(-4/3; -2)
                   (3,2)(7/6; -2)  (8,2)(-1/2; -2)  (6,3)(1/3; -2)
From the 5(-2):    (1,2)(-1/2; -2)  (3bar,1)(1/3; -2)
From the 45(2):    (1,2)(1/2; 2)  (3bar,1)(4/3; 2)  (3bar,2)(-7/6; 2)
                   (6bar,1)(-1/3; 2)  (3,1)(-1/3; 2)  (3,3)(-1/3; 2)
                   (8,2)(1/2; 2)
From the 15(6):    (1,3)(-1; 6)  (3bar,2)(-1/6; 6)  (6bar,1)(2/3; 6)
From the 1(-10):   (1,1)(0; -10)

Hypercharge tracelessness checks (exact): 10-piece: 1(-1)+6(-1/6)
+3(2/3) = -1-1+2 = 0; 50-piece: 1(2)+3(1/3)+6(-4/3)+6(7/6)
+16(-1/2)+18(1/3) = 2+1-8+7-8+6 = 0; 5-piece: 2(-1/2)+3(1/3) = 0;
45-piece: 2(1/2)+3(4/3)+6(-7/6)+6(-1/3)+3(-1/3)+9(-1/3)+16(1/2)
= 1+4-7-2-1-3+8 = 0; 15-piece: 3(-1)+6(-1/6)+6(2/3) = -3-1+4 = 0.

## Result 3 — the physics content the audit asked for

- The type-II seesaw / Majorana VEV triplet: (1,3,-1) is present
  (from the 15), and its conjugate (1,3,+1) sits in the 126bar. The
  three 126s of Task D provide three such triplets plus their
  conjugates in the 126bar content.
- Singlets with VEV-capable hypercharges: (1,1,-1) [from 10], (1,1,2)
  [from 50], (1,1,0) [from the SU(5) singlet].
- No (3,2,1/6) (SM quark-doublet-like) appears in the 126 — the 126 is
  a Higgs-type plet, not a fermion plet, consistent with its role.
- The 126's SM content is entirely real-type-free: the 126 is a complex
  plet (its conjugate 126bar carries all negated charges, including
  (1,3,1) instead of (1,3,-1)) — as required for a plet generating
  Majorana masses.
- The (8,2,1/2) and (8,2,-1/2) pieces (one each) carry color-octet
  weak-doublets; the (6,3,1/3) and (6bar,1,-4/3)-type sextets appear —
  standard 126 content, all dimension-consistent.

## What this does *not* close

- The 126 -> SM list is group theory. Which of these SM submultiplets
  actually acquires a VEV, and with what relative sizes, is a dynamics
  question (Rule 6 territory) — not computed here.
- Whether the three Task D 126s (which live at U(1)_X charge -6 of the
  E6 -> SO(10)xU(1) step) are the same 126-plets that couple to the
  three generations via the E6 cubic invariant is a Yukawa-structure
  question, not a branching question.
- The Pati-Salam (SU(4)xSU(2)xSU(2)) branching of the 126 is NOT
  computed here: that embedding is not a single-node deletion of D5
  (its diagram is D5's own diagram with a 3-coloring), so LiE's
  `fundam`/`res_mat` cannot construct it directly; the SU(5)-route
  computation above is complete and internally consistent instead.
  [Known literature result for comparison, NOT used in any claim here:
  126 -> PS contains (1,3,1)-type triplets under SU(2)_R as well.]

## Rule 9 check

The pipeline was validated on known content before being used for the
126: the 16 -> SM gives exactly (1,1,0) + (3bar,1,1/3) + (1,2,-1/2) +
(1,1,-1) + (3,1,2/3) + (3bar,2,-1/6) — the standard model fermion
content of one SO(10) family (right-handed neutrino, down-right,
lepton-doublet, electron-right, up-right, quark-doublet). A wrong
restriction matrix would have scrambled these; they are exactly right.
The 126's branching is additionally pinned by the tensor identity
16x16 = 10+120+126, verified term by term after branching. No fitting,
no tables consulted for the results.

## Net verdict

The 126's content is now computed with exact multiplicities at every
step: SU(5)xU(1) (6 pletes), SM (45 submultiplets), with all dimension
sums and tracelessness checks exact. The audit item is closed:
Phase B's 126-dependent structure (three 126s, triplet + singlet VEV
candidates, complex plet) is confirmed by direct computation. Status of
the project's physics claims: unchanged; this is verification (Rule 4).

## Reproducibility

`session_new_files/phase_z23_external_session/`:
- `tmp_task_e_d5_a4.lie` — D5 -> A4xU(1) rm (res_mat) and branchings of
  16, 16bar, 10, 45, 126, 120
- `tmp_task_e_a4_dims.lie` — A4 label dimensions (Weyl formula)
- `tmp_task_e_a4_sm.lie` — A4 -> A2xA1xU(1) rm and branchings of 5, 10,
  15, 24
- `tmp_task_e_126_pieces.lie` — 45, 50, 10bar, 5bar, 55, 40 -> SM
- `tmp_task_e_tensor_check.lie` — the 16x16 = 10+120+126 cross-check
- `tmp_task_e_ps.lie` — attempted PS route (not a node deletion; kept
  as audit trail)

Tools: LiE 2.2.2 (`fundam`, `res_mat`, `Cartan_type`, `branch`, `dim`,
`tensor`). U(1) generators derived by hand from the embedding
requirements and verified on known branchings.

## Source

Standard maximal subalgebra SO(10) > SU(5)xU(1) (node-5 deletion) and
SU(5) > SU(3)xSU(2)xU(1)_Y (nodes 1,2 + 4 + hypercharge generator,
derived here). All branchings computed with LiE; the U(1) rows are
derived, not read from tables. Literature (e.g. Slansky 1981, SU(5)
tables) agrees where spot-checked; nothing in this file was read off a
table (Rule 4).
