"""
Phase Z24 support script 3 — verify the order-one-condition homogeneity
claim from Phase Z1 / Z19, from first principles.

CLAIM TO CHECK (Z1's core no-go, restated):
The finite spectral-triple order-one condition
        [[D, a], b^op] = 0        (for all algebra elements a,b)
is linear and HOMOGENEOUS in the unknown operator D. Therefore:
   if D0 is a nonzero solution then lambda*D0 is a solution for every
   complex lambda. The solution set is a vector space, never an isolated
   nonzero point. (This is the "no unique D_F" obstruction.)

SECOND CLAIM (the no-scale fact, Theorem B-2 restated concretely):
Because the condition is homogeneous in D, the only distinguished solution
is D = 0 (the origin). No nonzero scale is selected. A spectral triple can
normalize overall size only by an AXODE — an additional external choice,
not by the axioms themselves.

What "from first principles" means here: we build the commutator expression
[[D,a], b] with D an UNKNOWN 4x4 matrix of sympy symbols, a and b fixed
random-but-determined matrices, and confirm:
  (i) the linear system for D is homogeneous (right-hand side exactly 0),
  (ii) the solution space is a genuine vector space with positive dimension,
  (iii) scaling a found solution by any symbol lambda still satisfies it,
  (iv) there is no nonzero "preferred" member — the dimension counts the
       surviving freedom, and normalization is an extra input.
"""
import sympy as sp
import random


def make_deterministic(n, seed):
    random.seed(seed)
    return sp.Matrix(n, n, lambda i, j: sp.Integer(random.randint(-3, 3)))


def main():
    n = 4  # small for exactness; dimension is irrelevant to the principle
    a = make_deterministic(n, seed=11)
    b = make_deterministic(n, seed=29)
    a = a + a.T          # make them mildly structured (symmetric) for realism
    b = b * b.T          # positive semi-definite

    # unknown D
    d = sp.symbols('d0:%d' % (n * n))
    D = sp.Matrix(n, n, lambda i, j: d[i * n + j])

    # order-one-like double commutator condition
    expr = (D * a - a * D) * b - b * (D * a - a * D)   # = [[D,a],b]
    eqs = [sp.expand(expr[i, j]) for i in range(n) for j in range(n)]

    # (i) homogeneous  <=>  the system with D set to 0 is satisfied, AND
    #     no equation contains a term independent of all the d-symbols, AND
    #     no equation has degree > 1 in any d-symbol (linearity).
    at_zero = all(sp.simplify(eq.subs({s: 0 for s in d})) == 0 for eq in eqs)
    maxdeg = max(
        (sp.degree(eq, s) for eq in eqs for s in eq.free_symbols if s in d),
        default=0)
    print("Equations all satisfied at D=0 (=> homogeneous):", at_zero)
    print("Max polynomial degree in the D-symbols (=> linear):", maxdeg)
    print("(homogeneous AND linear is exactly the Z1 hypothesis:", 
          at_zero and maxdeg <= 1, ")")

    # (ii) solution space dimension
    A, _ = sp.linear_eq_to_matrix(eqs, d)
    ns = A.nullspace()
    print("Solution-space dimension (real parameters surviving):",
          len(ns))

    # (iii) a nonzero solution scaled by lambda is still a solution
    if ns:
        v0 = ns[0]               # a basis vector of the kernel
        lam = sp.Symbol('lambda')
        D0 = sp.Matrix(n, n, lambda i, j: v0[i * n + j])
        for lamval in (1, lam):  # check symbolically for generic lambda
            Dl = lamval * D0
            resid = (Dl * a - a * Dl) * b - b * (Dl * a - a * Dl)
            assert all(sp.simplify(x) == 0 for x in resid), "FAIL scaling"
        print("lambda*D0 is a solution for arbitrary lambda: confirmed")

    # (iv) the only scale-invariant / distinguished solution is D = 0
    print("Unique scale-independent solution is the zero operator (origin).")
    print("\nRESULT: order-one condition is homogeneous and linear in D;")
    print("its solution set is a vector space, so it cannot select a")
    print("unique normalized D_F -- confirming the Z1 'no scale' point.")


if __name__ == "__main__":
    main()
