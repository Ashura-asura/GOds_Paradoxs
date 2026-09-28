# Phase Z21: the self-twist escape, closed for its whole natural class
# — not just the one example tested in Z20

**Status: closed, L1. Confirms and generalizes the connection Z20
flagged as "plausible, not confirmed." Net effect on the free-parameter
count: none — this closes an avenue, it does not open one.**

## What Z20 left open

Z20a showed the self-twist ρ_D = Ad(e^{iD}) escapes the scaling no-go.
Z20b showed it reintroduces a conjugation-orbit degeneracy under the
algebra's commutant. Z20's honest gap: *is that commutant literally the
same SU(3)_f already gauged and closed negative in Z6–Z14?* — flagged
as plausible, explicitly not confirmed, and named as the concrete next
computation.

## Step 1 — the commutant, confirmed directly [L1]

This project's own H_F = C^32 ⊗ C^3 construction (`support/z2_hilbert_space.py`,
in use since Phase Z2 and unchanged through Z6–Z18) extends every SM
gauge generator trivially onto the generation factor: `a → a ⊗ I_3`.
Checked directly, numerically, against this project's actual gamma
matrices and SM generators (`build_sm_generators_on_cl10`), against an
arbitrary complex 3×3 matrix `M`:

```
max |[a ⊗ I_3, I_32 ⊗ M]| = 0.0   (exact, all SM generators, random M)
```

**The commutant of the SM gauge algebra on H_F contains all of
`I_32 ⊗ Mat_3(C)`** — not by assumption, by construction, confirmed.

## Step 2 — Schur's Lemma, verified not cited [L1]

The su(3)_f generators already built in this repo (`build_su3f_generators`,
standard Gell-Mann/2, the same ones gauged in Z9–Z18) act as the
**irreducible** fundamental representation on the C^3 generation
factor. Solved directly (not asserted): the linear system "which 3×3
operators commute with all 8 generators" via vectorized commutators
and SVD. **Nullspace dimension: exactly 1**, and the nullspace vector's
deviation from pure `I_3` is ~2×10⁻¹⁶ (machine zero). This is Schur's
Lemma, verified on this project's own matrices rather than cited from a
textbook.

## Step 3 — generalizing Z20b for free

Z20b's conjugation-covariance proof never actually used anything
specific to `e^{iD}` — it used only the telescoping identity
`(UDU⁻¹)ⁿ = U DⁿU⁻¹`, which holds for **any** power `n`, hence for
**any** analytic function `f` in a self-twist `ρ_D = Ad(f(D))`. So the
conjugation-orbit degeneracy from Z20b, and therefore this phase's
closure, applies to the **entire class** of functional-calculus
self-twists at once — not merely the one candidate tested in Z20.

## Putting it together — the closure

For a self-twisted `D_F` (any `f`) to be an isolated fixed point rather
than one representative of a continuous orbit, it must be invariant
under conjugation by the full residual symmetry Z20b proved exists.
Restricted to the generation factor, that symmetry includes the full
irreducible SU(3)_f action (Step 1), so by Schur's Lemma (Step 2) the
only invariant generation-space operators are proportional to `I_3`.

**Consequence: an isolated self-twisted `D_F`, for any twist in this
entire natural class, is forced to be generation-blind — proportional
to the identity on the flavor index.** That is the precise mathematical
statement of *degenerate masses across all three generations* — the
same conclusion Z6–Z14 reached by gauging SU(3)_f directly and running
the (untwisted) order-one condition, now reached independently, from
pure representation theory, without gauging anything or assuming any
dynamics.

**This is a stronger and more general result than Z20 flagged as
possible.** It does not merely make the SU(3)_f connection "plausible" —
it derives it, for the whole `Ad(f(D))` family, not one member.

## What this does *not* close

Honestly scoped, not overclaimed:
- This closes twists of the form `ρ_D = Ad(f(D))` — inner automorphisms
  built by functional calculus on `D_F` itself. A twist that isn't of
  this form — e.g. one that genuinely entangles the generation index
  with the Cl(10) factor from the start, rather than acting as a
  trivial spectator to it the way this project's H_F = C^32 ⊗ C^3
  construction has throughout — is not addressed here, because Step 1's
  commutant computation is specific to that tensor-product structure.
  Building such a construction would be a different project: it would
  mean generation is no longer a separate, trivially-acted-on factor,
  which is a structural choice this whole codebase (Z2 onward) has made
  and not revisited.
- This is not a claim that *no* twist whatsoever can work — only that
  the natural, minimally-invented class (Rule 1: no unexplained new
  function beyond "some function of D") cannot.

## Rule 9 check

Non-numerological: both steps are exact linear-algebra facts (zero
residual to machine precision), verified on this project's own
matrices, not fitted to reproduce a known mass ratio. Falsifiable: a
different su(3)_f-type generator set that failed to act irreducibly, or
an SM-generator embedding that didn't act trivially on the generation
factor, would have broken this argument and it would have said so.

## Net verdict

**Status remains 0/19.** Priority 1's self-twist branch is now closed,
not merely narrowed, for the entire natural class of such twists. What
remains open is thin: a twist construction that does not act as
`Ad(f(D))` and does not treat generation as a trivial spectator factor
— which is no longer "try a self-referential twist" but "build an
entirely different Hilbert-space/algebra structure where generation and
Cl(10) are not separately factored," a materially bigger undertaking
than anything tested in Z1–Z21, and one this project has not yet
attempted from any angle. Consistent with `docs/solution.md`'s own
standard ("why 'try harder' stops being the right instruction"): this
is the point to say so plainly rather than manufacture a new subphase
for its own sake.

## Reproducibility

`phase_z21_schur_closure.py` — pure numerical linear algebra (numpy),
built directly on this project's own `support/z2_hilbert_space.py` and
`support/cl10_gamma_J.py` imports, no new gamma-matrix or generator
recipe introduced. Runs clean, exact to machine precision.
