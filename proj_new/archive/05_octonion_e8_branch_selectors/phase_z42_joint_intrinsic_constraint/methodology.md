# Z42 Methodology

Honesty about what is cited vs. derived vs. checked, per this
project's audit culture (Rule 1: no numerology; Rule 9: discriminating
power).

## Cited, not re-derived
- `E8 ⊃ E6 × SU(3)`, `248 = (78,1)+(1,8)+(27,3)+(27̄,3̄)`: Slansky
  1981, "Group Theory for Unified Model Building," Table 82. This is
  the same branching this project has used since Z6; re-derivation
  from the E8 root system is already done elsewhere in the repo
  (`phase_a2_e8_core.py`, `phase_z40.../e8_branching_analysis.py`) and
  not repeated here.
- First Fundamental Theorem of invariant theory for `SL(3,C)`/`SU(3)`:
  Weyl, 1939, *The Classical Groups*, Ch. II §6. This is a standard
  100-year-old result, not a novel claim of this project. It is the
  load-bearing citation for Task 5's theorem — flagged explicitly as
  cited rather than machine-proved from scratch, which would require
  invariant-theory tooling (e.g. a Gröbner-basis / SAGT computation)
  this environment does not have.

## Derived in this phase (new relative to Z39/Z40)
- That the SU(3)_f content of the *entire* 248 (not just the matter
  piece) is `{1,3,3̄,8}`, and that `8` decomposes with no leftover
  invariant-theory content (`3⊗3̄ = 1⊕8`, dimension-exact).
- The Task 5 theorem's generalization from "cubic Casimir, single
  flavon" (Z39) to "any order, single flavon" — this follows
  immediately once the FFT is invoked on the representation content
  established above, but had not been stated in the repo before this
  phase.
- The freedom-counting comparison in Task 4 (1 physical dof delivered
  vs. ~10 needed per sector) — arithmetic, not previously tabulated
  explicitly against the 10-parameter target.

## Numerically checked (Monte Carlo, machine precision, per Rule "L1
where possible")
- `δ` and `ε` invariance under random `SU(3)` elements (errors
  `< 2e-14`).
- A generic (non-`ε`) rank-3 tensor failing invariance in `>95%` of
  random trials — supporting evidence for the FFT claim at the
  relevant low degree, not a substitute for the classical proof.
- `ε_ijk φ^i φ^j φ^k = 0` for a single vector `φ`, exactly, over 500
  random trials (max value `0.0` to floating-point precision).
- Flatness of the single-flavon potential along the `SU(3)_f` orbit at
  fixed radius (`std < 1e-10` across 64 random directions).

## What was NOT attempted
- Alternative E8 maximal subgroups other than `E6 × SU(3)_f`.
- The non-factorized / NCG spectral-triple construction (Priority 1,
  repeatedly flagged as needing tooling this environment lacks).
- A from-scratch computer-algebra proof of the Weyl FFT itself.

Per Rule 9, none of Tasks 1–5 merely reproduce a previously-known
number: Task 1 checks a fact (full-adjoint SU(3)_f content) not
explicitly checked before; Task 5 produces a strictly more general
theorem than Z39/Z40's case-by-case results, with discriminating power
(it rules out an entire *class* of future attempts — "try a higher-
order E8 invariant" — rather than one more instance of it).
