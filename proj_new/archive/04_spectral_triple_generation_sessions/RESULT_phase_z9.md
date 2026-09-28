# Phase Z9 — the full su(3)_F algebra, not just one generator pair (this session)

## Question

Z8 flagged, as its first honest caveat, that the "3 real parameters
survive" result used only one pair of `su(3)_F` generators out of 8.
The order-one condition must hold for the **whole** algebra. This
phase closes that gap: intersect the constraint over all 8×8 = 64
generator pairs and see whether 3 real parameters really survive, or
fewer.

## Method

Same setup as Z8 (`Y_H = M10[0]`, `A32 = embed_doubled(Y_H)`,
`D_F(Y_gen) = A32 ⊗ Y_gen`), same Hermitian + symmetric constraints on
`Y_gen`. Instead of one `(a,b)` generator pair, looped over **all**
`i,j ∈ {0,...,7}` (`build_su3f_generators`'s full basis), accumulated
each pair's order-one constraint as a real `18×18` Gram matrix
(`GᵀG`, built incrementally to avoid materializing a
`1,179,684 × 18` matrix directly — the naive stacked-SVD approach
failed with a 10 TiB memory allocation on the first attempt, caught
and fixed rather than skipped), and read off the joint kernel from the
Gram matrix's null eigenspace.

## Result

```
Total real dim surviving ALL 64 su(3)_F generator pairs + Hermitian + Symmetric: 1

Smallest eigenvalues of the accumulated Gram matrix: [0, 4, 288, 288, 288, 288]
(one exact zero, then a clean gap to the next eigenvalue — not a near-degenerate cluster)

Surviving 1-parameter direction:
Re(Y_gen) = -0.577 * I_3   =  -1/sqrt(3) * I_3
Im(Y_gen) = 0
```

**Only one real parameter survives the full `su(3)_F` algebra, and its
texture is exactly proportional to the identity matrix.** Not "close
to diagonal" — exactly diagonal, exactly equal on all three entries,
to the numerical precision checked. Going from one generator pair (Z8:
3 real parameters, a nontrivial 2+1 texture) to the full 8-generator
algebra (Z9: 1 real parameter, pure identity) is a big, clean drop,
not a gradual one — consistent with the single-pair result being a
weaker, partial constraint, as it should be.

## Verdict — L1, and it explains something from the very start of this project

**L1**, directly computed, reproducible, sanity-checked (rank via two
methods, clean eigenvalue gap rather than an ambiguous near-zero
cluster).

**This closes a loop back to the original heterotic-audit material this
whole project started from.** An *unbroken* `su(3)_F` acting on three
identical generations forces the Yukawa coupling to be exactly
generation-blind (`Y_gen ∝ I_3`) — i.e., **all three generations get
identical mass, no hierarchy, no mixing.** That is not a viable
description of the real Standard Model (which has a roughly
`m_t : m_c : m_u` hierarchy spanning several orders of magnitude, and
nontrivial CKM mixing). This is exactly *why* the earliest phases of
this project (the pseudo-Goldstone / Froggatt-Nielsen `U(1)_A`
mechanism, `β ~ e^{-S}` hierarchy generation) exist in the first
place: **`su(3)_F` must be spontaneously broken**, not left exact, for
the model to produce anything resembling real fermion masses. This
phase gives that requirement a first-principles derivation rather than
an assumption: it's not a modeling choice to break `su(3)_F`, it's
forced, because the unbroken case is already excluded by direct
computation of what survives the order-one condition.

**Caveat, stated plainly**: this used one Higgs internal direction
(`M10[0]`) and one representation choice for how `Y_gen` sits in
`D_F`, per Z8's own flagged modeling assumption. The "identity only
survives" conclusion should be checked against `M120`/`M126` directions
before treating it as fully general — though given the argument's
flavor (a family-gauge-invariance-type obstruction), it would be
somewhat surprising, not reassuring, if a different Higgs direction
escaped it.

## Next step

1. Repeat for `M120` and `M126` internal directions — check whether
   "identity only" is universal across channels or specific to the
   vector-**10**.
2. If universal: the natural reading is that this project's entire
   premise (needing a spontaneously-broken flavor symmetry with a
   pseudo-Goldstone/FN-type mechanism to generate hierarchy, rather
   than an exact `su(3)_F`) is now supported by a direct calculation
   inside the Cl(10)×E8 framework itself, not just borrowed
   phenomenological reasoning from outside it. That would be worth
   stating as a completed, load-bearing result in the project's
   overall status, not just another phase file.
3. Resolve Z8's still-open modeling-assumption caveat (Hermitian +
   symmetric ansatz for the Majorana-type embedding) — it underlies
   this result too, and should be checked before either conclusion
   above is treated as final.

## Follow-up (same session) — checked M120 and M126, and the pattern is exact

Repeated the full-algebra (all 64 pairs) computation for the other two
Yukawa channels, using the correct generation-space symmetry for each
(`M120`: `Y_gen = -Y_gen^T`, antisymmetric; `M126`: `Y_gen = Y_gen^T`,
symmetric, same as `M10`):

```
M10  (symmetric):     1 real parameter survives -- Y_gen = -1/sqrt(3) * I_3
M126 (symmetric):     1 real parameter survives -- Y_gen = -1/sqrt(3) * I_3   (identical texture)
M120 (antisymmetric): 0 real parameters survive -- Y_gen forced to exactly zero
```

**This is not a coincidence needing a separate explanation per channel —
it's exactly what SU(3) representation theory predicts once `su(3)_F`
is treated as a genuine gauge symmetry.** A gauged symmetry requires
the physical coupling to be an invariant tensor under it. For the
fundamental of SU(3): the symmetric 2-tensor (`Sym²(3)`) decomposes as
a trivial singlet (`∝ I_3`) plus a traceless-symmetric **6** — only the
singlet survives contact with an exact gauge symmetry, which is
exactly the one nonzero direction found for `M10`/`M126`. The
antisymmetric 2-tensor (`Λ²(3) ≅ 3̄`) contains **no singlet at all** —
consistent with the found result that `M120` is forced to exactly
zero, not "small," not "constrained," identically zero.

This raises the earlier L1/L2 status: the computation isn't just
producing a number that happens to match expectations — it's
reproducing known, independent representation theory as a side effect
of the NCG order-one condition, which is a real (if indirect)
consistency check on the whole Z6→Z9 construction, not only on this
specific claim about flavor symmetry.

## Updated conclusion

**Exact, unbroken `su(3)_F` is now shown, by direct first-principles
computation rather than assumption, to forbid any realistic fermion
mass structure in this framework**: symmetric-channel Yukawas
(`10`, `126`) are forced to universal, generation-blind couplings
(no hierarchy, no mixing), and the antisymmetric channel (`120`) is
forced to vanish entirely. Spontaneous breaking of `su(3)_F` — the
pseudo-Goldstone / Froggatt-Nielsen mechanism the very first document
in this project was built around — is not an optional modeling choice
layered on top of the Cl(10)×E8 framework; it is now a *derived
necessity* of that framework, given this construction. That's a
substantive, load-bearing result for the project's overall status, not
just another phase file — recommend flagging it as such in whatever
top-level status document gets updated next.

## Remaining next step

Z8's flagged modeling caveat (whether "Hermitian ansatz + symmetric/
antisymmetric `Y_gen`" is the right way to embed a Majorana-type
Yukawa coupling in this doubled `H_F`, versus a more careful real-
structure-aware construction) still underlies all of Z8/Z9's results
and should be resolved before this is treated as fully settled rather
than "settled under a stated, reasonable, but unverified assumption."
