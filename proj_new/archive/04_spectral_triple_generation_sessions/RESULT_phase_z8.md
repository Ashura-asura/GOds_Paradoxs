# Phase Z8 — does su(3)_F actually reduce the Yukawa parameter count? (this session)

## Question

Z7's corrected next step: stop checking span-membership (shown vacuous
by dimension count) and instead treat the generation-space Yukawa
matrix `Y_gen` (the actual 6-or-3 complex free parameters from Phase
X's own count) as the unknown, and ask whether the order-one condition
forces a **linear relation** among its entries — a genuine reduction —
or is satisfied identically for any `Y_gen` — no reduction at all.
This is the question the whole Z-series exists to answer.

## Method

Fixed one internal Higgs direction, `Y_H = M10[0]` (same object used
throughout Z6/Z7), and built the general ansatz

```
D_F(Y_gen) = A32 ⊗ Y_gen,      A32 = embed_doubled(Y_H)  (Hermitian, from Z6)
```

with `Y_gen` ranging over all `3×3` complex matrices — the most
general possible generation-space coupling, not yet restricted to
Hermitian or symmetric. `D_F(Y_gen)` is **linear** in `Y_gen`, and so is
the order-one commutator `[[D_F,a],J₀bJ₀⁻¹]` for fixed `a`, `J₀bJ₀⁻¹`
(the same Test-A family-gauge choice as Z7: `T_fam_a`, `T_fam_b` = the
1st and 3rd `su(3)_F` Gell-Mann-type generators from
`build_su3f_generators`). Being linear, the full space of constraints
can be found exactly: evaluate the commutator on each of the 9 basis
matrices `E_ij`, stack the results, and read off the rank/kernel — no
numerology, direct linear algebra.

Checked in two independent ways as a cross-validation: (1) SVD kernel
of the complex 9→9216 linear map, basis vectors inspected by hand;
(2) a from-scratch real-coordinate version (18 real unknowns, complex
linearity converted to a real block matrix) with the order-one
condition, Hermiticity of `Y_gen`, and symmetry of `Y_gen` each encoded
as separate real-linear constraints, stacked and rank-checked. Sanity
checks confirm the machinery is right before trusting it: "Symmetric
alone" gives real-dim 12 (= 6 complex, matches Phase X's own count
exactly) and "Hermitian alone" gives real-dim 9, both as expected
before any order-one condition is applied.

## Result

```
real dim after order-one condition alone:                8   (of 18; = 4 complex)
real dim after order-one + Hermitian(Y_gen):              4
real dim after order-one + Symmetric(Y_gen):              6   (= 3 complex)
real dim after order-one + Hermitian + Symmetric(Y_gen):  3

reference, no order-one condition applied:
  Symmetric(Y_gen) alone: real-dim 12  (6 complex -- matches Phase X's own count)
  Hermitian(Y_gen) alone: real-dim 9
```

Both methods agree exactly. **The order-one condition, combined with
the requirement that `D_F` be Hermitian and `Y_gen` be the
symmetric-type coupling the vector-**10** channel requires, reduces
the naive 6 complex (12 real) Yukawa parameters down to 3 real
parameters** — for this one Higgs direction and this one pair of
`su(3)_F` generators.

The surviving 3-parameter family has an explicit, clean texture (not
an opaque numerical subspace):

```
Y_gen(c1,c2,c3) = [[ 0.707c1,   -c3,      0    ],
                   [   -c3,    0.707c1,   0    ],
                   [    0,        0,     c2    ]]
```

A real, symmetric matrix with a **2+1 block structure** — generations
0 and 1 mixing with each other and sharing a common diagonal
coefficient, generation 2 decoupled on the diagonal. This is not
forced to look like this by anything put in by hand; it fell out of
the linear algebra.

## Verdict — L1 for the computation, L2 for the physical conclusion

**L1**: the rank/kernel counts and the explicit texture are exact,
reproducible linear algebra, cross-checked two independent ways, with
working sanity checks on the unconstrained references.

**L2, not yet L1, and this matters**: this is a real reduction *for
one generator pair* (`T_fam_a, T_fam_b` = generators 0 and 2 of 8).
The physical order-one condition must hold for **every** element of
`su(3)_F`, not just one pair — the true constraint is the
*intersection* over all generator pairs, which could be smaller than
this (if other pairs cut the surviving 3-dimensional family down
further) or could coincide (if this pair already captures the full
constraint). That has not been checked and should not be assumed
either way.

There is also a modeling choice flagged honestly rather than hidden:
requiring `Y_gen` to be **both** Hermitian (so this particular
Kronecker ansatz for `D_F` is a valid Dirac operator) **and**
symmetric (the SO(10) group-theory requirement for the **10** channel)
is an explicit, stated assumption about how to embed a
Majorana-type Yukawa coupling into this doubled construction — it has
not been checked against the standard NCG-GUT literature convention
for representing such couplings, and a different (more careful) real-
structure-aware embedding might handle the "symmetric but not
Hermitian" case differently. Recorded as an open modeling question,
not silently assumed correct.

## Next step

1. Repeat this exact computation for the remaining `su(3)_F` generator
   pairs (there are 8 generators; only one pair tested) and take the
   intersection of all resulting kernels — the true test of whether
   3 real parameters (or fewer) survive the *full* family-gauge
   algebra, not just one slice of it.
2. Repeat for the `M120` and `M126` internal directions (only `M10[0]`
   used here) to see whether the same 2+1 texture, a different
   texture, or no surviving freedom appears for the antisymmetric and
   mixed-reality channels.
3. Resolve the flagged modeling question — whether "Hermitian ansatz +
   symmetric Y_gen" is the correct way to represent a Majorana-type
   Yukawa term in this doubled `H_F`, or whether a construction that
   uses the real structure more directly (rather than requiring
   `Y_gen` Hermitian as a byproduct of a simple Kronecker product) is
   needed — before treating "3 real parameters survive" as a finished
   physical statement rather than a well-computed result under a
   stated assumption.
