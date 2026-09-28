"""
Phase Z18: decuplet (10 = Sym^3(3)) flavon of SU(3)_f.

Every prior non-minimal flavon this project tried (Z15 adjoint-8, Z16
sextet-6, Z17 fundamental+adjoint portal) used a representation whose
generic/forced vacuum has a CONTINUOUS residual stabilizer (U(1)^2, SO(3),
U(1)). This phase tests a genuinely different structural possibility:
does the decuplet (rank-3 symmetric tensor, "Sym^3(3)", dimension 10)
admit a vacuum with a purely FINITE residual stabilizer -- specifically
the "clock" subgroup Z3 x Z3 subset SU(3) that emerges for free (no
potential-minimization argument needed) whenever the flavon takes the
"diagonal cubic" form phi = a*e1^3 + b*e2^3 + c*e3^3 for ANY nonzero
complex a,b,c?

This is checked directly from the defining representation, not assumed:
for g = diag(w^p, w^q, w^r) in SU(3) (w = primitive cube root of unity,
p+q+r = 0 mod 3, giving exactly 9 elements), acting on the Sym^3
representation sends e_i^3 -> w^(3p_i) e_i^3 = e_i^3 EXACTLY, since
w^3 = 1 for any integer p_i. So g fixes phi exactly (not just up to
phase) for every one of the 9 elements, for ANY a,b,c -- this holds
before any statement about which (a,b,c) the potential actually prefers.

We then run the same order-one-style invariance test Z14-Z17 used
(g^T Y g = Y for the symmetric-channel generation matrix Y, under every
unbroken generator/group element) restricted to this finite Z3 x Z3,
and report the dimension of the surviving invariant subspace.
"""
import numpy as np
import itertools

w = np.exp(2j * np.pi / 3)  # primitive cube root of unity


def clock_element(p, q, r):
    return np.diag([w**p, w**q, w**r]).astype(complex)


def su3_clock_group():
    """All (p,q,r) in Z3^3 with p+q+r = 0 mod 3 -> 9 elements, exact SU(3) subgroup."""
    elems = []
    for p, q, r in itertools.product(range(3), repeat=3):
        if (p + q + r) % 3 == 0:
            elems.append(clock_element(p, q, r))
    assert len(elems) == 9
    return elems


def check_decuplet_fixed(elems, a=1.3 + 0.7j, b=-0.4 + 2.1j, c=0.9 - 1.1j):
    """
    Verify each clock element fixes phi = a*e1^3 + b*e2^3 + c*e3^3 EXACTLY,
    by direct action on the three monomials (e_i -> w^{p_i} e_i, so
    e_i^3 -> w^{3 p_i} e_i^3 = e_i^3).
    """
    max_resid = 0.0
    for g in elems:
        p_vec = np.array([np.log(g[i, i]) / (2j * np.pi / 3) for i in range(3)])
        p_vec = np.round(p_vec.real).astype(int) % 3
        phase_e1 = w ** (3 * p_vec[0])
        phase_e2 = w ** (3 * p_vec[1])
        phase_e3 = w ** (3 * p_vec[2])
        # phi's coefficients (a,b,c) after transformation:
        a2, b2, c2 = a * phase_e1, b * phase_e2, c * phase_e3
        resid = abs(a2 - a) + abs(b2 - b) + abs(c2 - c)
        max_resid = max(max_resid, resid)
    return max_resid


def invariant_symmetric_subspace(elems):
    """
    Dimension of the space of symmetric 3x3 complex Y with g^T Y g = Y
    for every g in `elems`, found by stacking the linear constraints
    (g^T (x) g^T - I) vec(Y) = 0 over a symmetric-matrix basis and
    taking the null space rank.
    """
    # basis for symmetric 3x3 complex matrices, 6-dimensional
    basis = []
    for i in range(3):
        for j in range(i, 3):
            E = np.zeros((3, 3), dtype=complex)
            if i == j:
                E[i, j] = 1.0
            else:
                E[i, j] = 1.0
                E[j, i] = 1.0
            basis.append(E)
    n = len(basis)  # 6

    rows = []
    for g in elems:
        for k, E in enumerate(basis):
            transformed = g.T @ E @ g
            # express (transformed - E) in the same basis, append as constraint row
            row = np.zeros(n, dtype=complex)
            for m, Eb in enumerate(basis):
                # basis is not orthonormal in the trivial sense off-diagonal (norm 2),
                # so project by solving least squares against full basis matrix
                pass
            rows.append((transformed - E).flatten())
    # stack all 3x3 differences (flattened) for k=0..5 and each g, but we need
    # per-basis-vector constraint: build one big matrix mapping basis coeffs -> flattened diff
    M = np.zeros((9 * len(elems) * n, n), dtype=complex)
    idx = 0
    for g in elems:
        for k, E in enumerate(basis):
            diff = (g.T @ E @ g - E).flatten()
            # this diff, as a function of "turning on only basis vector k with coeff 1",
            # is one COLUMN of the operator (I - g^T (x) g^T) restricted to sym space,
            # in the k-th basis direction. Collect all such diffs as columns of a big op.
            M[idx:idx + 9, k] = diff
            idx += 9

    # Null space of M (6 columns) via SVD
    U, S, Vh = np.linalg.svd(M)
    tol = 1e-9
    rank = np.sum(S > tol)
    nullity = n - rank
    return nullity, S


if __name__ == "__main__":
    elems = su3_clock_group()
    resid = check_decuplet_fixed(elems)
    print(f"Z3 x Z3 clock group: {len(elems)} elements")
    print(f"Max residual fixing phi = a*e1^3+b*e2^3+c*e3^3 (generic a,b,c): {resid:.3e}")

    nullity, singvals = invariant_symmetric_subspace(elems)
    print(f"Dimension of Sym^2(3) subspace invariant under full clock group: {nullity}")
    print(f"Singular values of constraint operator: {np.round(singvals, 4)}")
