# Phase Z12 — mixed-channel (M10 + M126) Higgs vacuum (this session)

## Question

Z11's first flagged next step: every order-one computation from Z6
through Z11 turned on **one** channel's Higgs direction at a time. A
realistic symmetry-breaking vacuum has multiple channels nonzero
together. Because the order-one commutator is linear in `D_F`, and
`D_F` is linear in each channel's contribution, the joint constraint
with two channels on is the kernel of the **sum** of their commutator
images — not automatically the direct sum of the two single-channel
kernels. Cross-channel cancellation (a forbidden texture in one
channel compensated by a matching texture in the other) is logically
possible and has to be checked, not assumed away.

## Method

Turned on `M10` and `M126` simultaneously (the two symmetric channels
— `M120`'s antisymmetric `Y_gen` lives in an orthogonal constraint
block and was already shown forced to zero across the whole moduli
space in Z11, so it's not a candidate for hiding anything here).
Built the joint 36-real-parameter linear map (18 for `Y_gen10`, 18 for
`Y_gen126`), with `D_F = embed_doubled(Y_H^{(10)} (x) Y_gen10 +
Y_H^{(126)} (x) Y_gen126)`, accumulated the Gram matrix over all
8x8=64 `su(3)_F` pairs (Z9/Z10's method), and took the joint kernel.

Checked explicitly whether the joint kernel is *exactly* the direct
sum of the two single-channel kernels — i.e. whether the 4 "expected"
basis vectors (`Y_gen10=I_3` alone, `Y_gen10=iI_3` alone,
`Y_gen126=I_3` alone, `Y_gen126=iI_3` alone, each with the other
channel's block zero) span the same 4-dimensional space the Gram
matrix's null eigenspace finds — not just that the dimensions match.

## Result

```
Joint surviving real dim: 4  (direct-sum expectation: 2 + 2 = 4)
smallest eigenvalues: [0, 0, 0, 0, 288, 288, 288, 288]   (clean gap)

All 4 "expected" pure-channel basis vectors: exactly in the kernel
(||GtG @ v|| ~ 1e-13, machine precision)
Combined rank of [null_basis | expected_basis] = 4  (same span, not larger)
```

The raw eigenvectors returned by the numerical solver for this
degenerate 4-dimensional null space are, individually, rotated
combinations that mix both channels — but that is exactly what's
expected from an eigensolver acting on a degenerate (all-zero-
eigenvalue) subspace, which returns an arbitrary orthonormal basis of
that subspace, not a physically preferred one. The explicit check
above (both directions of containment: expected basis vectors lie in
the kernel, AND together with the solver's null_basis they don't span
anything bigger than dimension 4) rules out the more interesting
possibility — a genuine cross-channel mode not reducible to either
channel's identity direction alone.

## Verdict — L1

**L1.** No cross-channel cancellation occurs. Turning on `M10` and
`M126` simultaneously gives exactly the direct sum of what each gives
alone: `Y_gen10 = c1 * I_3`, `Y_gen126 = c2 * I_3`, `c1, c2` independent
complex numbers — 4 real parameters total, no new freedom and no
hidden constraint from the combination. This is a negative result in
the sense the project's own conventions treat as a real, valuable
finding (Rule 8, per the project's earlier phases): the two symmetric
channels don't talk to each other through the `su(3)_F` order-one
condition, so the "generation-blind, no hierarchy" conclusion for each
channel individually is not an artifact of testing them in isolation —
it survives the more realistic mixed-vacuum scenario unchanged.

## Remaining caveats

- Only `M10 + M126` was tested (the two symmetric channels). A
  three-channel vacuum with `M120` also nonzero was not separately
  checked, though there's no structural reason (given `M120`'s
  antisymmetric block is already orthogonal to the symmetric
  constraint rows) to expect a different outcome.
- Only one internal direction per channel was used here (`M10[0]`,
  the same `M126` direction as Z9/Z10) — the moduli sweep (Z11) was
  not repeated in the mixed-vacuum setting. Given Z11's uniform result
  across 55 single-channel directions and this phase's finding of no
  cross-channel effect, a mismatch seems unlikely, but it hasn't been
  directly checked.

## Next step

If a genuinely mixed vacuum with all three channels together (and
swept across internal directions) is wanted for full rigor, that's a
natural (if computationally heavier) extension. Otherwise, this
closes the mixed-vacuum question raised in Z11.
