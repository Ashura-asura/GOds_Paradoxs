# Phase Z11 — sweeping the internal Higgs-direction moduli (this session)

## Question

Z6 through Z10 all fixed **one** internal Higgs direction per channel
(`M10[0]=G[0]`, one `M120` triple `(0,1,2)`, one `M126` orthonormal
component) and used it for every order-one computation. Z9 and Z10
both flagged this as an open item: does `Y_gen` surviving only as a
scalar multiple of `I_3` (or exactly `0` for `M120`) hold across the
**whole** internal moduli space of each channel, or was it particular
to the one direction tested?

## Method

Swept, using the Z10 real-structure-aware ansatz throughout (no
artificial `Hermitian(Y_gen)` constraint):

- **M10** (internal space = the 10 real directions of the vector-**10**,
  `S^9`): all 10 `gamma_a` basis directions, plus 5 random unit
  vectors on `S^9` (generic points, not aligned with any basis axis).
- **M120** (internal space = 120 antisymmetric triples spanning
  `Λ³(10)`): 15 of the 120 basis triples (random sample), plus 5
  random real linear combinations of triples (generic antisymmetric
  3-tensors, not basis-aligned).
- **M126** (internal space = 126-dim self-dual 5-form subspace of
  `Λ⁵(10)`): 15 of the 126 orthonormal basis components (random
  sample; confirmed the self-dual subspace is exactly 126-dimensional
  as expected), plus 5 random complex linear combinations within that
  subspace.

55 internal directions total, each run through the full 64-pair
`su(3)_F` order-one intersection (same method as Z9/Z10), checking (a)
the surviving real dimension matches the expected value (`2` for
`M10`/`M126`, `0` for `M120`) and (b) the surviving texture, when
nonzero, is exactly a scalar multiple of `I_3` (no off-diagonal terms,
no unequal diagonal entries).

## Result

```
M10:  15/15 directions consistent  (10 basis + 5 random) -- surviving dim 2, texture = c*I_3
M120: 20/20 directions consistent  (15 basis + 5 random) -- surviving dim 0
M126: 20/20 directions consistent  (15 basis + 5 random) -- surviving dim 2, texture = c*I_3

OVERALL: ALL 55 DIRECTIONS CONSISTENT, ZERO MISMATCHES
```

Every single direction sampled — basis-aligned and generic random
alike, across all three channels — gives exactly the same qualitative
answer as the one direction Z9/Z10 originally checked.

## Verdict — L1

**L1.** This is not a coincidence needing separate explanation per
direction — it's the expected consequence of the representation-theory
argument Z9 already gave: the order-one condition constrains `Y_gen`'s
transformation under `su(3)_F`, treating `Y_H` as a fixed nonzero
spectator that the whole construction is linear in. Once `Y_H` is
*any* nonzero tensor of the right symmetry type (real symmetric for
`M10`, real antisymmetric for `M120`, complex symmetric for `M126`),
which internal direction it happens to be shouldn't matter to which
`SU(3)_F` irreducible pieces of `Y_gen` survive — only to the overall
scale. The sweep confirms this empirically rather than leaving it
assumed: **the "identity only" / "zero only" result is universal
across each channel's internal moduli space, not an artifact of the
one representative direction used throughout Z6–Z10.**

This closes the specific open item Z9 and Z10 both flagged and did not
resolve. Combined with Z10's fix to the Hermiticity artifact, the
project's core Z-series claim — **unbroken `su(3)_F` forces
generation-blind (or vanishing) Yukawa couplings in every channel,
independent of which internal Higgs direction is chosen** — is now
checked, not assumed, on both fronts that were previously open.

## Remaining caveats (stated plainly)

- The sweep is a large, deliberately varied *sample* (55 directions,
  mixing basis vectors and generic random combinations, across three
  channels) — not an exhaustive or analytic proof over the continuous
  moduli spaces (`S^9` for `M10`, high-dimensional Grassmannians/vector
  spaces for `M120`/`M126`). A sample with zero mismatches across
  basis-aligned *and* generic random points is strong evidence, not a
  formal proof; a closed-form representation-theoretic argument (which
  Z9's writeup already sketched informally) would be the fully rigorous
  version of this result.
- Only single-channel Higgs directions were swept (`Y_H` from one
  channel at a time). Mixed-channel vacua (e.g. simultaneous nonzero
  `M10` and `M126` directions, as a realistic GUT-breaking pattern
  would likely need) have not been tested and could behave differently
  — this is a natural next extension, not covered here.
- The `su(3)_F` generators used are still the standard flavor-space
  Gell-Mann basis (`build_su3f_generators`), as in every phase of the
  Z-series — a reasonable, standard choice, but not itself derived from
  the Cl(10)xE8 construction.

## Next step

With both flagged caveats (the Hermiticity artifact, and the
single-direction restriction) now closed, the natural next extensions
are: (1) mixed-channel Higgs vacua (nonzero `M10` and `M126`
simultaneously — the physically relevant case for realistic symmetry
breaking, per this project's own earlier phases), and (2) formalizing
the representation-theory argument sketched in Z9 as a clean, closed-
form proof (rather than a large empirical sample) that unbroken
`su(3)_F` forces `Y_gen` into the trivial singlet of `Sym²(3)` /
excludes `Λ²(3)` entirely, independent of `Y_H`.
