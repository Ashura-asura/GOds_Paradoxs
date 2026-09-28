# Phase Z23, Task C (delta) — Sage/Python cross-check of the LiE branching
# chains E8 -> D8 -> D5xA3 and E8 -> E7xA1 -> E6xU(1), with the E7-route
# "E6xSU(2)xSU(2)" disambiguation and the exact SU(4) "flavon" invariant ring

**Status: closed, L1. Every branching in RESULT_task_c_e8_branching.md is
now reproduced by a second, independent method: direct orthogonal
projection classification of the 240 E8 roots (exact Fraction arithmetic),
no branching-rule engine. Two new exact facts: (i) the chain
E8 > E7xSU(2) > E6xSU(2)xSU(2) does NOT exist as a chain of regular
subalgebras — C(E6 in E7) is a U(1) torus (0 roots), so the actual chain
is E8 > E7xSU(2) > E6xU(1)xSU(2); (ii) the SU(4) 'flavon' potential of the
SO(16)-route (the 4 of C(D5) = A3) has NO symmetry-breaking quartic: the
invariant ring of the SU(4) fundamental is C[|phi|^2] (the epsilon-quartic
is identically zero, verified term-by-term), so the 4-generation reading
cannot produce a non-cyclic 3-generation structure at the potential level
— reinforcing Task B's scoping conclusion that only the E6-route hosts
SU(3)_f.**

## What this phase tested

Task C's original result file computed the branchings via LiE 2.2.2
closures. The audit's Rule 9 requires independent verification; the
branchings are now recomputed from the root system alone, by the same
method as Task B: project each of the 240 E8 roots onto the subalgebra
planes, classify by (norm of the part, membership in the root set), and
count. This is a different algorithm from LiE's weight-restriction and
cannot share a systematic error.

## Method — projection classification (exact Fractions)

Same E8 machinery as Task B (verified Bourbaki simple roots, 240-root
closure, Gram-Schmidt, orthogonal projection). Each root r is written
r = r_S + r_T with r_S, r_T mutually orthogonal projections onto the two
planes of S x T; |r_S|^2 + |r_T|^2 = 2 asserted for every root. The pair
(|r_S|^2, |r_T|^2) and the membership of r_S, r_T in the root sets of S, T
determine the representation content.

## Result A — E8 -> D8 -> D5xA3 (Task C Result 3 cross-check)

D8 = {+-e_i +- e_j} (112 roots); D5 on coords 1..5, A3 on coords 6..8.
Projection classification of the 240 roots:

    (root, zero)  x 40   -> (45, 1)
    (zero, root)  x 12   -> (1, 15)
    (vec,  vec)   x 60   -> (10, 6)
    (spin, hspin) x 128  -> (16, 4bar) + (16bar, 4)
    total 240 + 8 Cartan = 248

matches RESULT_task_c_e8_branching.md Result 3 exactly: (45,1)+(1,15)+
(10,6)+(16,4bar)+(16bar,4). Independent method, identical numbers.

## Result B — E8 -> E7xA1 (Item 11 chain start cross-check)

E7 = <alpha1..alpha7> (126 roots, closed); A1 = C(E7 in E8) = {+-alpha8}
(2 roots). Projection classification by (|E7-part|^2, |A1-part|^2):

    (2, 0)     x 126 -> (133, 1)
    (3/2, 1/2) x 112 -> (56, 2)
    (0, 2)     x 2   -> (1, 3)

matches the LiE result 248 -> (133,1)+(56,2)+(1,3). Note the exact
values: the 56 weights of E7 have |part|^2 = 3/2 and the A1-weights 1/2
in the E8 metric — both verified as exact Fractions.

## Result C — E7 -> E6xU(1), and the "E6xSU(2)xSU(2)" label

E6 = <alpha1..alpha6> (72 roots). C(E6 in E7) = 0 roots: the centralizer
of E6 inside E7 is a rank-1 TORUS (the U(1)), not an A1. Therefore E7
does NOT contain E6 x SU(2) as a regular subalgebra, and the chain
"E8 -> E7xSU(2) -> E6xSU(2)xSU(2)" of audit Item 11 does not exist in
this form. The actual chain is E8 > E7xSU(2) > E6xU(1)xSU(2).

The E7 adjoint under E6xU(1), from the 126 roots:
    (2, 0)    x 72 -> 78 = 133|E6
    (4/3, 2/3) x 54 -> 27 + 27bar (the E6-27 weights have |part|^2 = 4/3
    in the E8 embedding — matching Task C's (27,3) roots with |A2-part|^2
    = 2/3, since 4/3 + 2/3 = 2)
    (0, 3/2)  -> 1 (the U(1) direction: no roots, 1 Cartan)

## Result D — E8 -> E6xU(1)xSU(2): full 248 classification (new)

All 240 roots classified by (|E6|^2, |U(1)|^2, |SU(2)|^2):

    (2, 0, 0)     x 72   -> (78,1,1)
    (0, 0, 2)     x 2    -> (1,1,3)
    (4/3, 2/3, 0) x 54   -> (27,1,1) + (27bar,1,1)
    (4/3, 1/6, 1/2) x 108 -> (27,2,1) + (27bar,2,1)
    (0, 3/2, 1/2) x 4    -> (1,2,2): the "1+1" content of E7's 56
                          under E6xU(1) (56 -> 27+27bar+1+1)
    total 240 roots + 8 Cartan = 248

So the Item 11 chain continues as
248 -> E7xSU(2) -> E6xU(1)xSU(2) with content (78,1,1)+(27,1,1)+
(27bar,1,1)+(1,1,3)+(27,2,1)+(27bar,2,1)+(1,2,2)+(1,2,2 non-root
entries in the Cartan). No E6xSU(2)xSU(2) at any step (Result C).

## Result E — SU(4) "flavon" invariant ring, exactly

The SO(16)-route's family factor is SU(4) = C(D5(1)) = A3, acting on the
(16,4bar): the "flavon" is the 4 of SU(4). Exact computation:

1. The holomorphic quartic candidate epsilon^{ijkl} phi_i phi_j phi_k
   phi_l was expanded: 24 terms, sum of signs = 0, identically zero
   (sympy verified: result 0). The epsilon-quartic/Pfaffian structure
   used in informal SO(16) discussions does NOT exist as a polynomial in
   a single field.
2. Tensor-singlet count: 4(x)4(x)4bar(x)4bar = (6+10) x (6bar+10bar) has
   2 singlets, but on one field phi^phi = 0 (antisymmetric square of a
   single vector) and sym(phi(x)phi) = phi.phi: both collapse to
   (phi^dag phi)^2.
3. Invariant ring of the SU(4) fundamental: C[|phi|^2] (SU(4) acts
   transitively on S^7, so the only polynomial invariants are powers of
   |phi|^2). The quartic "flavon" potential is therefore
   V4 = lambda (|phi|^2)^2 — a single term, no 3+1 split, no order-3
   structure.
4. Under SU(4) > SU(3)xU(1), 4 -> 3 + 1 is exact, but nothing in the
   SU(4)-invariant potential stabilizes or selects the split: 3
   generations from the SO(16)-route would require the explicit group
   reduction SU(4) -> SU(3)xU(1), leaving a spectator U(1) — i.e. a
   cyclic/abelian mechanism, not the non-cyclic SU(3)_f of Phase A2.

## Scoping conclusion (combined with Task B)

The SO(16)-route gives (16,4bar) with an SU(4) family group whose
fundamental has a trivial invariant ring: no potential can produce the
3-generation structure, and the only route to "3" is SU(4) -> SU(3)xU(1),
an abelian spectator. The E6-route's family group is SU(3) = A2 from the
start (maximal E8 > E6xSU(3)), with the S3 family-group structure and
the 27 -> 16+10+1 content (Task B Result 4): the non-cyclic 3-generation
mechanism is realized only there. Chain-selection remains undecided by
group theory (the algebra admits both chains), but the mechanism
"non-cyclic family group" is now pinned to the E6-route class.

## Rule 9 check

Falsifiable, no fitting: every count is an exact arithmetic classification
of the 240 roots with a per-root assertion |r_S|^2 + |r_T|^2 = 2; every
sum closes (126+112+2, 72+54, 240+8). The epsilon-quartic is provably
zero (24-term expansion). The invariant-ring statement follows from
transitivity of SU(4) on S^7 (standard, stated). No tables, no fitting.

## Net verdict

Closed, L1: Task C's LiE branchings independently reproduced (Results
A, B), the Item 11 chain corrected to E8 > E7xSU(2) > E6xU(1)xSU(2)
(Result C, D), and the SU(4) flavon question settled exactly: no
symmetry-breaking quartic exists in the fundamental of SU(4) (Result E).
Consistent with Task B: only the E6-route hosts the non-cyclic
3-generation mechanism.

## Reproducibility

`session_new_files/phase_z23_external_session/`:
- `tmp_task_c_sage_crosscheck.py` — the projection-classification
  computation (self-contained, exact Fractions + sympy)
- `task_c_sage_crosscheck_out.txt` — full log
- shared machinery with `tmp_task_b_so10_classes2.sage.py` (E8 base,
  closure, Gram-Schmidt, projection)

Tools: python3 (WSL Ubuntu) + sympy. Runs as plain python3 (no Sage/LiE
needed; LiE cross-check was the prior phase's method).

## Source

Computed here from the E8 root system (Rule 4). The transitivity of
SU(n) on the unit sphere and the standard maximal-subalgebra facts
(E7 > E6xU(1) maximal; E7 not containing E6xSU(2)) are textbook; the
root-level verification (C(E6 in E7) = 0 roots) is this computation's
output.
