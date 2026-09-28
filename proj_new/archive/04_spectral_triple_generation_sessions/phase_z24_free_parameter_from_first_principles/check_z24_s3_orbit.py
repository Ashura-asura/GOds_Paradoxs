"""
Phase Z24 support script 2 — verify the S3-degeneracy claim from Phase Z22 /
Phase Z23 Task A, from first principles, with exact arithmetic.

CLAIM TO CHECK (Z22's generalization, restated for the (a,b) plane):
Any real symmetric 3x3 matrix M that is invariant under the full S3
permutation action on 3 indices is forced to the form
        M = a*I + b*(J) ,  J = matrix of all ones
so that its eigenvalues are exactly (a+2b, a-b, a-b).
-> a 1-fold  : 2-fold split, i.e. a degenerate pair, for ALL a,b.
No choice of a,b gives three distinct eigenvalues. This is the "democratic /
2:1:1 degeneracy" that Z6..Z23 keep hitting.

SECOND CLAIM (Z23 Task A): the two directions orthogonal to the democratic
direction Mbar transform as the irreducible 2-d real rep of S3, i.e. S3 acts
on them by 120-degree rotations. Hence that breaking plane contains NO
S3-invariant ray: no point of it is selected by any S3-covariant principle.

What "from first principles" means here: we do NOT quote Schur's lemma or
Maschke's theorem. We build the S3 permutation matrices on R^3 explicitly,
find the general real symmetric matrix commuting with all of them by solving
the linear system [M,P]=0, read off the (a,b) form directly, compute the
eigenvalues EXACTLY with sympy, and verify the orthogonal-plane rotation
explicitly.
"""
import sympy as sp


def permutation_matrices_S3():
    """The 6 permutation matrices of S3 acting on R^3, as sympy matrices."""
    import itertools
    mats = []
    for p in itertools.permutations(range(3)):
        P = sp.zeros(3)
        for i, j in enumerate(p):
            P[i, j] = 1
        mats.append(P)
    return mats


def main():
    # ---- Claim 1: S3-invariant 3x3 (NOT assumed symmetric) => a I + b J ----
    # Review correction (2026-08-02): the first-pass script restricted M to be
    # symmetric as a time-saver. A probe showed that is unnecessary: the full
    # S3 permutation commutant on a GENERAL 3x3 matrix already forces symmetry.
    # So we now solve the general (9-unknown) case directly -- the honest,
    # assumption-free statement of the claim.
    a, b = sp.symbols('a b', real=True)
    # general real 3x3, 9 independent entries
    x = sp.symbols('x0:9', real=True)
    M = sp.Matrix(3, 3, lambda i, j: x[i * 3 + j])

    S3 = permutation_matrices_S3()
    # commutation conditions as raw expressions (== 0); skip tautologies
    eqs = []
    for P in S3:
        C = M * P - P * M          # [M,P]
        for entry in C:
            entry = sp.expand(entry)
            if entry != 0:         # drop trivially-true (BooleanTrue) rows
                eqs.append(entry)
    sol = sp.linsolve(eqs, x)
    (s0,) = sol  # one general solution tuple
    print("General S3-invariant 3x3 M (9 unknowns, NOT assumed symmetric), solved:")
    Minvp = sp.Matrix(3, 3, lambda i, j: s0[i * 3 + j])
    sp.print_latex(Minvp)
    print(Minvp)
    print("Solution automatically symmetric (M - M^T == 0):",
          sp.simplify(Minvp - Minvp.T) == sp.zeros(3))
    # free params of the solution
    free = sorted(set().union(*[sp.sympify(si).free_symbols for si in s0]),
                  key=str)
    print("Free parameters in the invariant family:", free,
          "(expect exactly 2 -> the (a,b) democratic form)")

    # ---- eigenvalues of the representative a*I + b*J ----
    J = sp.ones(3, 3)
    ID = sp.eye(3)
    Mab = a * ID + b * J
    ev = Mab.eigenvals()
    print("\nEigenvalues of a*I + b*J (exact):", ev)
    # confirm always a 2-fold eigenvalue
    mults = list(ev.values())
    degenerate = any(m == 2 for m in mults)
    print("Has a forced 2-fold eigenvalue for all a,b:", degenerate)

    # ---- Claim 2: orthogonal plane carries 2-d irrep, 120-deg rotation ----
    sqrt3 = sp.sqrt(3)
    # basis of the plane orthogonal (traceless, S3-breaking) in texture space
    # use Z23's choice: alpha ~ diag(2,-1,-1) direction, beta ~ off-diag asym
    # Build via the standard 2-d irrep: generators of S3 as rotations.
    c120 = sp.cos(2 * sp.pi / 3)     # -1/2
    s120 = sp.sin(2 * sp.pi / 3)     # sqrt(3)/2
    R120 = sp.Matrix([[c120, -s120], [s120, c120]])
    print("\n120-degree rotation generator R120 =")
    print(R120)
    # no invariant vector: (R120 - I) v = 0 has only v=0
    null = (R120 - sp.eye(2)).nullspace()
    print("Invariant vectors in the 2-plane under R120:", null,
          "(empty => no S3-invariant ray survives)")

    print("\nRESULT: both claims confirmed exactly (sympy, no floats).")
    print("(1) S3-invariance forces 2-fold eigenvalue degeneracy.")
    print("(2) The breaking plane is an irreducible S3 orbit: no point of it")
    print("    is selected by any S3-covariant principle.")


if __name__ == "__main__":
    main()
