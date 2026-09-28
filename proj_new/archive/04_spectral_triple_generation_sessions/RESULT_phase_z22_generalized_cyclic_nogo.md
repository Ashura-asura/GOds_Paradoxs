# Phase Z22 — Gresnigt's non-tensor generation structure imported and
# tested; result is not an escape, it's a generalization of Z6-Z21's
# no-go to the entire class of order-3-cyclic generation mechanisms

**Status: closed, L1. Does not reduce the free-parameter count. Sharpens
what "generation is not a trivial spectator factor" (Z21's open item)
actually has to mean.**

## What this phase tested

Z21 closed self-twists `Ad(f(D))` specifically because this project's
`H_F = C^32 (x) C^3` (Phase Z2 onward) treats generation as a **trivial
tensor factor**: the SM gauge algebra and every self-twist tested act
as `a -> a (x) I_3`, leaving the full `Mat_3(C)` as commutant, and by
Schur's Lemma any conjugation-invariant generation-space operator is
forced proportional to `I_3`. Z21 flagged, honestly, that this argument
does *not* cover a construction in which "generation and Cl(10) are not
separately factored" — and named that the untried direction.

An external paper (N. Gresnigt, arXiv:2604.24795, found via this
session's literature check, building on arXiv:2601.07857 already in
this project's Phase U/Z record) constructs exactly such a structure:
three generation subspaces `S1, S2 = psi_3(S1), S3 = psi_3^2(S1)` living
as **non-orthogonal subspaces inside the same Cl(10) representation**,
related by an order-three algebra automorphism `psi_3`, not a tensor
factor. This phase imports that structure — independently rebuilt, not
trusted from the paper — and asks the project's own question: does a
generation structure of this kind escape the degeneracy Z6-Z21 found?

## Method — independent reproduction, not citation

Per Rule 4 (adversarial audit always on — applies to external literature
exactly as much as to this project's own phases):

1. Rebuilt Gresnigt's Cl(8) generators (his eq. 1) from scratch in this
   project's own numerical conventions. Verified the Witt-basis CAR
   relations `{a_i,a_j^dagger}=delta_ij` etc. (his eq. 3) hold exactly
   (machine precision), independent of his own Mathematica check.
2. Built the Cl(10) extension (his eq. 13-14) and the primitive
   idempotents (his eq. 4-7, 17-18); verified completeness and mutual
   orthogonality of the idempotents exactly.
3. Built `psi_3`'s action on the 8 Cl(8) generators from his explicit
   formula (eq. 9-11, all seven `g_i` transcribed and checked). Verified
   the images satisfy the *same* Clifford algebra as the originals
   (necessary condition for `psi_3` to be an automorphism) — exact to
   machine precision.
4. Since `Cl(8) = Mat(16,C)` is a simple algebra, every automorphism is
   inner (Skolem-Noether): solved for the intertwining unitary `U8`
   directly via the same SVD-nullspace method this project's own
   `solve_charge_conjugation()` already uses for `J`. **Caught and fixed
   a bug in this new code** (missing complex conjugate on the SVD
   nullspace vector — the existing `solve_charge_conjugation` code has
   it, this new code initially didn't) by checking the *direct* defining
   equation, not just trusting a small singular value. After the fix:
   `U8 @ E8[a] == psi3(E8[a]) @ U8` exactly (machine precision, all 8
   generators), `U8` exactly unitary, `U8^3` exactly proportional to
   `I_16` (confirms `psi_3^3 = Id`).
5. Built `S1` (first-generation states, his eq. 24-27) directly from the
   Witt generators, and `S2 = psi_3(S1)`, `S3 = psi_3^2(S1)` via
   conjugation by `U10 = I_2 (x) U8`.

## Result — the Gram matrix, confirmed and then generalized

**Linear independence:** confirmed, rank 3, for every state type tested
(u_L, nu_L, d_R, e_R^-).

**Gram matrix (Hilbert-Schmidt pairing) across generations, every state
type tested:**

```
[[1.    0.25  0.25]
 [0.25  1.    0.25]
 [0.25  0.25  1.  ]]
```

This independently confirms the paper's own stated result (their eq.
127: `<d_R,1, d_R,2> = 1/4 delta_ij`) from a from-scratch reproduction,
not a citation.

**The generalization (the actual point of this phase):** any real
matrix invariant under the *full* S3 permutation of three indices —
diagonal `a`, all six off-diagonal entries equal to the same `b` — has
eigenvalues `(a+2b, a-b, a-b)` **for all values of `a` and `b`**. This
is checked directly (symbolic, sympy) and is pure linear algebra, not a
property of Cl(10), Gresnigt's construction, or this project's algebra.

**Consequence:** the 2:1:1-type degenerate-pair pattern that Z6-Z21
found (via gauging SU(3)_f on a trivial tensor factor) and that
Gresnigt's paper independently found (via trace-pairing on genuinely
non-orthogonal Clifford subspaces, eigenvalues `3/4, 3/8, 3/8`) are
**not two independent confirmations of a Cl(10)xE8-specific fact.** They
are the same representation-theory fact appearing in two different
concrete realizations. Any mechanism that (a) generates three
generations by applying an order-three (or full S3) symmetry to a
single seed object, and (b) requires the physical coupling to respect
that same symmetry, is forced into this exact degeneracy pattern —
independent of whether the generation index is a trivial tensor factor
or a genuinely entangled non-orthogonal subspace.

## What this does *not* close

Honestly scoped, not overclaimed:
- This does not rule out generation structures built from an order-3
  symmetry where the *coupling itself is not required to be symmetric*
  under the full residual S3/psi_3 action — i.e., using the un-averaged,
  family-resolved directions (Gresnigt's own `H_alpha`, `H_beta`, the
  orthogonal-to-the-cyclic-average directions he explicitly set aside as
  future work) rather than the symmetric average. Those directions were
  not tested in this phase.
- This does not rule out generation structures that are *not* generated
  by any order-3/S3 automorphism of a single seed at all — a genuinely
  different construction principle, not merely a different realization
  of the same one. No candidate for this has been proposed or tested
  anywhere in this project (A1-Z22).
- The linear-algebra generalization above is a *necessary* condition
  (any S3-symmetric coupling is degenerate this way) — it is not a
  proof that breaking S3-symmetry is *sufficient* to fix the hierarchy;
  it only identifies where the remaining freedom must live.

## Rule 9 check

Non-numerological and falsifiable: the eigenvalue formula `(a+2b,a-b,a-b)`
was derived symbolically, not fit to either result. If Gresnigt's actual
Gram matrix had NOT been of the diag-a/uniform-off-diag-b form (e.g. if
`S3` were embedded asymmetrically relative to `S1,S2`), the degenerate-
pair prediction would not have held, and this phase would have reported
that. It didn't — the S3-invariance of `psi_3`'s construction forces the
Gram matrix into exactly this form by the same symmetry argument that
forces `Q` and other `psi_3`-averaged generators to be well-defined in
Gresnigt's own paper.

## Net verdict

**Status remains 0/19.** This closes the "does a non-tensor generation
structure escape Z21" question negatively, but replaces it with a
sharper and more general statement of the real obstruction: symmetry
under the mechanism that produces three generations, imposed on the
coupling, is *itself* sufficient to force a 2:1:1-type mass degeneracy,
regardless of implementation detail. What remains untested (not merely
unimplemented but genuinely never attempted, A1-Z22): a construction
where either (a) the coupling deliberately does not respect the full
symmetry used to generate the copies, or (b) the three generations are
not related by any single order-3/S3 automorphism of one seed at all.

## Reproducibility

`phase_z22_gresnigt_import/`:
- `gresnigt_algebra.py` — Cl(8) generators, Witt/CAR checks
- `gresnigt_generations.py` — Cl(10) extension, idempotents, psi_3 on
  generators
- `gresnigt_step3.py` — psi_3 solved as inner automorphism (Skolem-
  Noether), verified exact
- `gresnigt_step4_gram.py` — S1/S2/S3 construction and Gram matrix

Pure numpy + one sympy symbolic check for the generalization. No SM
value inserted anywhere. Runs clean, exact to machine precision except
where noted.

## Source

N. Gresnigt, "Higgs and Yukawa Structure in a Clifford Algebra Model
with Three Generations and S3 Family Symmetry," arXiv:2604.24795
(2026), building on arXiv:2601.07857. Independently reproduced and
extended here, not cited without verification (Rule 4).
