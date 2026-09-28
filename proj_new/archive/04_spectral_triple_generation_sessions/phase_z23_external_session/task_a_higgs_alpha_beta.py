"""
Task A (Z23 external session) -- classify the symmetry-breaking Higgs
directions H_alpha, H_beta of the Gresnigt Cl(10)+S3 construction
(arXiv:2604.24795, Section 4.3, eq. 122-123; its M_a Yukawa matrices,
Section 5.2, eq. 138-141).

Question (master prompt Task A): does using the "orthogonal orbit"
directions H_alpha = H^(1) - (1/2)(H^(2)+H^(3)) and
H_beta = (sqrt(3)/2)(H^(2)-H^(3)) INSTEAD of the cyclically averaged
Hbar = (H^(1)+H^(2)+H^(3))/3 produce a Yukawa texture that is

  (a) forced into some other rigid, non-arbitrary pattern (new L1
      result), or
  (b) merely a relocation of the same continuous freedom (the Rule 9 /
      Rule 2 failure mode), or
  (c) genuinely constrained by E8-side structure (which would require
      E8 to select a direction in the (H_alpha,H_beta) 2-plane).

Method: reuse the verified Phase Z22 machinery (phase_z22_gresnigt_import)
for Cl(8)/Cl(10), psi_3 as inner automorphism U10, and the three
generation subspaces; build the four first-generation Higgs components
(eq. 72), their psi_3-images, H_alpha/H_beta, and the generation-space
Yukawa matrices via the Hilbert-Schmidt pairing Y(X_L,H,X_R) =
Tr((X_L H)^dag X_R) (eq. 76). Verify M_1, M_2, M_3 against the paper's
eq. 139 (this is an independent reproduction, not a citation). Then
compute M_alpha, M_beta, Mbar directly (and via linearity, as a
cross-check), their eigenvalues, the rank of the texture family, and
the exact count of remaining real degrees of freedom.

Nothing here is fitted. Every number is a direct computation from the
stated algebraic construction.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'phase_z22_gresnigt_import'))

from gresnigt_algebra import build_cl8_generators, build_witt, build_omega8
from gresnigt_generations import (
    build_cl10_generators, build_witt5, build_idempotents_cl8,
    build_idempotents_cl10, build_psi3_images)
from gresnigt_step3 import solve_psi3_inner_automorphism

N8 = 16
N10 = 32


def hs_inner(A, B):
    return np.trace(A.conj().T @ B)


def yukawa(XL, H, XR):
    """eq. (76): Y(X_L, H, X_R) = Tr((X_L H)^dag X_R)."""
    return np.trace((XL @ H).conj().T @ XR)


def main():
    E8 = build_cl8_generators()
    a4, ad4 = build_witt(E8)
    w8 = build_omega8(E8)
    idem8 = build_idempotents_cl8(a4, ad4)
    E10 = build_cl10_generators(E8, w8)
    a5, ad5 = build_witt5(E10)
    idem10 = build_idempotents_cl10(idem8, a5, ad5)

    # psi_3 as inner automorphism: solve for U8 (recomputed here, not loaded
    # from the .npy, so this script is self-contained), extend to Cl(10).
    psi3_e8 = build_psi3_images(E8)
    U8, singvals, n_null = solve_psi3_inner_automorphism(E8, psi3_e8)
    max_err = max(np.max(np.abs(U8 @ E8[a] - psi3_e8[a] @ U8)) for a in range(8))
    U10 = np.kron(np.eye(2, dtype=complex), U8)
    U10inv = U10.conj().T

    def psi3(M):
        return U10 @ M @ U10inv

    def psi3_sq(M):
        return psi3(psi3(M))

    print(f"[Setup] U8 recomputed: direct defining eq max err = {max_err:.3e} "
          f"(machine precision => U10 is the verified psi_3 intertwiner)")

    # ---- Higgs components, eq. (72) ----
    f9 = idem10['+++-+']     # f_{+++-+} = E_{9,9}
    f25 = idem10['+++--']    # f_{+++--} = E_{25,25}
    # Cl(10)-embedded Witt pairs (32x32), exactly as in step4_gram.py
    a10 = [np.kron(np.eye(2, dtype=complex), ai) for ai in a4] + [a5]
    ad10 = [np.kron(np.eye(2, dtype=complex), adi) for adi in ad4] + [ad5]
    a4c = a10[3]
    a5c = a10[4]
    ad5c = ad10[4]

    Hd0_1 = a4c @ ad5c @ f9    # H_d^0
    Hdm_1 = a4c @ f9           # H_d^-
    Hup_1 = a4c @ f25          # H_u^+
    Hu0_1 = a4c @ a5c @ f25    # H_u^0

    # eq. (73): matrix-unit check -- build matrix units explicitly (np.eye
    # indexing returns scalars, NOT matrices!)
    def munit(i, j):
        M = np.zeros((N10, N10), dtype=complex)
        M[i, j] = 1.0
        return M

    checks = {
        "H_d^0": (Hd0_1, -munit(16, 8)),   # -E_{17,9} (0-indexed 16,8)
        "H_d^-": (Hdm_1, 1j * munit(0, 8)),   # i E_{1,9}
        "H_u^+": (Hup_1, 1j * munit(16, 24)),  # i E_{17,25}
        "H_u^0": (Hu0_1, munit(0, 24)),        # E_{1,25}
    }
    print("\n=== Step 1: first-generation Higgs components vs paper eq. (73) ===")
    for name, (H, target) in checks.items():
        err = np.max(np.abs(H - target))
        # report the actual support: which matrix unit does H equal?
        nz = np.argwhere(np.abs(H) > 1e-9)
        support = [(int(i), int(j)) for i, j in nz]
        print(f"  {name}: max |H - paper matrix unit| = {err:.3e}; "
              f"support = {support}")
        if support:
            i, j = support[0]
            print(f"         H = {H[i, j]:.6f} * E_[{i + 1},{j + 1}] (+possibly others: "
                  f"{len(support)} entries)")

    # ---- psi_3 orbit of each component: H^(1), H^(2), H^(3) ----
    print("\n=== Step 2: psi_3 orbits of the four Higgs components ===")
    orbits = {}
    for name, H1 in (("Hd0", Hd0_1), ("Hdm", Hdm_1), ("Hup", Hup_1), ("Hu0", Hu0_1)):
        H2, H3 = psi3(H1), psi3_sq(H1)
        # orbit length check: psi_3^3 = Id on each Higgs component
        err3 = np.max(np.abs(psi3(H3) - H1))
        # linear independence of the three copies (as 32x32 matrices)
        S = np.stack([H1.flatten(), H2.flatten(), H3.flatten()])
        rank = np.linalg.matrix_rank(S, tol=1e-9)
        print(f"  {name}: psi_3^3 back to H^(1) err = {err3:.3e}, "
              f"rank of [H^(1),H^(2),H^(3)] = {rank} (expect 3)")
        orbits[name] = (H1, H2, H3)

    # ---- H_alpha, H_beta per component, eq. (122)-(123) ----
    print("\n=== Step 3: H_alpha, H_beta (eq. 122-123) ===")
    sqrt3 = np.sqrt(3.0)
    ortho = {}
    for name, (H1, H2, H3) in orbits.items():
        H_alpha = H1 - 0.5 * (H2 + H3)
        H_beta = (sqrt3 / 2.0) * (H2 - H3)
        ortho[name] = (H_alpha, H_beta)
        # HS orthogonality of the three directions Hbar, H_alpha, H_beta
        Hbar = (H1 + H2 + H3) / 3.0
        g = np.array([[hs_inner(x, y).real for y in (Hbar, H_alpha, H_beta)]
                      for x in (Hbar, H_alpha, H_beta)])
        print(f"  {name}: Gram of (Hbar, H_alpha, H_beta):")
        print("    " + str(np.round(g, 6).tolist()))

    # ---- Generation-space Yukawa matrices, eq. (138) ----
    # d-channel: u_L,r -> d_R,s via H_d^- (down-type), r,s = generation
    # (colour index fixed to i=j=1; delta_ij is colour conservation,
    #  verified below by computing a second colour and checking identity)
    print("\n=== Step 4: generation-space Yukawa matrices M_1, M_2, M_3 ===")
    fp = idem10['+++++']
    fpp = idem10['+++-+']

    uL1 = ad10[0] @ ad10[3] @ fp     # u_L, colour 1, generation 1 (eq. 24/40)
    dR1 = ad10[0] @ fpp              # d_R, colour 1, generation 1 (eq. 51)

    def generation_copy(state, g):
        out = state
        for _ in range(g):
            out = psi3(out)
        return out

    uL = [generation_copy(uL1, g) for g in range(3)]
    dR = [generation_copy(dR1, g) for g in range(3)]

    # verify the colour-diagonal structure delta_ij: repeat with colour 2
    uL_c2 = ad10[1] @ ad10[3] @ fp
    dR_c2 = ad10[1] @ fpp
    uL2c = [generation_copy(uL_c2, g) for g in range(3)]
    dR2c = [generation_copy(dR_c2, g) for g in range(3)]

    Hdm_orbit = orbits["Hdm"]  # (H_d^-(1), H_d^-(2), H_d^-(3))
    M_a = []
    for a, Ha in enumerate(Hdm_orbit):
        M = np.zeros((3, 3), dtype=complex)
        for r in range(3):
            for s in range(3):
                M[r, s] = yukawa(uL[r], Ha, dR[s])
        M_a.append(M)

    print("  M_1 =")
    print(np.round(M_a[0], 6))
    print("  M_2 =")
    print(np.round(M_a[1], 6))
    print("  M_3 =")
    print(np.round(M_a[2], 6))

    # paper's eq. (139):
    paper_M1 = np.array([[1, 1 / 4, 1 / 4],
                         [1 / 4, 1 / 4, -1 / 8],
                         [1 / 4, -1 / 8, 1 / 4]])
    paper_M2 = np.array([[1 / 4, 1 / 4, -1 / 8],
                         [1 / 4, 1, 1 / 4],
                         [-1 / 8, 1 / 4, 1 / 4]])
    paper_M3 = np.array([[1 / 4, -1 / 8, 1 / 4],
                         [-1 / 8, 1 / 4, 1 / 4],
                         [1 / 4, 1 / 4, 1]])
    for a, (M, pM) in enumerate(zip(M_a, (paper_M1, paper_M2, paper_M3))):
        print(f"  M_{a+1} vs paper eq. 139: max err = "
              f"{np.max(np.abs(M - pM)):.3e}")

    # colour-diagonal check (delta_ij in eq. 138)
    M_c2 = np.zeros((3, 3), dtype=complex)
    for r in range(3):
        for s in range(3):
            M_c2[r, s] = yukawa(uL2c[r], Hdm_orbit[0], dR2c[s])
    print(f"  colour-2 M_1 vs colour-1 M_1: max diff = "
          f"{np.max(np.abs(M_c2 - M_a[0])):.3e} (delta_ij colour structure)")

    # ---- Mbar, M_alpha, M_beta ----
    print("\n=== Step 5: Mbar, M_alpha, M_beta ===")
    Mbar = (M_a[0] + M_a[1] + M_a[2]) / 3.0
    # direct computation with H_alpha / H_beta matrices:
    Ha_alpha, Ha_beta = ortho["Hdm"]
    M_alpha_dir = np.zeros((3, 3), dtype=complex)
    M_beta_dir = np.zeros((3, 3), dtype=complex)
    for r in range(3):
        for s in range(3):
            M_alpha_dir[r, s] = yukawa(uL[r], Ha_alpha, dR[s])
            M_beta_dir[r, s] = yukawa(uL[r], Ha_beta, dR[s])
    # via linearity from M_1, M_2, M_3:
    M_alpha_lin = M_a[0] - 0.5 * (M_a[1] + M_a[2])
    M_beta_lin = (sqrt3 / 2.0) * (M_a[1] - M_a[2])

    print("  Mbar =")
    print(np.round(Mbar, 6))
    print(f"  Mbar vs paper eq. 141: max err = "
          f"{np.max(np.abs(Mbar - np.array([[1/2, 1/8, 1/8],
                                             [1/8, 1/2, 1/8],
                                             [1/8, 1/8, 1/2]]))):.3e}")
    print("  M_alpha (direct) =")
    print(np.round(M_alpha_dir, 6))
    print(f"  M_alpha direct vs linearity cross-check: max err = "
          f"{np.max(np.abs(M_alpha_dir - M_alpha_lin)):.3e}")
    print("  M_beta (direct) =")
    print(np.round(M_beta_dir, 6))
    print(f"  M_beta direct vs linearity cross-check: max err = "
          f"{np.max(np.abs(M_beta_dir - M_beta_lin)):.3e}")

    for name, M in (("Mbar", Mbar), ("M_alpha", M_alpha_dir),
                    ("M_beta", M_beta_dir)):
        ev = np.linalg.eigvalsh(M.real)
        print(f"  {name} eigenvalues: {np.round(ev, 6)}")

    # ---- Degree-of-freedom analysis ----
    print("\n=== Step 6: DOF analysis of the texture family ===")
    # The full family-resolved texture: M(c) = c1 M_1 + c2 M_2 + c3 M_3,
    # c_a in C. Dimension of the span over C:
    S = np.stack([Ma.flatten() for Ma in M_a])
    rank_C = np.linalg.matrix_rank(S, tol=1e-9)
    print(f"  rank of {M_a} (9-dim vectors) over C: {rank_C} "
          f"-> full texture family is {rank_C}-complex-dimensional "
          f"({2 * rank_C} real DOF)")

    # subfamily reachable from (H_alpha, H_beta) alone:
    S_ab = np.stack([M_alpha_dir.flatten(), M_beta_dir.flatten()])
    rank_ab = np.linalg.matrix_rank(S_ab, tol=1e-9)
    print(f"  rank of (M_alpha, M_beta): {rank_ab} -> {rank_ab}-complex-dim "
          f"({2 * rank_ab} real DOF) if only alpha/beta VEVs are allowed")

    # is Mbar in the span of M_alpha, M_beta? (i.e. is the averaged point
    # reachable from the orthogonal directions alone?)
    AB = np.stack([M_alpha_dir.flatten(), M_beta_dir.flatten()]).T
    coef = np.linalg.lstsq(AB, Mbar.flatten(), rcond=None)
    resid = np.max(np.abs(AB @ coef[0] - Mbar.flatten()))
    print(f"  Mbar in span(M_alpha, M_beta)? residual = {resid:.3e} "
          f"({'YES (averaged limit reachable from orthogonal dirs alone)'
             if resid < 1e-9 else 'NO'})")

    # ---- psi_3 transformation of (H_alpha, H_beta), eq. "rotation by 2pi/3" ----
    print("\n=== Step 7: psi_3 action on (H_alpha, H_beta) ===")
    for name, (Ha, Hb) in ortho.items():
        psi_Ha = psi3(Ha)
        psi_Hb = psi3(Hb)
        err_a = np.max(np.abs(psi_Ha - (-0.5 * Ha + (sqrt3 / 2.0) * Hb)))
        err_b = np.max(np.abs(psi_Hb - (-(sqrt3 / 2.0) * Ha - 0.5 * Hb)))
        print(f"  {name}: psi_3(H_alpha) == -1/2 H_alpha + sqrt3/2 H_beta? "
              f"err = {err_a:.3e};  psi_3(H_beta) == -sqrt3/2 H_alpha "
              f"- 1/2 H_beta? err = {err_b:.3e}")

    # ---- Sector independence: repeat for H_u^0 (up-type, neutral) ----
    # u_R lives in U_1^+ : u_R^(i) = a_i^dag a_5 f_{+++--} (eq. 27 sector)
    print("\n=== Step 8: up-type channel (H_u^0) ===")
    uR1 = ad10[0] @ a5c @ f25     # u_R, colour 1, generation 1
    uR = [generation_copy(uR1, g) for g in range(3)]
    Hu0_orbit = orbits["Hu0"]
    M_u = np.zeros((3, 3), dtype=complex)
    for r in range(3):
        for s in range(3):
            M_u[r, s] = yukawa(uL[r], Hu0_orbit[0], uR[s])
    print("  M_u (first copy of H_u^0, colour-1 channels):")
    print(np.round(M_u, 6))
    # paper's claim: same S3-invariant texture in all allowed sectors
    # "up to overall sign conventions determined by the algebraic representatives"
    diff_m1 = np.max(np.abs(M_u - M_a[0]))
    diff_m1neg = np.max(np.abs(M_u + M_a[0]))
    print(f"    max |M_u - M_1| = {diff_m1:.3e};  max |M_u + M_1| = {diff_m1neg:.3e}")
    for name, M in (("M_u/3", M_u / 3.0),):
        ev = np.linalg.eigvalsh(M.real)
        print(f"  {name} eigenvalues (texture should match Mbar's): "
              f"{np.round(ev, 6)}")

    # ---- summary: how many free real parameters does H_alpha/H_beta leave? ----
    print("\n=== Summary ===")
    print(f"Full family-resolved texture space: {2 * rank_C} real DOF "
          f"(3 complex coefficients c_1, c_2, c_3)")
    print(f"Orthogonal-direction-only texture space: {2 * rank_ab} real DOF")
    print(f"Averaged-limit texture: fixed point Mbar in that space "
          f"(imposed by hand, not derived)")
    print(f"E8 content of this construction: NONE (pure Cl(10)+S3); "
          f"E8-side selection question answered separately in result file")


if __name__ == "__main__":
    main()
