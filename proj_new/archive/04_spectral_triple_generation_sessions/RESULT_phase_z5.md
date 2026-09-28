# Phase Z5 — why the Cl(10)-intrinsic route is closed, and what to build instead (this session)

## Question

`RESULT_phase_z4.md` left one open next step: Z4 showed `M10`
(Phase X's vector-**10** CG tensor) commutes with `Γ_F` instead of
anticommuting, so it fails the grading axiom `{Γ_F, D_F} = 0` and can't
legally be substituted into `D_F`. The stated next step was to build an
explicit, grading-respecting map from `M10`/`M120`/`M126` to a
chirality-*flipping* block of a graded `D_F`. This session asked: is
that map findable at all inside the current construction, or is there
a structural reason it can't exist?

## Method

All computation reuses objects already on disk — the same
`gamma_i.npy` files, the same `C_mat` (SVD nullspace of the
charge-conjugation condition from `vertex_terms_resolved/build_and_test.py`),
the same `V` (16-dim `Γ_F=+1` chiral embedding). No new conventions,
no new free parameters.

1. Found the true `Γ_F=-1` complement `Wc` directly from
   `eigh(Γ_F)` (not assumed — computed), and checked whether
   `C_mat @ G[a]` has any component connecting the two chirality
   blocks (`V†(C_mat G[a])Wc` and `Wc†(C_mat G[a])V`), versus the
   within-block component `V†(C_mat G[a])V` that Z4 used.
2. Checked what `C_mat` alone does to `Γ_F` (`[Γ_F,C_mat]` vs.
   `{Γ_F,C_mat}`), to find *why* any cross-block component vanishes.
3. Compared `C_mat` directly against the project's own two
   charge-conjugation candidates, `C_plus`/`C_minus`
   (`solve_charge_conjugation` in `support/cl10_gamma_J.py`), including
   a nullity check on the defining SVD to see if `C_mat` is one choice
   among several or the unique solution.
4. Repeated the cross-block check for `M120` (sampled 20 of 120
   index-triples) and `M126` (sampled 5 of 126 self-dual 5-forms), built
   exactly as in `vertex_terms_resolved/build_and_test.py`, to test
   whether the mechanism found for `M10` generalizes to the full
   `16⊗16 = 10⊕120⊕126` decomposition or was specific to the vector
   channel.

## Result

**1. The cross-block (chirality-flipping) component of `C_mat @ G[a]` is exactly zero:**

```
norm VV (within Γ_F=+1 block, used by Z4):      3.9999999999999973
norm VW (+1 <- -1):                              5.59e-15
norm WV (-1 <- +1, the candidate flipping block): 5.91e-15
norm WW (within Γ_F=-1 block):                    3.9999999999999973
```

**2. Why: `C_mat` itself anticommutes with `Γ_F`, exactly:**

```
||[Γ_F, C_mat]|| = 11.313708498984752
||{Γ_F, C_mat}|| = 1.6269111658640403e-14   (exact zero, to numerical precision)
```

A single `γ_a` always anticommutes with `Γ_F` (standard Clifford
fact). `C_mat` anticommutes with `Γ_F` too. Composing two
chirality-flipping operators (`C_mat` then `γ_a`) gives a
chirality-*preserving* result — this is forced, not a construction
choice.

**3. `C_mat` is not one of several possible intertwiners — it is unique:**

```
A_stack (the SVD whose nullspace defines C_mat) smallest singular values: [2.0, 2.0, 1.82e-15]
```

Only one near-zero singular value: the SO(10)-covariant
charge-conjugation intertwiner is unique up to phase for this Cl(10)
representation. Directly comparing it to the project's own two named
candidates:

```
C_mat vs C_plus:  relative diff after phase-align = 0.0000
C_mat vs C_minus: relative diff after phase-align = 1.4142
```

`C_mat` (used throughout Phase X for the Yukawa CG tensors) **is**
`C_plus` (used in Z1–Z4 for the real structure `J`) — the same object,
not two independent choices the project happened never to compare.

**4. The mechanism generalizes to the entire Yukawa decomposition, not just the vector channel:**

`Γ_F` anticommutes with any *odd*-length antisymmetrized gamma
product, and `16⊗16 = 10 ⊕ 120 ⊕ 126` for SO(10) — built respectively
from 1-, 3-, and 5-gamma antisymmetrized products, all odd. Flip-parity
= 1 (from `C_mat`) + odd (from the tensor) = even, always. Checked
directly rather than just argued:

```
M120 (sampled 20 of 120 triples): chirality-preserving block ~4.00, chirality-flipping block ~5.9e-15
M126 (sampled 5 of 126 self-dual forms): chirality-preserving block ~5.66, chirality-flipping block ~8.4e-15
```

There is no fourth channel to check — `10⊕120⊕126` is the complete
decomposition. This mechanism, not a per-channel coincidence, accounts
for all of it.

## Verdict — L1, closed, and stronger than Z4

**Within Cl(10)'s 32-dim Fock space, with `Γ_F` the standard Clifford
volume element as the grading and `C_mat` the (unique) SO(10)-covariant
charge conjugation, no term in the complete Yukawa decomposition
`10⊕120⊕126` can be chirality-flipping.** This is not "not yet found" —
it is algebraically excluded, exhaustively, across every channel that
exists. The "re-embed / pick a different block of the same tensors"
route that Z4's own next-step was aiming at is provably not a route at
all: there is no other block, and no other intertwiner, to try.

This also resolves a latent inconsistency the project had not
previously flagged: `C_mat` (Yukawa CG construction, Phase X) and
`C_plus` (candidate real structure `J`, Phase Z1–Z4) are the same
operator. That's either a reassuring consistency (the framework is
using one coherent notion of charge conjugation throughout, not two
unrelated ones) or a red flag that the two roles were conflated without
anyone checking — worth being aware of either way if this thread is
revisited.

## Recommendation — best approach going forward

Two options were on the table after last session:

1. **Accept the no-go as final** for the Cl(10)-intrinsic construction
   and close Priority 1 under this formulation.
2. **Question the premise**: `Γ_F` was taken to be Cl(10)'s own volume
   element, and `H_F` was taken to be the single 32-dim Cl(10) irrep
   (its own `+1`/`-1` chirality eigenspaces standing in for
   fermion/antifermion). Standard NCG-GUT constructions in the
   literature (Chamseddine–Connes–van Suijlekom-style "grand
   symmetry" models) don't do this — they build `H_F` as an
   **externally doubled** space, two separate copies of the 16 with a
   grading and real structure defined independently of Clifford
   chirality, specifically so that the Yukawa block can be placed
   off-diagonal by construction rather than derived.

**Recommended: option 2.** Reasoning: option 1 doesn't fail toward a
*different* mechanism — it simply stops, on a construction that is now
proven (not just suspected) incapable in principle. Option 2 is not
speculative; it is the standard, literature-validated way this exact
problem (chirality-preserving Clifford bilinears vs. a chirality-
flipping Dirac operator) is normally solved in NCG-GUT model-building,
and it directly targets the mechanism identified above rather than
retrying the same one. It is real, scoped new work, not a quick patch —
but it is work with a known destination, which the current route no
longer has.

**Concrete scope for the next phase (Z6), stated so it isn't attempted
carelessly:**

- Define `H_F = C^16 ⊕ C^16` explicitly (two copies, not one 32-dim
  Cl(10) irrep), with grading `ε = diag(+1,...,+1,-1,...,-1)` (16 of
  each) imposed *by construction*, not derived from `Γ_F`.
- Place `M10`, `M120`, `M126` (already correctly built as genuine
  SO(10)-covariant 16→16 maps — nothing about them was wrong, they
  were only being asked to play the wrong role) directly into the
  off-diagonal (first-copy → second-copy) block of `D_F`. This
  satisfies `{ε, D_F}=0` by placement, not by proof — trivial, but only
  because the space was built to allow it.
- Independently define a real structure `J₀` on this doubled space
  (standard candidate: complex conjugation composed with the swap of
  the two copies) and check the KO-dimension conditions
  (`J₀² = ±1`, `J₀D_F = ±D_F J₀`, `J₀ε = ±εJ₀`) explicitly — these
  have never been checked for this doubled construction and are not
  guaranteed to hold just because they hold in the textbook SM case.
- Only after that scaffolding is verified does re-running Z1–Z4's
  order-one condition against the real `M10/M120/M126` (instead of
  Z2's generic random-matrix stand-ins) become a meaningful test of
  whether the graded freedom equals Phase X's 6-or-3 Yukawa
  parameters — which is the original question the whole Z-series was
  trying to answer.

## Next step

Build the Z6 scaffolding above (`H_F`, `ε`, `J₀`) and verify the
KO-dimension conditions before touching the order-one condition again.
This is genuine new construction work, not a rerun of anything in Z1–Z5,
and should be treated and audited as its own phase.
