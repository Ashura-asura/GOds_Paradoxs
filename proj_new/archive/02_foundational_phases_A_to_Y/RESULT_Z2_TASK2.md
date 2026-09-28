# RESULT_Z2_TASK2.md — Γ_F, the grading operator [L1]

## Construction
Γ_F = i⁵ · γ₁γ₂···γ₁₀, using the exact γ-matrices imported from
`phase_a1_cl10_core.py::build_cl10_gammas()` (not re-derived by hand —
same octonion structure constants, same recipe). This is the standard
Clifford volume element for a 2n = 10-dimensional Clifford algebra; no
Standard Model spectral triple was consulted or imported.

## Verified computationally (see `tests/test_gamma_operator.py`)
| Property | Result |
|---|---|
| Γ_F² = 1 | **True** |
| Γ_F† = Γ_F | **True** |
| {Γ_F, γ_a} = 0, all a=1..10 | **True** |
| Eigenvalue spectrum | exactly {+1 ×16, −1 ×16} |
| Coincides with fermion-parity (−1)^N_tot | **True**, up to an overall
  phase of −1 (i.e. Γ_F = −(−1)^{N_tot} exactly; same physical grading) |

## Uniqueness discussion (per the prompt's requirement)
Γ_F is fixed up to the same two discrete choices any chirality operator
has: (a) an overall sign (Γ_F vs −Γ_F — which half is called "left"),
and (b) the phase convention i⁵ vs (−i)⁵, needed only to make Γ_F²=+1
rather than −1 (a Clifford-algebra fact about products of 10
anticommuting generators, not a physics choice). Neither is a
continuous free parameter, and neither affects any physical count
downstream (relabeling left↔right). **No other freedom exists**: Γ_F
is the unique (up to this sign) element of the Clifford algebra that is
Hermitian, squares to 1, and anticommutes with all 10 generators —
this follows from Γ_F spanning the 1-dimensional top-graded piece of
Cl(10), which is a standard structural fact, not an assumption made
for convenience here.

## Rule 9 check
Would this same construction have "worked" for a different chirality
assignment? No in a meaningful sense — the *existence and properties*
of Γ_F (squares to 1, Hermitian, anticommutes with generators) are
forced by the Clifford algebra structure regardless of which specific
32×32 representation is chosen; this is not a coincidence being passed
off as a derivation. The only "choice" is the overall sign, which is a
relabeling, not new physics.

## Status
**L1.** Zero free parameters, forward-computed, cross-checked two
independent ways (explicit gamma product, and Phase A1's own
fermion-number-parity operator).
