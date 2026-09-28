# Phase Z4 — projecting Z3 onto Phase X's physical subspace (this session)

## Question

`docs/POST_AUDIT_TARGET.md`'s Phase Z3 update names this as the first,
cheapest next step: Z3 showed `[[D_F,a],JbJ^-1]` goes nonzero in all 9
generation-pair blocks when a real `su(3)_f` generator is put into `a`
— but Z3 used **generic random 32×32 matrices** for the D_F blocks.
Phase X separately proved the only *physical* direction in that space,
per generation pair, is a single fixed CG tensor `T_H` (unique up to
overall complex scale, for a chosen Higgs channel). Does Z3's effect
survive when D_F is restricted to that actual physical direction, or
does it only show up when D_F is given unphysical input?

## Method

`session_new_files/phase_z4_physical_projection_test.py`. Reuses
`vertex_terms_resolved/build_and_test.py`'s own CG construction
verbatim (same gamma matrices, same charge-conjugation `C`, same
16-dim chiral embedding `V`) to build `M10`, the 10 CG matrices for the
vector-**10** Higgs channel — no new construction, no new conventions.

- `T16 = M10[0]` — one fixed physical direction (a specific Higgs VEV
  component; which component is picked is an external VEV choice, same
  status as every other VEV in this project — see
  `docs/POST_AUDIT_TARGET.md` section B).
- `T32 = V @ T16 @ V†` — embedded into the full 32-dim Cl(10) factor
  (`|T16| = |T32| = 4.0000`, confirming `V` is an isometry, i.e. no
  normalization bug in the embedding).
- `D_F_phys`: blocks (0,1) and (1,2) set to `Y01·T32` and `Y12·T32`
  (arbitrary nonzero complex scalars, not fitted to anything), all
  other blocks zero — same skeleton as Z3's `D_F_two`, but "scalar ×
  the one physical direction" replacing "generic random 32×32 matrix."
- Re-ran Z3's exact Test A / Test B, plus a new check: for each nonzero
  induced block, what fraction of its norm lies along `T32` (physical,
  i.e. another valid Yukawa-type term) versus orthogonal to it
  (unphysical, no Yukawa interpretation at all)?

## Result

```
Test A (pure family-gauge action):
Block-norm matrix:
[[0.     0.4031 0.5701]
 [0.4937 0.     0.4031]
 [0.4031 0.4937 0.    ]]
Fraction along physical direction T32:
[[nan  0.  0.]
 [ 0. nan  0.]
 [ 0.  0. nan]]

Test B (SM generator (x) family generator):
Block-norm matrix:
[[0.4663 0.3475 0.2637]
 [0.337  0.2786 0.3318]
 [0.2371 0.3208 0.4446]]
Fraction along physical direction T32:
[[0.     0.0272 0.095 ]
 [0.     0.09   0.    ]
 [0.0203 0.     0.    ]]
```

Two findings, both against Z3 carrying real selection power:

*(Note, added after the grading-axiom check below: these two findings
are numerically real but are shown further down to be about an
invalid candidate D_F — read them as "what the numbers do," not yet as
"what they mean physically." The grading check is what actually
resolves the question this file set out to answer.)*

1. **Test A: the diagonal blocks (0,0), (1,1), (2,2) are exactly
   zero** with physical input — versus Z3's generic-matrix run, where
   *all 9* blocks including the diagonal were nonzero. Some of Z3's
   effect was an artifact of feeding the commutator matrices with no
   physical meaning.
2. **Every nonzero induced block, in both tests, has essentially zero
   overlap with the one physical direction `T32`** (0 to ~0.095 out of
   a maximum of 1.0). What Z3's family-gauge action generates in the
   off-blocks is overwhelmingly *not* a new Yukawa-type term — it's
   populating directions in the 32×32 space that Phase X already ruled
   out as gauge-non-invariant, i.e. not physically real.

**L2, not L1** (see caveat below): this is evidence, not proof, that
Z3's cross-generation effect is close to orthogonal to the actual
Yukawa parameter space, i.e. that it plausibly does *not* constrain the
6-or-3 count in section C of `docs/POST_AUDIT_TARGET.md`, consistent
with the "likely fails net" expectation already on record — but now
via a different, independent line of evidence than the Rule-9
gauge-boson-cost argument.

## Grading-axiom check (this session, `check_grading.py`) — L1, and it changes the verdict

The projection result above still needed one check before it could be
trusted at all: does `T32` (hence `D_F_phys`) actually satisfy the
standard noncommutative-geometry grading axiom for a Dirac operator —
`{Γ_F, D_F} = 0` (D must flip chirality), not `[Γ_F, D_F] = 0`
(D preserves chirality)? Neither Z2, Z3, nor the projection test above
had checked this. Directly computed:

```
||{Gamma_F, T32}|| = 8.0        (exactly ||T32|| * 2, i.e. maximal violation)
||[Gamma_F, T32]|| = 0.0        (exact)
||T32|| = 4.0
```

**`T32` commutes with Γ_F exactly; it does not anticommute.** It is a
chirality-*preserving* operator, not a chirality-flipping one. This is
a real, structural finding, not a numerical artifact (the anticommutator
norm is exactly twice the operator norm — the algebraic signature of
total failure to anticommute, not partial/noisy failure).

**This means Phase X's CG tensor `M10` and Z1–Z3's graded `D_F` are, as
currently built, not the same kind of object.** `M10` encodes the
SO(10) Yukawa coupling using charge conjugation to let a single chiral
16 stand in for both a fermion and its conjugate (correct and standard
for SO(10) model-building) — but that construction is chirality-
*preserving* by nature, while the spectral-triple `D_F` that Z1–Z3's
order-one condition is stated for is required to be chirality-
*flipping* by the grading axiom itself (Z1's own moduli argument
implicitly assumed this, per the standard NCG axiom set it invoked).
**Z4's `D_F_phys` was therefore never a valid candidate in the first
place** — not because of a bug, but because the physical Yukawa tensor
and the graded spectral-triple Dirac operator are not interchangeable
without an explicit map between them that this project has not built.

## Verdict

**Closed, L1, negative — but not the negative result the "next step"
was aiming for.** Z4 does not establish whether Z3's cross-block effect
overlaps the physical Yukawa subspace, because the physical Yukawa
tensor `T32` cannot legally be substituted for a block of `D_F` in the
graded order-one-condition formalism at all — doing so violates the one
axiom (`{Γ_F, D_F} = 0`) that makes `D_F` a Dirac operator in this
framework to begin with. **This is a genuine Rule-8 structural
failure**, and it is a more fundamental gap than the one Z4 set out to
check: it means the entire Z1→Z3 line's central question — "does the
graded spectral triple's freedom equal Phase X's 6-or-3 Yukawa
parameters?" — has never actually been tested against Phase X's real
Yukawa tensors, only against Z2's generic, chirality-agnostic random
matrix stand-ins and (in Z3) an `su(3)_f` generator acting on those same
generic stand-ins.

## Next step

Before Z3's cross-block effect can be checked against physical Yukawa
directions at all, someone needs to build the actual bridge: an
explicit, grading-respecting map from Phase X's chirality-preserving CG
tensors `M10`/`M120`/`M126` to a chirality-*flipping* block of a graded
`D_F` on the 32-dim Fock space (standard in the NCG-GUT literature via
the `Γ_F`-odd part of the Dirac operator built from a "mass matrix ⊗
off-diagonal chirality block" construction — not attempted here, and
not a small addition; it is a genuine new construction, not a
parameter tweak). Until that bridge exists, **no numeric result in
Z2, Z3, or Z4 about "does the order-one condition constrain the Yukawa
freedom" can be read as being about the actual Yukawa freedom** — they
are all, as built, statements about a different (chirality-preserving)
object living in the same vector space. This should be treated as a
correction to Phase Z1's framing, not just an unresolved technical
detail, and is recorded as such in `docs/MECHANISM_FAILURE_MAP.md`.
