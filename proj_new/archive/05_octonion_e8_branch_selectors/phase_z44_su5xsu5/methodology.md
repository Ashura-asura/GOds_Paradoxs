# Z44 Methodology

Matches the Z39-Z43 methodology exactly, applied to the SU(5)_A x
SU(5)_B branching:

| Quantity | How computed here | How computed in Z39-Z43 |
|---|---|---|
| Branching / dimension checks | Direct integer/rational arithmetic on cited (Slansky, Georgi-Glashow) branching rules | Same (Z43's Cauchy-formula dimension check) |
| Factorized vs. non-factorized structure | Direct matrix construction (Kronecker products), measured deviation from pure product structure | Z43: explicit basis construction of Lambda^3(C^9), classification of basis elements by color/family index mixing |
| Commutant / residual freedom | Generators built explicitly, commutator condition vectorized, nullspace found via Hermitian Gram-matrix eigendecomposition (equivalent to, and cross-checked against, direct SVD) | Z21: identical technique (build generators, vectorize, SVD nullspace), on a differently-shaped problem |
| Freedom counting | Complex dimension counts, no fitting | Z42 Task 4: same style (dimension counting, "no fitting; only dimension counting") |
| External-input flagging (Rule 1) | Explicit check: does fixing a 3-dimensional generation direction inside the untouched family block require an unmotivated extra choice? | Same question asked of Z42's flavon direction |

## Deviations from Z39-Z43's exact numerical setup

- Z21's commutant calculation is embedded in this project's
  Cl(10)-based Hilbert space construction (H_F = C^32 (x) C^3); this
  phase does not reuse that Hilbert space, because the object under
  test (SU(5)_A x SU(5)_B bifundamental pieces of the E8 adjoint) is
  a different representation entirely. Instead, the solver was
  reimplemented independently and cross-checked against Z21's own
  published answer (commutant dimension exactly 1 for SU(3)_f acting
  irreducibly) before being applied to the new case. This is flagged
  explicitly rather than silently assumed to generalize.
- The original SVD-based nullspace approach OOM'd at this problem's
  size (50-dimensional ambient space, 12 generators -> a 30000x2500
  matrix). Replaced with the mathematically equivalent Gram-matrix
  eigendecomposition (nullspace of L is the nullspace of L^H L), which
  is a standard, exact reformulation, not an approximation -- verified
  by reproducing Z21's exact known answer first.

## Z44-R1 addendum

A post-closure audit pass added
`scripts/z44_audit_commutant_recheck.py`, which (a) checks the
spectral gap around the original commutant=200 result, and (b)
recomputes the commutant under the equal-footing assumption that
SU(5)_B is also gauged (24 generators via the induced action on
Lambda^2(C^5), added to the original 12 SM generators). This produced
the corrected commutant value of 2 for the fair comparison against
Z21. See `audit_report.md` and `interpretation.md` for the full
correction and its mathematical basis (Schur's Lemma applied to both
factors). This is an additive check, not a rerun of Tasks 1-4: the
original scripts and their outputs are unchanged and still stand for
the ungauged-SU(5)_B question they were scoped to answer.

## What this phase does NOT compute

Full physical Yukawa-freedom counting (masses, mixing angles, phases,
as in Z42 Task 4) was not attempted here, because that requires first
deciding which pieces of the (5,10bar)+(5bar,10)+(10,5bar)+(10bar,5)
content play the role of matter vs. Higgs -- a model-building choice
this phase's brief did not ask for and that would itself need to be
justified under Rule 1. The commutant/freedom count computed here
(Task 4) answers the prior, more basic question: is there ANY
gauge-forced constraint on the generation direction at all, before
any Yukawa structure is even written down. The answer is no.
