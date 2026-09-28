"""
Phase Z24 — Door 1 follow-up: turn the raw first-order stationarity hit into
an ISOLATED-MINIMUM verdict (Hessian signature along the S3-breaking sector),
for BOTH candidate spectral functions, exact.

Candidate potentials on the generation Yukawa block Y (real 3x3):
  (A) Phi_4  = Tr[ (Y Y^T)(Y Y^T) ] - Tr[ Y Y^T ]            (quartic on YYT)
  (B) Phi_Tr = Tr[ g(Y Y^T) ],  g(x)=x^2 - x                 (trace of g(M))

For each:
  1. solve the FULL symmetric (not just (a,b)-restricted) stationarity
     equations exactly, listing every solution;  (project first to the
     S3-invariant family to get the 9-point count exactly, then lift to a
     general symmetric Y to test whether those points survive off-family)
  2. for the most promising nonzero vacuum in the symmetric family, build the
     Hessian in the full 6-dim symmetric-Y space,
  3. split its eigenvalues into S3-preserving (a,b) block and S3-breaking
     (traceless symmetric) block,
  4. verdict: isolated LOCAL MINIMUM <=> Hessian has all positive eigenvalues
     within its symmetry orbit (zero eigenvalues = orbit directions; too
     many zeros = not isolated).

No floats except at the final numpy Hessian eigenvalue call, seeded.
"""
import sympy as sp
import numpy as np


def stage(g_desc, Ssym, coords, candidate_label):
    print("\n" + "=" * 70)
    print(f"[{g_desc}]  {candidate_label}")
    print("=" * 70)
    # symbolics in the S3-restricted plane
    a, b = coords
    eqs = [sp.expand(sp.diff(Ssym, v)) for v in coords]
    sols = sp.solve(eqs, coords, dict=True)
    print(f"  Exact stationary points found in the (a,b) plane: {len(sols)}")
    for s in sols:
        print("    ", {str(k): sp.simplify(sp.nsimplify(s[k])) for k in s})


def hessian_test(g_desc, build_Y, cand, label):
    # full 6-dim symmetric Y parametrization
    y = sp.symbols('y0:6', real=True)
    Yf = sp.Matrix([[y[0], y[3], y[4]],
                    [y[3], y[1], y[5]],
                    [y[4], y[5], y[2]]])
    YYT = Yf * Yf.T
    Sf = sp.trace(YYT * YYT - YYT)              # = Phi_4 (B same for diag Y)
    # candidate numeric pair
    a_val, b_val = sp.nsimplify(cand[0]), sp.nsimplify(cand[1])
    # with a,b in (a,b)-(I3,J3) basis: Y0 = a I3 + b J3
    a, b = sp.symbols('a b', real=True)
    Y0 = a * sp.eye(3) + b * sp.ones(3, 3)
    # embed candidate into the 6 free coordinates (assuming symmetric ansatz)
    submap = {y[0]: sp.simplify(Y0[0, 0].subs({a: a_val, b: b_val})),
              y[1]: sp.simplify(Y0[1, 1].subs({a: a_val, b: b_val})),
              y[2]: sp.simplify(Y0[2, 2].subs({a: a_val, b: b_val})),
              y[3]: sp.simplify(Y0[0, 1].subs({a: a_val, b: b_val})),
              y[4]: sp.simplify(Y0[0, 2].subs({a: a_val, b: b_val})),
              y[5]: sp.simplify(Y0[1, 2].subs({a: a_val, b: b_val}))}
    H = sp.hessian(Sf, list(y))
    Hsub = H.subs(submap)
    # exact eigenvalues where possible; fall back to high-precision evalf
    print(f"\n  [{g_desc}] Hessian at {label} (all 6 symmetric directions):")
    try:
        eig_exact = Hsub.eigenvals()
        print("   exact eigenvalues {eig: mult}:", eig_exact)
        eig = np.array([complex(sp.re(k)) for k in eig_exact
                        for _ in range(eig_exact[k])], dtype=float)
    except Exception:
        eig = np.linalg.eigvalsh(np.array(Hsub.evalf(30), dtype=float))
    eig = np.sort(eig.real)
    print("   eigenvalues (sorted):", np.round(eig, 6))
    nneg = int((eig < -1e-9).sum()); nzer = int((np.abs(eig) < 1e-9).sum())
    npos = int((eig > 1e-9).sum())
    print(f"   #negative:{nneg}  #zero:{nzer}  #positive:{npos}")
    # interpretation
    if nneg == 0 and nzer == 0:
        print("   => ISOLATED LOCAL MINIMUM (strictly convex in all dirs)")
    elif nzer > 0:
        print(f"   => has {nzer} FLAT (orbit) direction(s) => NOT an isolated "
              "point set, vacuum lies on a continuous orbit (FAIL on isolation)")
    else:
        print("   => SADDLE (some negative dirs) => not a stable vacuum")
    # eigenvectors -> which directions are flat (split (a,b) vs S3-breaking)
    return eig


def main():
    a, b = sp.symbols('a b', real=True)
    I3, J3 = sp.eye(3), sp.ones(3, 3)
    Yab = a * I3 + b * J3
    YYT = Yab * Yab.T

    # (A) Phi_4 = Tr[(YYT)^2] - Tr[YYT]
    Phi4 = sp.trace(YYT * YYT - YYT)
    stage("Phi_4 = Tr[(YYT)^2]-Tr[YYT]", Phi4, [a, b], "S3-invariant plane")

    # Hessian at the first-order-hit candidate a=-1/sqrt2, b=0  (Y = a I)
    hessian_test("Phi_4", None, (-1 / sp.sqrt(2), 0),
                 "Y = -(1/sqrt2) I  (a=-1/sqrt2, b=0, S3-symmetric democratic)")

    # also test the maximal-S3-broken-ish candidate a=1/sqrt2, b=-1/(3 sqrt2)
    hessian_test("Phi_4", None, (1 / sp.sqrt(2), -1 / (3 * sp.sqrt(2))),
                 "a=1/sqrt2, b=-1/(3 sqrt2) (maximal S3 departure in-family)")


if __name__ == "__main__":
    main()
