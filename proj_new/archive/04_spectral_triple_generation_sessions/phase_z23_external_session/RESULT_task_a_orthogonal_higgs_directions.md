# Phase Z23, Task A — Symmetric vs. orthogonal Higgs directions in
# Gresnigt's Cl(10)+S3 model: the degeneracy-lifting subspace is real,
# irreducible under S3, and does NOT contain the symmetric VEV

**Status: closed, L1. The paper's own escape hatch (H_alpha, H_beta,
VEVs in the directions orthogonal to the cyclic average) is fully
characterized: exact spectra (0, +/-9 sqrt(2)/16), a 4-real-DOF texture
family, irreducible 120-degree S3 action on the plane — and the crucial
negative result that the symmetric fixed point Mbar is NOT reachable
from this subspace. Does not reduce the free-parameter count; adds a
free VEV-direction angle instead.**

## What this phase tested

Z22 closed the general question "does an order-3/S3 generation mechanism
escape the 2:1:1 degeneracy" negatively, but explicitly left untested
Gresnigt's own set-aside direction (paper Section 4.3, "additional
S3-breaking effects, or vacuum expectation values in the orthogonal
Higgs directions, are needed to lift the degeneracy"): the un-averaged,
family-resolved orbit combinations

    H_alpha := H^(1) - 1/2 (H^(2) + H^(3)),   H_beta := (sqrt3/2)(H^(2) - H^(3))

of each of the four electroweak Higgs components (H_d^0, H_d^-,
H_u^+, H_u^0), and the corresponding generation-space Yukawa textures
M_alpha, M_beta (the paper's eq. 122-123 in Higgs space, extended here
to texture space). This phase tests whether those directions lift the
Z22 degeneracy and what freedom they contain.

## Method — independent computation, both direct and cross-checked

Per Rule 4 (adversarial audit always on):

1. Rebuilt the entire Cl(8)/Cl(10) machinery from scratch (same code
   base as Z22, verified exact there): generators, Witt bases, psi_3
   solved as an inner automorphism (Skolem-Noether), U10 = I_2 (x) U8.
   Direct defining equation max err 9.4e-16.
2. Higgs components per the paper's eq. (72): H_d^0 = a_4 a_5^+ f_(+++-+),
   H_d^- = a_4 f_(+++-+), H_u^+ = a_4 f_(+++--), H_u^0 = a_4 a_5 f_(+++--).
3. **Matrix-unit check vs. the paper's eq. (73): all four match EXACTLY
   (0.000e+00)** — H_d^0 = -E_{17,9}, H_d^- = i E_{1,9}, H_u^+ = i E_{17,25},
   H_u^0 = E_{1,25} (1-indexed), verified from the actual nonzero support
   of each 32x32 matrix, not from a pre-assumed entry position.
   [Audit note: an initial run reported err = 1.000 for all four; this
   was a BUG IN OUR CHECK, not a mismatch — `np.eye` scalar indexing
   (`E[16,8]`) returns 0.0, not the matrix unit E_{17,9}. Fixed by
   building matrix units explicitly. The paper was right all along.]
4. Each component's psi_3 orbit (H^(1), H^(2), H^(3)): psi_3^3 = Id
   exactly (4.4e-16) and the three copies are linearly independent
   (rank 3) for all four components.
5. H_alpha, H_beta built per eq. 122-123; Gram matrix (Hilbert-Schmidt)
   of (Hbar, H_alpha, H_beta) computed for every component.
6. Generation-space textures via the paper's Yukawa trace pairing
   eq. (138), Y(X_L, H, X_R) = Tr((X_L H)^+ X_R), for u_L, d_R colour-1
   states and, in Step 8, the up-type channel u_L -> u_R with H_u^0
   (u_R^(i) = a_i^+ a_5 f_(+++--), the U_1^+ sector of eq. 27).
   Every matrix computed BOTH directly from the definitions AND from
   linear combinations of the directly-computed M_1, M_2, M_3 — the two
   independent routes agree to machine precision (1.1e-16 / 2.2e-16).
7. All eigenvalue claims verified symbolically (sympy), not fitted.

## Result 1 — the paper's M matrices are reproduced exactly

- M_1, M_2, M_3 (eq. 139) reproduced exactly: max err 1.7e-16,
  1.1e-15, 1.3e-15. Colour structure diagonal (delta_ij): colour-2
  texture = colour-1 texture to 6.9e-16.
- Mbar = (M_1+M_2+M_3)/3 = 3/8 I + 1/8 J (eq. 141), max err 5.6e-16;
  exact eigenvalues (3/4, 3/8, 3/8).
- Up-type sector (Step 8): M_u from (u_L, H_u^0, u_R) = M_1 EXACTLY
  (0.000e+00) — sector independence confirmed; here even stronger than
  the paper's "up to overall sign conventions" (no sign flip in our
  convention).

## Result 2 — the orthogonal directions: exact spectra and Gram

- Gram matrix of (Hbar, H_alpha, H_beta) = diag(1/2, 9/8, 9/8) for ALL
  four Higgs components: H_alpha and H_beta are mutually
  Hilbert-Schmidt-orthogonal and both orthogonal to Hbar, with equal
  norms sqrt(9/8). The orthogonal directions are an honest orthonormal
  (up to scale) basis of the 2-dim complement of Hbar inside each
  Higgs-orbit family.
- Generation textures: both M_alpha and M_beta have exact spectrum
  (0, +9 sqrt(2)/16, -9 sqrt(2)/16) ~ (0, +0.7955, -0.7955), verified
  symbolically. Trace = 0 for both.
- psi_3 action on the (H_alpha, H_beta) plane (Step 7): exact 120-degree
  rotation,

      psi_3(H_alpha) = -1/2 H_alpha + (sqrt3/2) H_beta
      psi_3(H_beta)  = -(sqrt3/2) H_alpha - 1/2 H_beta

  (err 2.8e-16 / 5.6e-16, all four components). The plane carries the
  real 2-dimensional irreducible representation of S3 — irreducible, so
  it contains NO S3-invariant direction. This is representation theory
  (S3's 2d real irrep is the standard one), not numerics.

## Result 3 — the key negative result: Mbar is NOT in span(M_alpha, M_beta)

- Texture-space DOF analysis (Step 6): the family of matrices spanned by
  M_1, M_2, M_3 is 3-complex-dimensional (6 real DOF); the orthogonal
  subspace span(M_alpha, M_beta) is 2-complex-dimensional (4 real DOF).
- Projection check: residual of Mbar onto span(M_alpha, M_beta) = 0.5.
- Exact proof: Tr(Mbar) = 3/2, but Tr(M_alpha) = Tr(M_beta) = 0, so any
  linear combination of the orthogonal directions is trace-free and can
  never equal Mbar. Symbolic, no fitting.

**Consequence:** the "symmetric" limit Hbar — the direction whose
texture reproduces the 2:1:1 spectrum (3/4, 3/8, 3/8) that Z6-Z22 found
degenerate — is unreachable from the orthogonal subspace. A VEV purely
in (H_alpha, H_beta) gives a trace-free texture with exact eigenvalues
(0, +/-9 sqrt(2)/16): one massless generation and one mass of opposite
sign, NOT the near-degenerate hierarchy. Lifting the Z22 degeneracy
requires an S3-breaking VEV in the orthogonal plane, whose direction is
a free continuous parameter (rotated by psi_3), and which cannot
deform continuously into the symmetric point Mbar.

## What this does *not* close

- The (H_alpha, H_beta) plane is a genuine 2-real-dimensional moduli
  space of S3-breaking VEV directions, irreducible under the residual
  S3/psi_3 action. Nothing in the construction selects an angle in it:
  E8 plays NO role in this model (pure Cl(10)+S3; the paper has no E8
  machinery at all), so no E8-side selection mechanism exists to fix
  the VEV direction. This is an open parameter, not a derived one.
- Whether some OTHER combination of the 6-real-DOF family space (not
  just the trace-free 4-real-DOF subspace) could realize a
  near-degenerate-but-non-degenerate spectrum is untested; the paper
  proposes no such combination, and it would still leave the additional
  freedom unexplained rather than derived.
- The spectrum (0, +/-9 sqrt(2)/16) itself is not a mass-hierarchy
  prediction — it is the texture of the S3-breaking directions, shown
  here to be unable to reach the symmetric point.

## Rule 9 check

Non-numerological and falsifiable. Every quantity was computed two
independent ways (direct definition vs. linearity) and every eigenvalue
claim was verified symbolically with sympy: Mbar (3/4, 3/8, 3/8) exactly,
M_alpha/M_beta (0, +/-9 sqrt(2)/16) exactly, Tr(Mbar) = 3/2 vs trace-free
orthogonal matrices. If S3's 2d irrep were NOT the real standard one
(e.g. if psi_3 acted as a reflection rather than a 120-degree rotation),
Result 2's rotation matrix would have failed its check — it passed at
machine precision. The irreducibility of the (H_alpha,H_beta) plane is
the same fact that forces Mbar to be the unique S3-invariant direction
in each Higgs-orbit family, and the trace argument is a theorem, not a
fit.

## Net verdict

**Status remains 0/19.** Task A confirms the paper's own set-aside
mechanism exists (irreducible 4-real-DOF S3-breaking texture family,
exact spectra, exact 120-degree S3 action) and proves its limits: it
cannot reach the symmetric point, it introduces a free VEV-direction
angle rather than reducing parameters, and E8 provides no selection
mechanism in this construction. The paper's eq. (72), (73), (122),
(123), (138)-(141) are all independently reproduced exactly.

## Reproducibility

`session_new_files/phase_z23_external_session/`:
- `task_a_higgs_alpha_beta.py` — full Task A computation (self-contained:
  recomputes U8 via Skolem-Noether, rebuilds all Higgs components,
  orbits, Gram, textures, DOF analysis, sector-independence check)
- `task_a_full_output.txt` — full run output (all steps, exact errors)
- `task_a_step1_fixed.txt` — post-fix Step 1 matrix-unit verification
  (0.000e+00 for all four components)

Pure numpy + sympy (eigenvalue exactness only). No SM value inserted
anywhere. Depends on the verified Z22 import
`session_new_files/phase_z22_gresnigt_import/`.

## Source

N. Gresnigt, "Higgs and Yukawa Structure in a Clifford Algebra Model
with Three Generations and S3 Family Symmetry," arXiv:2604.24795v2
(2026), eqs. 72, 73, 116-123, 138-144, Section 4.3. Independently
reproduced and extended (texture-space analysis, exact spectra, trace
theorem), not cited without verification (Rule 4).
