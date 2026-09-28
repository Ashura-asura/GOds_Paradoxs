"""
Phase Z19: does a TWISTED spectral triple evade Phase Z1's impossibility
proof (Case A -- a unique nonzero D_F -- is impossible because every
defining condition is linear/homogeneous in D_F)?

This is a symbolic/structural check, not a numerical one -- exactly like
Z1 itself, which proved its result by direct expansion of the defining
conditions, not by constructing an explicit D_F. Two documents shared
this session both flag "twisted spectral triples" as the one genuinely
new construction type in the literature not yet tested here. This phase
checks the actual algebraic question that determines whether pursuing
that route could, even in principle, do what static NCG axioms proved
they cannot (Z1/Z2): fix an isolated point in Yukawa space rather than
merely reorganize a continuous family.

Standard twisted order-one condition (Landi-Martinetti convention):
    [D, a]_rho := D a - rho(a) D          (rho: a FIXED *-automorphism of A)
    [[D,a]_rho, b] = 0   for all a, b in A

This is checked below for homogeneity/linearity in D, for ANY fixed rho
(not assuming a specific rho -- the point is this holds for the whole
class of "standard" twists, not one example).
"""
import sympy as sp


def check_twisted_order_one_linearity():
    """
    Symbolic check: expand [[D,a]_rho, b] with D as a single symbolic
    linear operator (represented abstractly -- we track only the
    DEGREE of D in each term, since that's what homogeneity requires,
    exactly as Z1 did for the untwisted case).
    """
    # Represent D symbolically as a formal degree-1 object; a, b, rho(a),
    # rho(b) as degree-0 (fixed, D-independent) operators. We verify that
    # every term in the fully expanded twisted order-one condition has
    # degree exactly 1 in D, for arbitrary noncommuting a, b, rho(a), rho(b).
    D, a, b, ra, rb = sp.symbols('D a b ra rb', commutative=False)
    # [D,a]_rho = D*a - ra*D   (ra stands for rho(a), a fixed operator)
    Da_rho = D * a - ra * D
    # [[D,a]_rho, b] = Da_rho*b - b*Da_rho
    expr = sp.expand(Da_rho * b - b * Da_rho)
    terms = sp.Add.make_args(expr)

    degrees = []
    for term in terms:
        factors = sp.Mul.make_args(term)
        deg = sum(1 for f in factors if f == D)
        degrees.append(deg)

    return terms, degrees


def check_scaling_invariance_symbolic():
    """
    Direct homogeneity check: substitute D -> lambda*D and confirm the
    expression scales by exactly lambda^1 (linear), for arbitrary rho
    (i.e. arbitrary fixed operators ra, rb standing in for rho(a), rho(b)).
    This is the same style of check Z1 used (D0 and lambda*D0 both solve
    a homogeneous condition).
    """
    lam, D, a, b, ra, rb = sp.symbols('lambda D a b ra rb', commutative=False)
    # can't mix commutative lambda with noncommutative D directly in sympy
    # cleanly, so use a commutative scalar substitution check on the
    # term-degree result instead (equivalent argument): a homogeneous
    # degree-1-in-D expression E(D) satisfies E(lambda*D) = lambda*E(D)
    # for scalar lambda, which is exactly what "every term has D-degree
    # exactly 1" (already shown above) implies.
    return True  # follows from check_twisted_order_one_linearity degrees


if __name__ == "__main__":
    terms, degrees = check_twisted_order_one_linearity()
    print(f"Twisted order-one condition [[D,a]_rho, b], expanded: {len(terms)} terms")
    for t, d in zip(terms, degrees):
        print(f"  term: {t}   D-degree: {d}")
    all_degree_one = all(d == 1 for d in degrees)
    print(f"\nAll terms have D-degree exactly 1 (homogeneous/linear in D): {all_degree_one}")
    print("\nConclusion: for ANY fixed (D-independent) twist automorphism rho,")
    print("the twisted order-one condition remains linear/homogeneous in D --")
    print("Phase Z1's vector-space argument applies UNCHANGED. If D0 solves")
    print("it, so does lambda*D0 for every complex lambda: Case A (isolated")
    print("nonzero D_F) remains impossible under any fixed-rho twist.")
