# AUDIT_Z2_INITIAL_STATE.md — 2026-07-28

Re-read (this session): `phase_a1_cl10_core.py`, `phase_a2_e8_core.py`
(the file named in the prompt as `phase_a2_e8_branching.py` does not
exist in the archive; `phase_a2_e8_core.py` is the file that plays that
role, confirmed by its docstring), `phase_x_hom_g_invariant_audit.py`,
`docs/POST_AUDIT_TARGET.md`, `docs/PHASE_Z_SPECTRAL_TRIPLE_RESULT.md`,
`docs/PHASE_Z1_SPECTRAL_TRIPLE_MODULI_RESULT.md`.

## 1. Hilbert space dimension
- Cl(10) factor: **32**, built as 5 Witt pairs on a Fock space (Phase
  A1). Confirmed by direct re-run of `build_cl10_gammas()`.
- Generation factor: **3**, from E8 → E6 × SU(3)_f, (16,3) piece of 248
  (Phase A2). Exists only at the root-system / branching level — no
  explicit 3-dimensional basis with basis vectors has been built as
  code anywhere in the repo.
- Full H_F (Task 1's target) = C³² ⊗ C³, dim 96: **not yet built as an
  explicit object**. This is real, not-yet-done work (see Task 1 result).

## 2. Existing Clifford basis
10 gamma matrices, 32×32, built from octonion left-multiplication
matrices (`support/qosc_division_connection.py`) via a Weyl-type
recipe. Re-verified this session: all 10 are anti-Hermitian with
γ_a² = −1 and {γ_a, γ_b} = 0 for a≠b (i.e. this is a representation of
the negative-definite real Clifford algebra Cl(0,10), not Cl(10,0) —
consistent with, not a contradiction of, Phase A1's own CAR
verification, which only checks {a_i,a_j†}=δ_ij and never asserts
Hermitian generators).

## 3. Existing SO(10)/E8 representations
SU(3)_c and SU(2)_L generators are built explicitly as bilinears in the
Witt creation/annihilation operators (Phase A1). No SO(10) generators
beyond this SM subgroup, and no explicit 248-dimensional E8 adjoint
action on H_F, exist as matrices anywhere in the repo — E8/E6 branching
is verified at the root/weight level (Phase A2, Phase X), not built as
an operator acting on the 32- or 96-dim Hilbert space.

## 4. Generation-index implementation
Not implemented as an explicit tensor factor (see item 1). Phase X's
6-or-3 count is a dimension count of Sym²(C³)/Λ²(C³) as abstract
vector spaces, not a computation done on explicit basis vectors.

## 5. Chirality operator Γ
**Did not exist before this session.** Now constructed (this session,
see `RESULT_Z2_TASK2.md`): Γ_F = i⁵γ₁···γ₁₀ on the 32-dim factor,
verified Γ_F²=1, Hermitian, anticommutes with all 10 gammas, splits
H_{Cl(10)} into 16+16, and coincides with the fermion-number-parity
operator (−1)^{N_tot} up to overall sign.

## 6. Reality operator J
**Did not exist before this session.** Now partially constructed (see
`RESULT_Z2_TASK3.md`): two inequivalent unitary intertwiners C survive
(giving J²=−1 or J²=+1), both compatible with Γ_F but not yet
disambiguated by a KO-dimension pinned from D_F, which doesn't exist
yet.

## 7. Finite Dirac operator D_F
**Does not exist.** No matrix, block structure, or Yukawa parametrization
has been built anywhere in the repo. Phase X computed the *dimension*
of the space such couplings would live in (6 or 3, as an abstract
Hom_G count) without ever constructing an explicit D_F matrix.

## Missing objects (in order needed for Tasks 1–6)
1. Explicit 3-dim generation basis + explicit SU(3)_f generator matrices
   acting on it (needed before H_F can be built as a concrete 96-dim
   space with a verifiable inner product and gauge action).
2. Explicit SO(10) (not just SM subgroup) generator matrices on the
   32-dim Cl(10) factor, if "gauge covariance under the parent
   Cl(10)×E8 structure" (Task 5) is meant literally rather than just
   SU(3)_c×SU(2)_L×U(1)_Y.
3. KO-dimension selection criterion to pick between the two J_F
   candidates found this session (see Task 3 result) — this is a real
   open mathematical question, not a missing library.
4. An explicit basis for the 10/126/120 representations' Hom_G
   generators (Phase X computed dimensions, not the actual invariant
   tensors/Clebsch coefficients) — needed to write D_F's off-diagonal
   block explicitly rather than just count its dimension.

## Blockers / risk flags
- Building full SO(10) (45 generators) or E8 (248 generators) as
  explicit matrices on a 32- or 96-dim space and solving the order-one
  condition as a literal 96×96 linear system is a large but *tractable*
  computation — no missing library, just substantial remaining work
  (estimate: several more focused sessions' worth, consistent with what
  Phase Z1 already flagged).
- The KO-dimension ambiguity found in Task 3 (two consistent sign
  patterns, matching mod-8 dimensions 2 and 6) cannot be resolved from
  Γ_F and Clifford data alone — Connes' own table requires the ε′
  relation `JD_F = ε′D_F J`, which needs an actual D_F. This is flagged
  now rather than glossed over, per Rule 9 / the Task 8 discrimination
  test.
