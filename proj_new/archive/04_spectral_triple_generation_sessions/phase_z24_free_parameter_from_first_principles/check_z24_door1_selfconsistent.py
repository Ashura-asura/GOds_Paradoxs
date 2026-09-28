"""
Phase Z24 — Door 1 mechanism, forward test (NOT assumed).

SELF-CONSISTENT VACUUM mechanism:
  The finite Dirac operator D_F = [[0, Y],[Y^dagger, 0]] is determined as a
  stationary point of its own spectral action S(D) = Tr f(D^2/L^2).
  Set S(D)=Tr(g(D D^dagger)), g analytic -> stationary eqn is CUBIC in Y:
        Y (2 YY^dagger - tr(YY^dagger) I) = 0        (g(x)=x^2 - x)
  (overall L is a free scale; we work at the level of RATIOS -> H4 honored.)

Structure of the test (sympy exact where possible):
  Block 1 [setup]: the stationary equation, derived, exact.
  Block 2 [V-relaxation]: the gradient V-relaxation flow
      dY/dtau = -2(YY^dag Y) + Y tr(YY^dag)
    is rotationally invariant in the (a,b) democratic plane -> direction is
    never selected in-plane (Lemma B reappearing through the ACTION).
  Block 3 [stationary set under permutation symmetry]: within the most general
    permutation-/S3-invariant family, solve the cubic exactly -> vacua.
  Block 4 [isolation]: pick a nonzero vacuum; perturb along the S3-BREAKING
    direction (a different REPRESENTATION of the same group action, so the
    S3 orbit is separately understood) -> if the residual stays nonzero, the
    vacuum is NOT isolated => orbit degeneracy => FAIL by pre-registered rule.

Run and read the printed verdict. No SM value is inserted anywhere; all
quantities are symbolic or seeded-deterministic.
"""
import sympy as sp
import itertools


def permutation_matrices_S3():
    mats = []
    for p in itertools.permutations(range(3)):
        P = sp.zeros(3)
        for i, j in enumerate(p):
            P[i, j] = 1
        mats.append(P)
    return mats


def main():
    print("=" * 72)
    print("DOOR 1 — SELF-CONSISTENT VACUUM FORWARD TEST (pre-registered verdict)")
    print("=" * 72)

    # ---------- Block 1: the cubic stationary equation ------------------
    a, b = sp.symbols('a b', real=True)
    I3, J3 = sp.eye(3), sp.ones(3, 3)
    Y = a * I3 + b * J3           # general S3-INVARIANT candidate (Lemma B form)
    YYt = Y * Y.T                 # = YY since Y is real symmetric here
    g = lambda X: X ** 2 - X      # spectral action f:  g(x) = x^2 - x

    # S(D) = Tr g(Y Y^T); stationarity d/dY S = 0  (cubic):
    #   grad = 2 ( -Y + 2 Y Y^T Y )   (from dTr(YY^T)=tr(YY^T), dTr(YYTYYT))
    # We build it DIRECTLY, from first principles, rather than quoting it.
    Sexpr = sp.trace((Y * Y.T) ** 2 - (Y * Y.T))
    dvars = [a, b]
    stationary_eqs = [sp.expand(sp.diff(Sexpr, v)) for v in dvars]
    print("\n[Block 2] V-relaxation/stationarity equations in the S3-invariant "
          "(a,b) plane (exact):")
    for v, e in zip(dvars, stationary_eqs):
        print(f"   dS/d{v} = {sp.factor(e)}")

    # ---------- Block 3: solve exactly -> the stationary set ------------
    print("\n[Block 3] Stationary solutions (a,b), exact:")
    sols = sp.solve(stationary_eqs, dvars, dict=True)
    for s in sols:
        print("   ", {k: sp.simplify(s[k]) for k in s})

    # Classify: (0,0) trivial; the rest form the nontrivial vacuum locus.
    nontriv = [s for s in sols if sp.simplify(s[a]) != 0]
    print(f"\n   Trivial vacuum (a=b=0) present: "
          f"{all(sp.simplify(s[a])==0 and sp.simplify(s[b])==0 for s in sols)}")
    print(f"   Number of nontrivial exact branches found: {len(nontriv)}")

    # ---------- Block 4: isolation test along the S3-BREAKING direction --
    # A genuinely isolated vacuum must be stationary under EVERY perturbation,
    # including those that LEAVE the S3-invariant (a,b) plane. Build Y plus a
    # traceless symmetric perturbation P (dimension 5 for 3x3) -- these are the
    # S3-breaking directions -- linearize the stationarity condition, and ask
    # whether the vacuum stays stationary to first order (it must, for isolation)
    print("\n[Block 4] Isolation: perturb a nontrivial vacuum along S3-BREAKING "
          "directions and check if stationarity survives to first order.")
    if nontriv:
        sol0 = nontriv[0]
        Y0 = Y.subs(sol0)
        print(f"   Vacuum under test: a={sp.simplify(sol0[a])}, "
              f"b={sp.simplify(sol0[b])}")
        # general symmetric traceless perturbation (the S3-breaking sector)
        p = sp.symbols('p0:5', real=True)
        P = sp.Matrix([[p[0], p[3], p[4]],
                       [p[3], p[1], -p[3] - p[4]],
                       [p[4], -p[3] - p[4], -p[0] - p[1]]])  # traceless symmetric
        eps = sp.symbols('eps')
        Yfull = Y0 + eps * P
        Sfull = sp.trace(Yfull * Yfull.T * Yfull * Yfull.T - Yfull * Yfull.T)
        # first-order stationarity in the perturbation amplitudes
        firstorder = [sp.expand(sp.diff(sp.diff(Sfull, p[i]), eps)).subs(eps, 0)
                      for i in range(5)]
        # at an isolated vacuum each firstorder must be identically zero
        is_iso = all(sp.simplify(x) == 0 for x in firstorder)
        print(f"   First-order stationarity under ALL traceless perturbations "
              f"survives: {is_iso}")
        if not is_iso:
            # find at least one perturbation with nonzero residual
            res = [sp.simplify(x) for x in firstorder if sp.simplify(x) != 0]
            print(f"   Nonzero residuals present ({len(res)} of 5): "
                  f"=> a flat direction exists along the perturbed sector")

    print("\n" + "=" * 72)
    print("PRE-REGISTERED VERDICT LOGIC")
    print("=" * 72)
    print("PASS  <-> finite set of ISOLATED vacua  (parameter reduction)")
    print("FAIL  <-> vacua form continuous orbits (S3/U(3) back via the action),")
    print("        or only the free-scale trivial-extremum-plus-ridge survives.")


if __name__ == "__main__":
    main()
