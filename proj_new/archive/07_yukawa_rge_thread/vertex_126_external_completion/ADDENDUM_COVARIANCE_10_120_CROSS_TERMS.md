# ADDENDUM — Attempted closure of the λ(120,10)/λ(10,120) covariance gap

**Status: partially closed. Do not mark this gap as fully resolved.**

## Why this addendum exists

A repository-consistency audit found that the explicit multi-generator
covariance test (`[T,S_a] = Σ_c R_ac S_c`, run against several independent
generators `T`) had only ever been applied to `λ(10,10)=-8` (sanity case)
and the two new zero entries `λ(10,126)=λ(120,126)=0`. The nonzero
cross-channel entries `λ(120,10)=48` and `λ(10,120)=4` — the *only* source
of Y10–Y120 mixing in the assembled β-system — had been validated only by
"the Schur ratio is constant across every component," never by the same
generator-commutator test used elsewhere. This addendum is an attempt,
using an independently built Cl(10) representation (different code, not
`build_cg.py`), to close that gap.

## What this addendum actually establishes

1. **Independent re-derivation of the values themselves: successful.**
   Recomputing `λ(120,10) = Σ_{b∈120} M_b (M_a^{10})^† M_b`, projected onto
   `M_a^{10}`, gives **48.000000 exactly, std = 0** across all 10
   components of the external index. Recomputing `λ(10,120)` the same way
   gives **4.000000 exactly, std = 0** across all 120 components. This is
   a genuine independent confirmation, from a different gamma-matrix basis
   and different code, of the two numbers already in the vertex table.

2. **The additional multi-generator closure test: did not close, and the
   reason is understood, not hand-waved.** The script also attempted the
   stronger check used for the other entries: pick a generic `so(10)`
   generator `T` (a random real combination of several `Σ_ab`'s, chosen
   to avoid an accidental special-case cancellation found with a single
   `Σ_{0,1}`), extract the rotation matrix `R` from `[T,M_c]=Σ_d R_cd M_d`
   on the 10 and 120 channels separately, then check whether the *vertex
   sum* `S_a = Σ_b M_b X_a M_b` obeys the same covariance law with the
   same `R`. **It did not close** — the residual was of the same order
   as the generator's own coefficients, not floating-point noise.

   Tracing this by hand: the restricted operator commutator
   `[T_16, (Cγ_a)|_{16}]` is **not** the same object as the correct
   charge-conjugation-twisted bilinear-form transformation law. The
   invariance condition for `C` is `TᵀC + CT = 0` (verified exactly,
   residual 0.0), which is a *transpose*-based condition, not the
   commutator condition `[T,C]=0` (which is generically **nonzero** and
   was the unexamined assumption behind the failed closure test). This
   points to a convention mismatch between `M_a = Vᵀ C γ_a V` (transpose,
   matching the literal bilinear-form definition `ψᵀCM_aψ`) and
   `M_a = V^† C γ_a V` (dagger, used throughout this addendum and in the
   original audit, and confirmed to reproduce −8/4/48/8 correctly). These
   two conventions coincide for the *scalar* Schur-ratio computation
   (test 1, above) but evidently do not both satisfy the same naive
   commutator-closure test — reconciling exactly why needs a careful pass
   through the dagger-vs-transpose bookkeeping that this session did not
   complete.

## Honest bottom line

- The **numbers** λ(120,10)=48 and λ(10,120)=4 are now independently
  confirmed twice, by two different code paths (this addendum, and the
  original audit's from-scratch Cl(10) build). Confidence in the values
  themselves is high.
- The **specific style of generator-covariance proof** used elsewhere in
  this repository for λ(10,10), λ(10,126), λ(120,126) has **not** been
  successfully extended to λ(120,10)/λ(10,120) yet. This gap from the
  prior audit is **downgraded from "untested" to "attempted, one
  technical obstruction identified, not yet closed"** — it should still
  be listed as an open item, not a resolved one.

See `covariance_check_10_120_addendum.py` for the runnable script and full
output.
