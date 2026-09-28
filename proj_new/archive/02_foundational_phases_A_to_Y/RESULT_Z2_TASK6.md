# RESULT_Z2_TASK6.md — moduli-space dimension

Response to Task 6 of `PRIORITY_2_EXPLICIT_J_GAMMA_DIRAC_MODULI_PROMPT`.
New test: `tests/test_dirac_moduli_dimension.py` (4/4 pass).

## Computation

From Task 5: the 9 generation-pair blocks (k,l = 1..3) are constrained
independently, with per-block freedom equal to Phase X's Hom_G
multiplicity (1, for each eligible H in {10,120,126}; 0 for every other
H — Phase X's own result, imported unchanged, not re-derived here).

Before any further constraint: **9 independent complex coefficients**
y_kl, one per block.

The one remaining constraint — NOT from order-one/reality/chirality
(Task 5 shows those impose nothing across blocks), but from the
**exchange symmetry of the two fermion 16's meeting the same H field**
(a Bose/Fermi-statistics fact about the coupling `16_i (x) 16_j (x) H`,
already identified by Phase X as the origin of the symmetric-vs-
antisymmetric split) — identifies y_kl with +/- y_lk:

- **H = 10 or 126 (symmetric):** y_kl = y_lk. 3 diagonal + 3 independent
  off-diagonal pairs = **6 complex parameters** = dim(Sym^2(C^3)).
- **H = 120 (antisymmetric):** y_kl = -y_lk forces y_kk = 0. 3
  independent off-diagonal pairs = **3 complex parameters** =
  dim(Lambda^2(C^3)).

## dim(M_D)

**dim(M_D) = 6 (H=10,126) or 3 (H=120) — exactly Phase X's number, not
smaller, not larger.**

This is **Outcome B** in the prompt's own classification: "the spectral
triple reproduces the Phase X freedom... constrains the allowed
structure but does not determine Yukawa values." Outcome A (a genuine
reduction below 6/3) is now excluded by Task 5's block-independence
proof, not merely unobserved. Outcome C in the sense of "more freedom
than Phase X" is also excluded, since the 9-before-statistics count is
itself capped by Phase X's per-block multiplicity of exactly 1 (not
higher), and the statistics constraint is forced (not optional) by which
H channel is being considered.

## Confidence level

**L1** for "no relation among generation-pair blocks can come from
order-one/reality/chirality/gauge-covariance" (proved directly, Task 5).
**L1** for the arithmetic 9 -> 6 or 9 -> 3 under the symmetric/
antisymmetric identification (trivial combinatorics, this file).
**L2** for the per-block multiplicity being exactly 1 for H in
{10,120,126} and 0 otherwise, since that number is imported from Phase
X, not re-derived with an explicit numerical tensor in this phase (see
`RESULT_Z2_TASK4.md`'s honest caveat).

Combined: **dim(M_D) = 6 or 3 is proved at L1 conditional on Phase X's
L1/L2 multiplicity count**, which is a strictly stronger status than
Phase Z1's "argued, not independently computed" — the open step Phase Z1
flagged (whether order-one/reality/chirality act block-by-block on
generation-pair indices) is now closed, in the affirmative, at L1.
