# RESULT_Z2_TASK1.md — explicit H_F = C^32 (x) C^3

Response to Task 1 of `PRIORITY_2_EXPLICIT_J_GAMMA_DIRAC_MODULI_PROMPT`.
New file: `support/z2_hilbert_space.py`. New test: `tests/test_hilbert_space.py`
(5/5 pass).

## What was built

- **Cl(10) factor (C^32):** reused, unchanged, from `support/cl10_gamma_J.py`
  / `phases/phase_a1_cl10_core.py` — the same 32-state Witt-pair Fock space
  every other phase in this repo uses. Not rebuilt with new conventions.
- **Generation factor (C^3):** the standard orthonormal basis, verified.
- **SU(3)_f generators:** the 8 standard Gell-Mann matrices / 2, verified
  Hermitian, traceless, and closing the su(3) algebra ([T1,T2]=iT3 checked
  directly).
- **H_F = C^32 (x) C^3, dim = 96.**
- **SM gauge generators on H_F:** Phase A1's own SU(3)_c, SU(2)_L, U(1)_Y
  generators (lam3, lam8, Tx, Ty, Tz, Y — same recipe, re-derived from the
  same Witt-pair creation/annihilation operators, not copied as numbers),
  extended trivially to H_F as `a -> a (x) I_3`. All verified Hermitian;
  su(2)_L closure ([Tx,Ty]=iTz) checked on the full 96-dim extension, not
  just the 32-dim factor.

## What is still abstract vs. explicitly implemented

- **Explicitly implemented:** Cl(10) factor, generation factor, SU(3)_f
  generators, SM gauge generators, their extension to H_F.
- **Still abstract:** the literal 16-vs-16bar chiral projection combined
  with an explicit embedding of the {10, 120, 126} Higgs-channel
  intertwiner tensor. This project has never built a numerical Clebsch-
  Gordan tensor for 16(x)16(x)H — Phase X's Hom_G=1 result is a weight-
  table (Cartan/Dynkin) dimension count, not an explicit tensor with
  numerical entries. This remains open; see `RESULT_Z2_TASK4.md`.

## Orthonormality / representation-action checks

All pass exactly (see `tests/test_hilbert_space.py`): generation basis
orthonormal, SU(3)_f generators Hermitian/traceless/closing, SM generators
Hermitian on both the 32-dim factor and its 96-dim extension, su(2)_L
algebra closure holds on H_F.
